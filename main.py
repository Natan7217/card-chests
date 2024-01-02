from menu import MenuApp
from objects import LoadingScreen

if __name__ == '__main__':
    loading_screen = LoadingScreen(asleep=10, titles=['Game loading...'], key_flag=False)
    screen = loading_screen.run()
    app = MenuApp(parent=screen)
    app.run()
