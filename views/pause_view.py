import arcade

from pyglet.graphics import Batch
from arcade.gui import UIManager, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.background_color = (25, 20, 43)
        self.manager = UIManager()
        self.manager.enable()
        self.game_view = game_view
        self.batch = Batch()
        self.pause_text = arcade.Text('PAUSED', self.window.width / 2, self.window.height / 3 * 2,
                                      arcade.color.RED, font_size=80, anchor_x='center', batch=self.batch)

        self.anchor_layout = UIAnchorLayout()
        self.setup_widgets()
        self.manager.add(self.anchor_layout)

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_lbwh_rectangle_filled(0, 0, self.window.width, self.window.height, (0, 0, 0, 100))
        self.batch.draw()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.continue_g()

    def setup_widgets(self):
        continue_btn = UIFlatButton(text='CONTINUE', width=300, height=70, color=arcade.color.BLUE)
        continue_btn.on_click = lambda event: self.continue_g()
        self.anchor_layout.add(continue_btn, align_x=0, align_y=-90)

        restart_btn = UIFlatButton(text='TRY AGAIN', width=300, height=70, color=arcade.color.BLUE)
        restart_btn.on_click = lambda event: self.restart()
        self.anchor_layout.add(restart_btn, align_x=0, align_y=-180)

        quit_btn = UIFlatButton(text='MAIN MENU', width=300, height=70, color=arcade.color.BLUE)
        quit_btn.on_click = lambda event: self.quit_g()
        self.anchor_layout.add(quit_btn, align_x=0, align_y=-270)

    def continue_g(self):
        self.game_view.paused = False
        self.window.show_view(self.game_view)
        self.manager.disable()

    def restart(self):
        game_view = self.window.view_dict['game_view'](self.game_view.star_list)
        self.window.show_view(game_view)
        self.manager.disable()

    def quit_g(self):
        menu_view = self.window.view_dict['menu_view']()
        self.window.show_view(menu_view)
        self.manager.disable()
