import arcade

from pyglet.graphics import Batch
from random import randint


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = (25, 20, 43)
        self.mouse_pos = (0, 0)

        self.star_list = arcade.SpriteList()
        self.update_stars()

        self.batch = Batch()
        self.main_text = arcade.Text('CosmicDash', self.window.width / 2, self.window.height / 2 + 100,
                                     arcade.color.RED, font_size=60, anchor_x='center', bold=True, batch=self.batch)
        self.start_text = arcade.Text('Start', self.window.width / 2, self.window.height / 2 - 20,
                                      arcade.color.RED, font_size=40, anchor_x='center', batch=self.batch)

    def on_draw(self):
        self.clear()
        self.star_list.draw()
        arcade.draw_lbwh_rectangle_filled(0, 0, self.window.width, self.window.height, (242, 48, 255, 40))
        if 340 <= self.mouse_pos[0] <= 460 and 370 <= self.mouse_pos[1] <= 420:
            arcade.draw_lbwh_rectangle_filled(340, 370, 120, 50, arcade.color.BLUE)
        self.batch.draw()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if 340 <= x <= 460 and 370 <= y <= 420:
            game_view = self.window.view_dict['game_view'](self.star_list)
            self.window.show_view(game_view)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = (x, y)

    def update_stars(self):
        self.star_list.clear()
        for i in range(100):
            star = arcade.Sprite('sprites/star.png', randint(80, 110) / 100,
                                 randint(0, int(self.window.width)), randint(0, int(self.window.height)))
            self.star_list.append(star)

