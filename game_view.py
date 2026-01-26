import random

import arcade

from pyglet.graphics import Batch
from player import Ship, Bullet
from projectiles import ProjectileA


class GameView(arcade.View):
    def __init__(self, star_list):
        super().__init__()
        self.background_color = (25, 20, 43)
        self.star_list = star_list
        self.keys_pressed = set()
        self.player_list = arcade.SpriteList()
        self.bullets_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.ship = Ship(self.window.width / 2, self.window.height / 5, 250, self.window.width, self.window.height)
        self.player_list.append(self.ship)
        self.can_shoot = True
        self.shoot_cooldown = 0.4
        self.is_dashing = False
        self.dash_cooldown = 100
        self.dash_use_cd = 0.01
        self.dash_refill_cd = 0.05
        arcade.schedule(self.dash_refill, self.dash_refill_cd)
        self.projectile_cd = 0.1
        self.projectile_amo = 1
        arcade.schedule(self.spawn_projectiles, self.projectile_cd)
        self.emitters = []

        self.batch = Batch()
        self.dash_cd = arcade.Text(str(self.dash_cooldown // 10 * 10), 0, self.window.height,
                                   arcade.color.RED, font_size=60, anchor_x='left', anchor_y='top',
                                   bold=True, batch=self.batch)

    def on_draw(self):
        self.clear()
        self.star_list.draw()
        self.projectile_list.draw()

        self.bullets_list.draw()
        self.player_list.draw()
        self.dash_cd = arcade.Text(str(self.dash_cooldown // 10 * 10), 0, self.window.height,
                                   arcade.color.RED, font_size=60, anchor_x='left', anchor_y='top',
                                   bold=True, batch=self.batch)
        self.batch.draw()

    def on_update(self, delta_time):
        if self.dash_cooldown <= 0:
            self.is_dashing = False
            self.dash_cooldown = 0
            arcade.unschedule(self.dash_use)

        self.player_list.update(delta_time, self.keys_pressed, self.is_dashing)
        self.bullets_list.update(delta_time)
        self.projectile_list.update(delta_time)
        for star in self.star_list:
            star.center_y -= 10 * delta_time
            if star.center_y < -5:
                star.center_y = self.window.height + 5

        emitters_copy = self.emitters.copy()
        for e in emitters_copy:
            e.update(delta_time)
        for e in emitters_copy:
            if e.can_reap():
                self.emitters.remove(e)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.ESCAPE:
            pause_view = self.window.view_dict['pause_view'](self)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.can_shoot:
            self.bullets_list.append(Bullet(self.ship.center_x, self.ship.center_y, x, y, 650,
                                            self.window.width, self.window.height))
            self.can_shoot = False
            arcade.schedule(self.weapon_ready, self.shoot_cooldown)

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.is_dashing = True
            arcade.schedule(self.dash_use, self.dash_use_cd)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.is_dashing = False
            arcade.unschedule(self.dash_use)

    def weapon_ready(self, delta_time):
        self.can_shoot = True
        arcade.unschedule(self.weapon_ready)

    def dash_use(self, delta_time):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

    def dash_refill(self, delta_time):
        if self.dash_cooldown < 100:
            self.dash_cooldown += 1

    def spawn_projectiles(self, delta_time):
        for i in range(self.projectile_amo):
            projectile = ProjectileA(random.randint(-200, self.window.width + 200), self.window.height + 200,
                                     self.ship.center_x, self.ship.center_y, 150, self.window.width, self.window.height)
            self.projectile_list.append(projectile)
