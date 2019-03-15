from variables import *
from game import Game


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.font = 20
        self.text_color = WHITE
        self.pressed = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
        arcade.draw_text(self.text, self.x - 50, self.y, self.text_color, self.font)


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.button_list = None
        self.p = None
        self.n = None
        self.game = Game(1)
        self.run = None
        self.text = None
        self.font = 60
        self.count = 0

    def on_draw(self):
        arcade.start_render()
        if not self.game.connected():
            text = "Waiting for Player"
            arcade.draw_text(text, WIDTH/2 - 300, HEIGHT/2, BLACK, 60)
        else:
            head1 = "Your Move"
            arcade.draw_text(head1, 100, 700, BLACK, 60)
            head2 = "Opponent Move"
            arcade.draw_text(head2, 400, 700, BLACK, 60)
            move1 = self.game.get_player_move(0)
            move2 = self.game.get_player_move(1)
            if self.game.bothWent():
                text1 = move1
                text2 = move2
            else:
                if self.game.p1went and self.p == 0:
                    text1 = move1
                elif self.game.p1went:
                    text1 = "Locked in"
                else:
                    text1 = "waiting"
                if self.game.p2went and self.p == 1:
                    text2 = move2
                elif self.game.p2went:
                    text2 = "Locked in"
                else:
                    text2 = "waiting"

                if self.p == 1:
                    arcade.draw_text(text2, 130, 300, BLACK, 40)
                    arcade.draw_text(text1, 530, 300, BLACK, 40)
                else:
                    arcade.draw_text(text1, 130, 300, BLACK, 40)
                    arcade.draw_text(text2, 530, 300, BLACK, 40)

            for button in self.button_list:
                button.draw()
            if self.text:
                arcade.draw_text(self.text, WIDTH/2 - 150, HEIGHT/2 + 200, RED, self.font)
                self.count += 1
                if self.count >= 120:
                    self.text = "New Game"
                    self.count = 0

    def setup(self):
        arcade.set_background_color(BLUE)
        self.n = Network()
        self.p = int(self.n.getP())
        self.game = self.n.send('get')
        print("you are player: ", self.p)

        self.run = True
        self.button_list = [Button('ROCK', 200, 150, RED),
                            Button('PAPER', 400, 150, ORANGE),
                            Button('SCISSORS', 600, 150, GREEN)]

    def update(self, delta_time):
        if self.run:
            try:
                self.game = self.n.send('get')
            except:
                self.run = False
                print("couldn't get game")
                return
            if self.game.bothWent():
                time.sleep(0.5)
                try:
                    self.game = self.n.send("reset")
                except:
                    run = False
                    print("couldn't get game")
                    return

                if (self.game.winner() == 1 and self.p == 1) or (self.game.winner() == 0 and self.p == 0):
                    self.text = "You Won!"
                elif self.game.winner() == -1:
                    self.text = "Draw!"
                else:
                    self.text = "You Lost!"
                self.run = True


    def check_mouse_press_for_buttons(self, x, y, button_list):
        for button in button_list:
            if x > button.x + button.width / 2:
                continue
            if x < button.x - button.width / 2:
                continue
            if y > button.y + button.height / 2:
                continue
            if y < button.y - button.height / 2:
                continue
            self.n.send(button.text)

    def check_mouse_release_for_buttons(self, x, y, button_list):
        for button in button_list:
            if button.pressed:
                button.on_release()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.game.connected():
            if self.p == 0:
                if not self.game.p1went:
                    self.check_mouse_press_for_buttons(x, y, self.button_list)
            else:
                if not self.game.p2went:
                    self.check_mouse_press_for_buttons(x, y, self.button_list)


    def on_key_press(self, key, mods):
        if key == ESC:
            self.run = False
            self.close()

    def on_key_release(self, key, mods):
        pass


def main():
    window = Window(WIDTH, HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
