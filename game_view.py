import arcade

from player import Ship, Bullet


class GameView(arcade.View):
    def __init__(self, star_list):
        super().__init__()
        self.background_color = (25, 20, 43)
        self.star_list = star_list
        self.keys_pressed = set()
        self.player_list = arcade.SpriteList()
        self.bullets_list = arcade.SpriteList()
        self.ship = Ship(self.window.width / 2, self.window.height / 5, 250, self.window.width, self.window.height)
        self.player_list.append(self.ship)

    def on_draw(self):
        self.clear()
        self.star_list.draw()
        self.bullets_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update(delta_time, self.keys_pressed)
        self.bullets_list.update(delta_time)
        for star in self.star_list:
            star.center_y -= 10 * delta_time
            if star.center_y < -5:
                star.center_y = self.window.height + 5

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.ESCAPE:
            pause_view = self.window.view_dict['pause_view'](self)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.bullets_list.append(Bullet(self.ship.center_x, self.ship.center_y, x, y, 650,
                                            self.window.width, self.window.height))
