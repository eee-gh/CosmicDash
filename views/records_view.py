import arcade

from pyglet.graphics import Batch
from arcade.gui import UIManager, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout


class RecordsView(arcade.View):
    def __init__(self, star_list):
        super().__init__()
        self.background_color = (25, 20, 43)
        self.manager = UIManager()
        self.manager.enable()
        self.star_list = star_list

        self.batch = Batch()
        self.main_text = arcade.Text('RECORDS', self.window.width / 2, self.window.height,
                                     arcade.color.YELLOW, font_size=80, anchor_x='center', anchor_y='top',
                                     bold=True, batch=self.batch)
        self.r1 = arcade.Text('', self.window.width / 2, self.window.height / 7 * 5,
                              arcade.color.YELLOW, font_size=50, anchor_x='center', anchor_y='center', batch=self.batch)
        self.r2 = arcade.Text('', self.window.width / 2, self.window.height / 7 * 4,
                              arcade.color.GREEN, font_size=50, anchor_x='center', anchor_y='center', batch=self.batch)
        self.r3 = arcade.Text('', self.window.width / 2, self.window.height / 7 * 3,
                              arcade.color.RED, font_size=50, anchor_x='center', anchor_y='center', batch=self.batch)
        self.r4 = arcade.Text('', self.window.width / 2, self.window.height / 7 * 2,
                              arcade.color.BLUE, font_size=50, anchor_x='center', anchor_y='center', batch=self.batch)
        self.r5 = arcade.Text('', self.window.width / 2, self.window.height / 7 * 1,
                              arcade.color.BLUE, font_size=50, anchor_x='center', anchor_y='center', batch=self.batch)

        self.anchor_layout = UIAnchorLayout()
        self.setup_widgets()
        self.manager.add(self.anchor_layout)

        self.records = self.window.db_manager.get_records()
        if len(self.records) > 0:
            self.r1.text = f'1. {self.records[0][0]}   {self.records[0][1]}S   {self.records[0][2]}PTS'
        if len(self.records) > 1:
            self.r2.text = f'2. {self.records[1][0]}   {self.records[1][1]}S   {self.records[1][2]}PTS'
        if len(self.records) > 2:
            self.r3.text = f'3. {self.records[2][0]}   {self.records[2][1]}S   {self.records[2][2]}PTS'
        if len(self.records) > 3:
            self.r4.text = f'4. {self.records[3][0]}   {self.records[3][1]}S   {self.records[3][2]}PTS'
        if len(self.records) > 4:
            self.r5.text = f'5. {self.records[4][0]}   {self.records[4][1]}S   {self.records[4][2]}PTS'

    def on_draw(self):
        self.clear()
        self.star_list.draw()
        arcade.draw_lbwh_rectangle_filled(0, 0, self.window.width, self.window.height, (255, 17, 0, 60))
        arcade.draw_lbwh_rectangle_filled(50, 50, 700, 600, (0, 0, 0, 220))
        self.batch.draw()
        self.manager.draw()

    def setup_widgets(self):
        return_btn = UIFlatButton(text='<', width=70, height=70, color=arcade.color.BLUE)
        return_btn.on_click = lambda event: self.return_g()
        self.anchor_layout.add(return_btn, align_x=-350, align_y=350)

    def return_g(self):
        menu_view = self.window.view_dict['menu_view']()
        self.window.show_view(menu_view)
        self.manager.disable()
