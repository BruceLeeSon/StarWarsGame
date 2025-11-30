import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Star Wars"
LASER_SPEED = 5


class Laser(arcade.Sprite):
    def __init__(self):
        super().__init__('laser.png', 0.8)
        self.center_x = window.falcon.center_x
        self.bottom = window.falcon.top
        self.change_y = LASER_SPEED
        self.laser_sound = arcade.load_sound('laser.wav')


    def update(self):
        self.center_y += self.change_y


class Falcon(arcade.Sprite):
    def __init__(self):
        super().__init__('falcon.png', 0.3)
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 100

    def update(self):
        self.center_x += self.change_x


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        self.bg = arcade.load_texture('background.jpg')
        self.falcon = Falcon()
        self.lasers = arcade.SpriteList()

    def setup(self):
        pass

    def on_draw(self):
        self.clear((255, 255, 255))
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.falcon.draw()
        self.lasers.draw()

    def update(self, delta_time: float):
        self.falcon.update()
        self.lasers.update()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.falcon.center_x = x

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            laser = Laser()
            arcade.play_sound(laser.laser_sound, 0.5)
            self.lasers.append(laser)


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()

arcade.run()
