import arcade
import random

from pyglet.graphics import Batch
from player import Ship, Bullet, ShipHitbox, Shield
from projectiles import ProjectileA, ProjectileB


class GameView(arcade.View):
    def __init__(self, star_list):
        super().__init__()
        self.background_color = (25, 20, 43)
        self.star_list = star_list
        self.keys_pressed = set()
        self.paused = False
        self.player_list = arcade.SpriteList()
        self.bullets_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.projectile_list_b = arcade.SpriteList()
        self.ship = Ship(self.window.width / 2, self.window.height / 5, 250, self.window.width, self.window.height)
        self.ship_hitbox = ShipHitbox(self.ship.center_x, self.ship.center_y)
        self.shield = Shield(self.ship.center_x, self.ship.center_y)
        self.player_list.append(self.ship)

        self.time = 0
        self.score = 0
        arcade.schedule(self.one_second, 1)
        self.lives = 3
        self.lives_texture = arcade.load_texture('sprites/live.png')
        self.lives_texture.size = 1.5
        self.invulnerable = False
        self.invulnerability_time = 1.2
        self.can_shoot = True
        self.shoot_cooldown = 0.4
        self.is_dashing = False
        self.dash_cooldown = 100
        self.dash_use_cd = 0.01
        self.dash_refill_cd = 0.05
        arcade.schedule(self.dash_refill, self.dash_refill_cd)
        self.projectile_cd = 1
        self.projectile_amo = 7
        self.projectile_b_rate = 30
        arcade.schedule(self.spawn_projectiles, self.projectile_cd)
        self.emitters = []

        self.batch = Batch()
        self.dash_cd = arcade.Text(str(self.dash_cooldown // 10 * 10) + '%', 0, self.window.height / 12 * 11,
                                   arcade.color.BABY_BLUE, font_size=50, anchor_x='left', anchor_y='top',
                                   bold=True, batch=self.batch)
        self.time_show = arcade.Text(str(self.time), self.width / 2, self.window.height,
                                     arcade.color.BABY_BLUE, font_size=60, anchor_x='center', anchor_y='top',
                                     bold=True, batch=self.batch)
        self.score_show = arcade.Text(str(self.score) + 'pts', self.window.width, self.window.height,
                                      arcade.color.BABY_BLUE, font_size=50, anchor_x='right', anchor_y='top',
                                      bold=True, batch=self.batch)

    def on_draw(self):
        self.clear()
        self.star_list.draw()

        self.bullets_list.draw()
        self.player_list.draw()
        self.projectile_list.draw()

        self.dash_cd = arcade.Text(str(self.dash_cooldown // 10 * 10) + '%', 0, self.window.height / 12 * 11,
                                   arcade.color.BABY_BLUE, font_size=50, anchor_x='left', anchor_y='top',
                                   bold=True, batch=self.batch)
        self.time_show = arcade.Text(str(self.time), self.width / 2, self.window.height,
                                     arcade.color.BABY_BLUE, font_size=60, anchor_x='center', anchor_y='top',
                                     bold=True, batch=self.batch)
        self.score_show = arcade.Text(str(self.score) + 'pts', self.window.width, self.window.height,
                                      arcade.color.BABY_BLUE, font_size=50, anchor_x='right', anchor_y='top',
                                      bold=True, batch=self.batch)

        for i in range(self.lives):
            rect = arcade.Rect(i * 100, i * 100 + 100, self.window.height, self.window.height - 100, 100, 100,
                               i * 100 + 50, self.window.height - 50)
            arcade.draw_texture_rect(self.lives_texture, rect)

        if not self.ship.dead:
            self.batch.draw()

    def on_update(self, delta_time):
        if self.paused:
            return

        if self.dash_cooldown <= 0:
            self.is_dashing = False
            self.dash_cooldown = 0
            arcade.unschedule(self.dash_use)

        if self.lives <= 0:
            self.game_over()

        self.player_list.update(delta_time, self.keys_pressed, self.is_dashing)
        self.ship_hitbox.center_x = self.ship.center_x
        self.ship_hitbox.center_y = self.ship.center_y
        self.shield.center_x = self.ship.center_x
        self.shield.center_y = self.ship.center_y
        self.bullets_list.update(delta_time)
        self.projectile_list.update(delta_time)

        for bullet in self.bullets_list:
            projectiles_hit_list = arcade.check_for_collision_with_list(bullet, self.projectile_list_b)
            if projectiles_hit_list:
                bullet.remove_from_sprite_lists()
                for projectile in projectiles_hit_list:
                    self.destroy_projectile(projectile)

        ship_hit_list = arcade.check_for_collision_with_list(self.ship_hitbox, self.projectile_list)
        if ship_hit_list:
            if not self.invulnerable:
                self.lives -= 1
                self.player_list.append(self.shield)
                arcade.schedule(self.invulnerability_toggle, self.invulnerability_time)
                self.invulnerable = True
            for projectile in ship_hit_list:
                self.destroy_projectile(projectile)

        for star in self.star_list:
            star.center_y -= 16 * delta_time
            if star.center_y < -8:
                star.center_y = self.window.height + 8

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
            self.paused = True
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

    def one_second(self, delta_time):
        if self.paused:
            return

        self.time += 1
        self.score += 50

    def weapon_ready(self, delta_time):
        if self.paused:
            return

        self.can_shoot = True
        arcade.unschedule(self.weapon_ready)

    def dash_use(self, delta_time):
        if self.paused:
            return

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

    def dash_refill(self, delta_time):
        if self.paused:
            return

        if self.dash_cooldown < 100:
            self.dash_cooldown += 1

    def invulnerability_toggle(self, delta_time):
        if self.paused:
            return

        self.invulnerable = False
        if self.shield in self.player_list:
            self.shield.remove_from_sprite_lists()
        arcade.unschedule(self.invulnerability_toggle)

    def spawn_projectiles(self, delta_time):
        if self.paused:
            return

        for i in range(self.projectile_amo):
            n = random.randint(1, 100)
            p_x = self.ship.center_x + random.randint(-200, 200)

            if p_x > self.window.width:
                p_x = self.window.width
            elif p_x < 0:
                p_x = 0
            p_y = self.ship.center_y + random.randint(-200, 200)
            if p_y > self.window.width:
                p_y = self.window.width
            elif p_y < 0:
                p_y = 0

            if n > self.projectile_b_rate:
                projectile = ProjectileA(random.randint(-200, self.window.width + 200), self.window.height + 200,
                                         p_x, p_y, random.randint(100, 200), self.window.width,
                                         self.window.height)
            else:
                projectile = ProjectileB(random.randint(-200, self.window.width + 200), self.window.height + 200,
                                         p_x, p_y, random.randint(100, 200), self.window.width,
                                         self.window.height)
                self.projectile_list_b.append(projectile)
            self.projectile_list.append(projectile)

    def destroy_projectile(self, projectile):
        if projectile.__class__.__name__ == 'ProjectileB':
            self.score += 200
        projectile.remove_from_sprite_lists()

    def game_over(self):
        end_view = self.window.view_dict['end_view'](self)
        self.ship.dead = True
        self.shield.remove_from_sprite_lists()
        self.paused = True
        self.window.show_view(end_view)
