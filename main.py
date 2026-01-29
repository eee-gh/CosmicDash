import arcade

from views.menu_view import MenuView
from views.game_view import GameView
from views.pause_view import PauseView
from views.end_view import EndView

views = {'menu_view': MenuView, 'game_view': GameView, 'pause_view': PauseView, 'end_view': EndView}

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
TITLE = 'CosmicDash'


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.view_dict = views
    window.set_update_rate(1 / 60)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
