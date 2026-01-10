import arcade

from game_view import GameView
from pyglet.graphics import Batch
from random import randint


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = (25, 20, 43)

        self.star_list = arcade.SpriteList()
        for i in range(100):
            star = arcade.Sprite('sprites/star.png', randint(80, 110) / 100,
                                 randint(0, int(self.window.width)), randint(0, int(self.window.height)))
            self.star_list.append(star)

        self.batch = Batch()
        self.main_text = arcade.Text("Главное Меню", self.window.width / 2, self.window.height / 2 + 50,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы начать!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.star_list.draw()
        arcade.draw_lbwh_rectangle_filled(0, 0, self.window.width, self.window.height, (242, 48, 255, 40))
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = GameView(self)
            self.window.show_view(game_view)
