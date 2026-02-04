import arcade
import random

screen_width = 800
screen_height = 450
screen_title = "GAME"

gravity = 3
jump_speed = 15
player_speed = 5
ground_y = 100
#OBSTACLE_SPEED = 5

class GAME (arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.player = None
        self.lista_player = arcade.SpriteList()
        #self.obstacle = None
        self.score = 0
        #self.game_over = False
        self.move_left = False
        self.move_right = False 
        self.move_up = False
        arcade.set_background_color(arcade.color.SKY_BLUE)
        #self.camera = arcade.camera.Camera2D()

        self.setup()
        

    def setup (self):

        self.player = arcade.Sprite("./assets/player.png")
        self.player.center_x = 150
        self.player.center_y = ground_y
        
        self.player.change_x = 0
        self.player.change_y= 0

        self.player.scale = 0.5
        self.lista_player.append(self.player)
        
    def on_draw(self):
        self.clear()
        #self.camera.use()
        self.lista_player.draw ()
        arcade.draw_text(f"score: {self.score}", 10, screen_height - 30, arcade.color.WHITE, 20)

    def on_update(self, delta_time):
        #self.camera.position = self.player.position

        if self.move_left:
            self.player.change_x = -player_speed
        elif self.move_right:
            self.player.change_x = player_speed
        elif self.move_up:
            self.player.change_y = player_speed
        else:
            self.player.change_x = 0
            self.player.change_y = 0

        self.player.center_x += self.player.change_x
        self.player.center_y -= gravity
        self.player.center_y += self.player.change_y

        if self.player.center_y <= ground_y:
           self.player.center_y = ground_y
           self.player.change_y = 0

    def on_key_press(self,key, modifiers):
        if key == arcade.key.A:
            self.move_left = True
        elif key == arcade.key.D:
            self.move_right = True
        elif key == arcade.key.W:
            self.move_up = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.move_left = False
        elif key == arcade.key.D:
            self.move_right = False
        elif key == arcade.key.W:
            self.move_up = False
        
def main():
    gioco = GAME(screen_width, screen_height, "GAME")
    arcade.run()

if __name__ == "__main__":
    main()