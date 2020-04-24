import random
import time
from enum import Enum

import arcade

from triple_vision import Settings as s
from triple_vision import Tile
from triple_vision.entities.entities import LivingEntity
from triple_vision.entities.sprites import HealthBar, MovingSprite
from triple_vision.entities.weapons import ChargedLaserProjectile
from triple_vision.pathfinding import PathFinder
from triple_vision.utils import pixels_to_tile, tile_to_pixels
from triple_vision.sound import SoundManager


class States(Enum):
    # TODO save player states by current weapon and update cursor
    IDLE = 0
    # MOVING = 1
    ATTACKING_RANGED = 2
    ATTACKING_MELEE = 3
    AIMING_BLOCKED = 4
    AIMING_NOT_BLOCKED = 5


class Player(LivingEntity, MovingSprite):

    def __init__(self, view: arcade.View, gender: str) -> None:
        super().__init__(
            sprite_name='wizzard',
            assets_path='assets/wizard',
            is_colored=True,
            has_hit_frame=True,
            gender=gender,
            scale=s.SCALING,
            hp=1000,
            ctx=view.game_manager,
            moving_speed=3,
            rotate=False
        )

        self.view = view
        self.last_shot = time.time()

        self.state = States.IDLE

        self.is_alive = True
        self.attack_multiplier = 1
        self.dexterity = 0.75

        self._curr_color = self.curr_color

        self.path_finder = PathFinder()
        self.path = None

        self.mana_bar: HealthBar = None
        self.health_bar: PlayerLiveManager = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    @property
    def curr_color(self):
        return self._curr_color

    @curr_color.setter
    def curr_color(self, value):
        if value == 'red':
            self.resistance = 0.1
            self.attack_multiplier = 1.5
            self.speed_multiplier = 1.1
            self.dexterity = 0.6

        elif value == 'green':
            self.resistance = 0.5
            self.attack_multiplier = 1.1
            self.speed_multiplier = 1
            self.dexterity = 0.75

        elif value == 'blue':
            self.resistance = 0
            self.attack_multiplier = 1
            self.speed_multiplier = 1.5
            self.dexterity = 0.5

        else:
            raise ValueError('Color can only be red, green, or blue.')

        self._curr_color = value

    def setup(self) -> None:
        self.set_hit_box([
            (-4.0, -1.0),
            (4.0, -1.0),
            (6.0, -3.0),
            (6.0, -11.0),
            (4.0, -13.0),
            (-4.0, -13.0),
            (-6.0, -11.0),
            (-6.0, -3.0)
        ])
        self.curr_color = 'red'

        self.mana_bar = HealthBar(
            self.view,
            fill_part_filename="assets/healthbar/mana_fill_part.png",
            fill_part_width=44.0,
            filename="assets/healthbar/mana_bar_border.png",
            center_x=420,
            center_y=18,
            scale=1,
            auto_filling_speed=1.5
        )
        self.health_bar = PlayerLiveManager(self.view, self.hp)

        center = tuple()

        while True:
            center = tile_to_pixels(random.randrange(0, s.MAP_SIZE[0]), random.randrange(0, s.MAP_SIZE[1]))

            if (
                    len(arcade.get_sprites_at_point(center, self.view.collision_list)) == 0 and
                    len(arcade.get_sprites_at_point(center, self.view.map.sprites)) > 0
            ):
                break

        self.center_x = center[0]
        self.center_y = center[1] + s.PLAYER_CENTER_Y_COMPENSATION

    def process_key_press(self, key) -> None:
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

    def process_key_release(self, key) -> None:
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

    def process_left_mouse_press(self, x, y, charge) -> None:
        if time.time() - self.last_shot < self.dexterity:
            SoundManager.add_sound("empty_gun.wav")
            SoundManager.play_sound("empty_gun.wav")
            return

        bullet = ChargedLaserProjectile(
            charge=charge,
            center_x=self.center_x,
            center_y=self.center_y,
            rotate=True
        )

        bullet.move_to(x, y, set_target=False)
        bullet.play_activate_sound()
        self.view.game_manager.player_projectiles.append(bullet)
        self.last_shot = time.time()
        self.mana_bar.remove_filling_part()
        self.state = States.ATTACKING_RANGED

    def kill(self):
        self.is_alive = False
        super().kill()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        change_x = 0
        change_y = 0

        if self.up_pressed and not self.down_pressed:
            change_y = 1
        elif self.down_pressed and not self.up_pressed:
            change_y = -1

        if self.left_pressed and not self.right_pressed:
            change_x = -1
        elif self.right_pressed and not self.left_pressed:
            change_x = 1

        dest = tile_to_pixels(
            *pixels_to_tile(
                self.center_x + change_x * Tile.SCALED,
                self.center_y + change_y * Tile.SCALED
            )
        )
        if not arcade.get_sprites_at_exact_point(dest, self.view.collision_list):
            self.move_to(dest[0], dest[1] + s.PLAYER_CENTER_Y_COMPENSATION)
            # self.state = States.MOVING

        super().on_update(delta_time)

    def update_health_bars(self, delta_time):
        self.mana_bar.on_update(delta_time)
        self.health_bar.update()

    def draw(self):
        super().draw()
        self.mana_bar.draw()
        self.health_bar.draw()


class PlayerLiveManager:
    def __init__(
        self,
        view,
        *args,
        life_count: int = 10,
        is_filled: bool = True,
        scale: float = 1,
        **kwargs
    ) -> None:

        super().__init__(*args, scale=scale, **kwargs)
        self.view = view
        self.camera = self.view.camera
        self.player = self.view.player
        self.life_count = life_count
        self.margin = 30
        self.hearts = arcade.SpriteList()
        self.heart_map = [2, 2, 2]
        self.scaling = scale

        if not is_filled:
            return

        for i in range(3):
            self.hearts.append(
                arcade.Sprite(
                    "assets/hearts/heart_2.png",
                    center_x=100 + i * self.margin,
                    center_y=100,
                    scale=self.scaling
                )
            )

    def update_hearts(self):
        for i in range(3):
            current_heart = self.hearts.sprite_list[i]
            self.hearts.sprite_list[i] = arcade.Sprite(
                f"assets/hearts/heart_{i}.png",
                center_x=current_heart.center_x,
                center_y=current_heart.center_y,
                scale=self.scaling
            )

    def update(self):
        # hearts = round(self.life_count / 3, 1)
        for index, h in enumerate(self.heart_map):
            heart_pos = h * (index + 1)
            if heart_pos > self.life_count:
                self.heart_map[index] -= 1
            elif heart_pos < self.life_count:
                self.heart_map[index] += 1

    def draw(self):
        self.hearts.draw()