import arcade
import random

from pyglet.graphics import Batch
from arcade.gui import UIManager, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = (25, 20, 43)
        self.manager = UIManager()
        self.manager.enable()

        self.star_list = arcade.SpriteList()
        self.update_stars()

        self.batch = Batch()
        self.main_text = arcade.Text('CosmicDash', self.window.width / 2, self.window.height / 3 * 2,
                                     arcade.color.RED, font_size=80, anchor_x='center', bold=True, batch=self.batch)

        self.anchor_layout = UIAnchorLayout()
        self.setup_widgets()
        self.manager.add(self.anchor_layout)

    def on_draw(self):
        self.clear()
        self.star_list.draw()
        arcade.draw_lbwh_rectangle_filled(0, 0, self.window.width, self.window.height, (242, 48, 255, 40))
        arcade.draw_lbwh_rectangle_filled(240, 175, 320, 270, (0, 0, 0, 170))
        self.batch.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        pass

    def update_stars(self):
        self.star_list.clear()
        for i in range(100):
            star = arcade.Sprite('sprites/star.png', random.randint(80, 110) / 100,
                                 random.randint(0, int(self.window.width)), random.randint(0, int(self.window.height)))
            self.star_list.append(star)

    def setup_widgets(self):
        start_btn = UIFlatButton(text='START', width=300, height=70, color=arcade.color.BLUE)
        start_btn.on_click = lambda event: self.start_g()
        self.anchor_layout.add(start_btn, align_x=0, align_y=0)

        records_btn = UIFlatButton(text='RECORDS', width=300, height=70, color=arcade.color.BLUE)
        records_btn.on_click = lambda event: self.records()
        self.anchor_layout.add(records_btn, align_x=0, align_y=-90)

        quit_btn = UIFlatButton(text='QUIT', width=300, height=70, color=arcade.color.BLUE)
        quit_btn.on_click = lambda event: self.quit_g()
        self.anchor_layout.add(quit_btn, align_x=0, align_y=-180)

    def start_g(self):
        game_view = self.window.view_dict['game_view'](self.star_list)
        self.window.show_view(game_view)
        self.manager.disable()

    def records(self):
        records_view = self.window.view_dict['records_view'](self.star_list)
        self.window.show_view(records_view)
        self.manager.disable()

    def quit_g(self):
        self.window.close()
        self.manager.disable()
