import arcade

from menu_view import MenuView

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
TITLE = 'CosmicDash'


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.set_update_rate(1 / 60)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
