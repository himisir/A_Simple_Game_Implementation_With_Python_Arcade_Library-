import arcade

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MOVEMENT_SPEED = 10


class Ball:

    def __init__(self, position_x, position_y, change_x, change_y, radius, color):

        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color
        self.flag = False

    def draw(self):
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def update(self):

        self.position_y += self.change_y
        self.position_x += self.change_x

        if self.position_x < self.radius:
            self.change_x *= -1
        if self.position_x > SCREEN_WIDTH - self.radius:
            self.change_x *= -1
        if self.position_y > SCREEN_HEIGHT - self.radius:
            self.change_y *= -1

        if self.flag:
            if self.position_y < self.radius + 20:
                self.change_y *= -1
            self.flag = False


class Rect:
    def __init__(self, position_x, position_y, rect_width, rect_height, change_x, color):
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x

        self.rect_height = rect_height
        self.rect_width = rect_width
        self.color = color

    def draw(self):
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.rect_width, self.rect_height, self.color)

    def update(self):
        print(self.position_x, " ", self.rect_width / 2, " ", self.change_x)

        # Left and Right Range of Rect:

        if SCREEN_WIDTH - self.rect_width / 2 >= self.position_x + self.change_x >= self.rect_width / 2:
            self.position_x += self.change_x


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.set_background_color(arcade.color.WHITE)
        # arcade.set_viewport(0, SCREEN_WIDTH-1, 0, SCREEN_HEIGHT -1)
        self.game_view = GameView()
        print(" Score: ", self.window.total_score)

    def on_draw(self):
        arcade.start_render()
        output = f"Score: {self.window.total_score}"
        arcade.draw_text(output, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2, arcade.color.RED, 30)

    def on_mouse_press(self, x, y, button, modifiers):
        self.game_view.setup()
        self.window.show_view(self.game_view)


class GameView(arcade.View):
    def __init__(self):
        # call super
        super().__init__()

        self.score = 0

        # sounds
        self.move_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.score_sound = arcade.load_sound(":resources:sounds/phaseJump1.ogg")

        # set background
        arcade.set_background_color(arcade.color.ASH_GREY)

        # create a rect
        self.rect = Rect(SCREEN_WIDTH / 2, 0, 80, 20, 0, arcade.color.BLACK)

        # create a ball

        self.ball = Ball(50, 50, 3, 3, 15, arcade.color.BABY_BLUE_EYES)

        # Game initializing

    def setup(self):
        self.window.total_score = 0
        self.score = 0
        self.rect = Rect(SCREEN_WIDTH / 2, 0, 80, 20, 0, arcade.color.BLACK)
        self.ball = Ball(50, 50, 3, 3, 15, arcade.color.BABY_BLUE_EYES)

    def on_draw(self):
        arcade.start_render()
        self.rect.draw()
        self.ball.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time, ):
        self.ball.update()

        if abs(self.ball.position_x - self.rect.position_x) < 40:

            if self.ball.position_y == self.ball.radius + self.rect.rect_height:
                self.score += 1
                self.ball.flag = True
                self.window.total_score += 1
                arcade.play_sound(self.score_sound)

        if self.ball.position_y < self.ball.radius:
            arcade.play_sound(self.game_over_sound)
            view = GameOverView()
            self.window.show_view(view)
        self.rect.update()

    def on_key_press(self, key, modifiers):
        arcade.play_sound(self.move_sound)
        if key == arcade.key.LEFT:
            self.rect.change_x -= MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.rect.change_x += MOVEMENT_SPEED
        else:
            self.rect.change_x = 0
            self.rect.change_y = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.rect.change_x = 0
            self.rect.change_y = 0
        else:
            self.rect.change_x = 0
            self.rect.change_y = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Bounce")
    window.total_score = 0
    start_view = GameView()
    window.show_view(start_view)
    arcade.run()


main()
