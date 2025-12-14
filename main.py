import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Star Wars"
LASER_SPEED = 5
ENEMIES_SPEED = 1
ENEMIES_DISTANCE = 50


class Meteor(arcade.Sprite):
    def __init__(self):
        super().__init__('meteorit.png', 0.5)
        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT * 3)
        self.change_y = ENEMIES_SPEED + LASER_SPEED

    def update(self):
        self.center_y -= self.change_y
        if self.top < 0:
            self.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT * 3)
            self.center_x = random.randint(0, SCREEN_WIDTH)

class TieFighter(arcade.Sprite):
    def __init__(self):
        super().__init__('TieFighter.png', 0.2)
        self.angle = 90
        self.change_y = ENEMIES_SPEED

    def update(self):
        self.center_y -= self.change_y
        if self.top < 0:
            self.kill()


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
        self.enemies = arcade.SpriteList()
        self.game = True
        self.win_sound = arcade.load_sound('A New Hope.mp3')
        self.victory = arcade.load_texture('victory.jpg')
        self.meteor = Meteor()

    def setup(self):
        for i in range(50):
            tie_fighter = TieFighter()
            tie_fighter.center_x = random.randint(0, SCREEN_WIDTH)
            tie_fighter.center_y = SCREEN_HEIGHT + i * ENEMIES_DISTANCE
            self.enemies.append(tie_fighter)

    def on_draw(self):
        self.clear((255, 255, 255))
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.falcon.draw()
        self.lasers.draw()
        self.enemies.draw()
        self.meteor.draw()
        if len(self.enemies) == 0:
            self.game = False
            arcade.play_sound(self.win_sound, 0.2)
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.victory)


    def update(self, delta_time: float):
        if self.game == True:
            self.falcon.update()
            self.lasers.update()
            self.enemies.update()
            self.meteor.update()

            for laser in self.lasers:
                hit_list = arcade.check_for_collision_with_list(laser, self.enemies)
                if hit_list:
                    laser.kill()
                    for enemy in hit_list:
                        enemy.kill()

            if arcade.check_for_collision(self.meteor, self.falcon):
                self.game = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.game == True:
            if 0 + self.falcon.width / 2 < x < SCREEN_WIDTH - self.falcon.width / 2:
                self.falcon.center_x = x

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.game == True:
            if button == arcade.MOUSE_BUTTON_LEFT:
                laser = Laser()
                arcade.play_sound(laser.laser_sound, 0.5)
                self.lasers.append(laser)


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()

arcade.run()
