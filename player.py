import arcade
import math


class Ship(arcade.Sprite):
    def __init__(self, x, y, speed, sw, sh):
        super().__init__('sprites/ship.png', scale=1)
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.screen_wight = sw
        self.screen_height = sh
        self.speed_x = 0
        self.speed_y = 0

    def update(self, delta_time, keys):
        dx, dy = 0, 0
        if arcade.key.W in keys: dy += 1
        if arcade.key.S in keys: dy -= 1
        if arcade.key.A in keys: dx -= 1
        if arcade.key.D in keys: dx += 1
        if dx != 0 and dy != 0:
            dx *= 1 / math.sqrt(2)
            dy *= 1 / math.sqrt(2)
        self.center_x += self.speed * delta_time * dx
        self.center_y += self.speed * delta_time * dy
        self.center_x = max(self.width // 2, min(self.center_x, self.screen_wight - self.width // 2))
        self.center_y = max(self.height // 2, min(self.center_y, self.screen_height - self.height // 2))

    def dash(self, end_x, end_y, dst):
        angle = math.atan2(end_y - self.center_y, end_x - self.center_x)
        dx = math.cos(angle)
        dy = math.sin(angle)
        angle = math.degrees(-angle)
        self.center_x += self.speed * dx
        self.center_y += self.speed * dy


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, speed, sw, sh):
        super().__init__('sprites/bullet.png')
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
        if not (0 < self.center_x < self.screen_wight and 0 < self.center_y < self.screen_height):
            self.remove_from_sprite_lists()
