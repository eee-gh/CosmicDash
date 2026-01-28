import arcade
import math


class ProjectileA(arcade.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, speed, sw, sh):
        texture = arcade.make_soft_square_texture(50, arcade.color.RED, 255)
        super().__init__(texture)
        self.center_x = start_x
        self.center_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.speed = speed
        self.screen_wight = sw
        self.screen_height = sh
        self.angle = math.atan2(self.end_y - self.center_y, self.end_x - self.center_x)
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        self.angle = math.degrees(-self.angle)

    def update(self, delta_time):
        self.center_x += self.speed * delta_time * self.dx
        self.center_y += self.speed * delta_time * self.dy
        if self.center_x < -200:
            self.remove_from_sprite_lists()


class ProjectileB(arcade.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, speed, sw, sh):
        texture = arcade.make_soft_square_texture(50, arcade.color.GREEN, 255)
        super().__init__(texture)
        self.center_x = start_x
        self.center_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.speed = speed
        self.screen_wight = sw
        self.screen_height = sh
        self.angle = math.atan2(self.end_y - self.center_y, self.end_x - self.center_x)
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        self.angle = math.degrees(-self.angle)

    def update(self, delta_time):
        self.center_x += self.speed * delta_time * self.dx
        self.center_y += self.speed * delta_time * self.dy
        if self.center_x < -200:
            self.remove_from_sprite_lists()
