import arcade

from menu_view import MenuView
from game_view import GameView
from pause_view import PauseView

views = {'menu_view': MenuView, 'game_view': GameView, 'pause_view': PauseView}

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
