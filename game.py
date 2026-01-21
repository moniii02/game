import arcade
import random

screen_width = 800
screen_height = 450
screen_title = "GAME"

#GRAVITY = 1
#JUMP_SPEED = 15
#OBSTACLE_SPEED = 5

class GAME (arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.player = None
        self.lista_player = arcade.SpriteList()
        #self.obstacle = None
        self.score = 0
        #self.game_over = False

        arcade.set_background_color(arcade.color.SKY_BLUE)


    def setup (self):

        self.player = arcade.sprite("./assets/ci metti lo sprite")
        self.player.center_x = 150
        self.player.center_y = 100
        self.player.scale = 1
        self.lista_player.append(self.player)
        
    def on_draw(self):
        arcade.start_render()
        self.lista_player.draw ()
        arcade.draw_text(f"score: {self.score}", 10, screen_height - 30, arcade.color.WHITE, 20)

    #def on_update(self):
        
def main():
    game = GAME()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()