import arcade

from pause_view import PauseView


class GameView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.background_color = (25, 20, 43)
        self.menu_view = menu_view
        self.star_list = menu_view.star_list
        self.keys_pressed = set()

    def on_draw(self):
        self.clear()
        self.star_list.draw()

    def on_update(self, delta_time):
        for star in self.star_list:
            star.center_y -= 10 * delta_time
            if star.center_y < -5:
                star.center_y = self.window.height + 5

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
