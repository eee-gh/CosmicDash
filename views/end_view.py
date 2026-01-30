import arcade

from pyglet.graphics import Batch
from arcade.gui import UIManager, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout


class EndView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.background_color = (25, 20, 43)
        self.manager = UIManager()
        self.manager.enable()
        self.game_view = game_view
        self.time = game_view.time
        self.score = game_view.score
        self.alph = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.record_saved = False
        self.c1, self.c2, self.c3 = 0, 0, 0
        self.name = self.alph[self.c1] + self.alph[self.c2] + self.alph[self.c3]

        self.batch = Batch()
        self.go_text = arcade.Text('GAME OVER!', self.window.width / 2, self.window.height / 5 * 4,
                                   arcade.color.RED, font_size=80, anchor_x='center', bold=True, batch=self.batch)

        self.name_l1 = arcade.Text(self.alph[self.c1], self.window.width / 14 * 5.5, self.window.height / 2,
                                   arcade.color.BLUE, font_size=80, anchor_x='center', anchor_y='center', bold=True,
                                   batch=self.batch)
        self.name_l2 = arcade.Text(self.alph[self.c2], self.window.width / 2, self.window.height / 2,
                                   arcade.color.BLUE, font_size=80, anchor_x='center', anchor_y='center', bold=True,
                                   batch=self.batch)
        self.name_l3 = arcade.Text(self.alph[self.c3], self.window.width / 14 * 8.5, self.window.height / 2,
                                   arcade.color.BLUE, font_size=80, anchor_x='center', anchor_y='center', bold=True,
                                   batch=self.batch)

        self.score_text = arcade.Text(f'SCORE:', 0, self.window.height / 12 * 8,
                                      arcade.color.BABY_BLUE, font_size=40, anchor_x='left', anchor_y='top',
                                      bold=True, batch=self.batch)
        self.score_show = arcade.Text(f'{self.score}PTS', 0, self.window.height / 12 * 7,
                                      arcade.color.BABY_BLUE, font_size=40, anchor_x='left', anchor_y='top',
                                      bold=True, batch=self.batch)
        self.time_text = arcade.Text(f'TIME:', 0, self.window.height / 12 * 5,
                                     arcade.color.BABY_BLUE, font_size=40, anchor_x='left', anchor_y='top',
                                     bold=True, batch=self.batch)
        self.time_show = arcade.Text(f'{self.time}S', 0, self.window.height / 12 * 4,
                                     arcade.color.BABY_BLUE, font_size=40, anchor_x='left', anchor_y='top',
                                     bold=True, batch=self.batch)

        self.anchor_layout = UIAnchorLayout()
        self.setup_widgets()
        self.manager.add(self.anchor_layout)

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_lbwh_rectangle_filled(0, 0, self.window.width, self.window.height, (0, 0, 0, 150))

        self.name_l1 = arcade.Text(self.alph[self.c1], self.window.width / 14 * 5.5, self.window.height / 2,
                                   arcade.color.BLUE, font_size=80, anchor_x='center', anchor_y='center', bold=True,
                                   batch=self.batch)
        self.name_l2 = arcade.Text(self.alph[self.c2], self.window.width / 2, self.window.height / 2,
                                   arcade.color.BLUE, font_size=80, anchor_x='center', anchor_y='center', bold=True,
                                   batch=self.batch)
        self.name_l3 = arcade.Text(self.alph[self.c3], self.window.width / 14 * 8.5, self.window.height / 2,
                                   arcade.color.BLUE, font_size=80, anchor_x='center', anchor_y='center', bold=True,
                                   batch=self.batch)

        self.batch.draw()
        self.manager.draw()

    def setup_widgets(self):
        up1 = UIFlatButton(text='/\\', width=55, height=55, color=arcade.color.BLUE)
        up1.on_click = lambda event: self.change_name(1, True)
        self.anchor_layout.add(up1, align_x=-86, align_y=65)

        up2 = UIFlatButton(text='/\\', width=55, height=55, color=arcade.color.BLUE)
        up2.on_click = lambda event: self.change_name(2, True)
        self.anchor_layout.add(up2, align_x=0, align_y=65)

        up3 = UIFlatButton(text='/\\', width=55, height=55, color=arcade.color.BLUE)
        up3.on_click = lambda event: self.change_name(3, True)
        self.anchor_layout.add(up3, align_x=86, align_y=65)

        down1 = UIFlatButton(text='\\/', width=55, height=55, color=arcade.color.BLUE)
        down1.on_click = lambda event: self.change_name(1, False)
        self.anchor_layout.add(down1, align_x=-86, align_y=-80)

        down2 = UIFlatButton(text='\\/', width=55, height=55, color=arcade.color.BLUE)
        down2.on_click = lambda event: self.change_name(2, False)
        self.anchor_layout.add(down2, align_x=0, align_y=-80)

        down3 = UIFlatButton(text='\\/', width=55, height=55, color=arcade.color.BLUE)
        down3.on_click = lambda event: self.change_name(3, False)
        self.anchor_layout.add(down3, align_x=86, align_y=-80)

        save_rec = UIFlatButton(text='SAVE', width=120, height=120, color=arcade.color.BLUE)
        save_rec.on_click = lambda event: self.save_record(save_rec)
        self.anchor_layout.add(save_rec, align_x=250, align_y=-5)

        restart_btn = UIFlatButton(text='TRY AGAIN', width=300, height=70, color=arcade.color.BLUE)
        restart_btn.on_click = lambda event: self.restart()
        self.anchor_layout.add(restart_btn, align_x=0, align_y=-180)

        quit_btn = UIFlatButton(text='MAIN MENU', width=300, height=70, color=arcade.color.BLUE)
        quit_btn.on_click = lambda event: self.quit_m()
        self.anchor_layout.add(quit_btn, align_x=0, align_y=-270)

    def change_name(self, n, d):
        a = 1 if d else -1

        if n == 1:
            self.c1 += a
            if self.c1 < 0:
                self.c1 = len(self.alph) + self.c1
            elif self.c1 > len(self.alph) - 1:
                self.c1 = self.c1 % len(self.alph)
        elif n == 2:
            self.c2 += a
            if self.c2 < 0:
                self.c2 = len(self.alph) + self.c2
            elif self.c2 > len(self.alph) - 1:
                self.c2 = self.c2 % len(self.alph)
        elif n == 3:
            self.c3 += a
            if self.c3 < 0:
                self.c3 = len(self.alph) + self.c3
            elif self.c3 > len(self.alph) - 1:
                self.c3 = self.c2 % len(self.alph)

    def save_record(self, btn):
        if self.record_saved:
            return
        self.window.db_manager.add_record(self.alph[self.c1] + self.alph[self.c2] + self.alph[self.c3],
                                          self.time, self.score)
        self.record_saved = True
        btn.text = 'SAVED!'

    def restart(self):
        game_view = self.window.view_dict['game_view'](self.game_view.star_list)
        self.window.show_view(game_view)
        self.manager.disable()

    def quit_m(self):
        menu_view = self.window.view_dict['menu_view']()
        self.window.show_view(menu_view)
        self.manager.disable()
