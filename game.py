import arcade
import random

screen_width = 900
screen_height = 450
screen_title = "GAME"

gravity = 3 #pulls player down
jump_speed = 50
player_speed = 6
ground_y = 100 #an imaginary line to stop the player from falling

class GAME (arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.player = None
        self.lista_player = arcade.SpriteList()
        self.score = 0
        self.move_left = False
        self.move_right = False 
        self.on_ground = False
        self.enemy = None
        self.enemy_list = arcade.SpriteList()
        self.game_over = False
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.setup()
        

    def setup(self):

        self.player = arcade.Sprite("./assets/player.png")
        self.player.center_x = 75
        self.player.center_y = ground_y
        
        self.player.change_x = 0
        self.player.change_y= 0

        self.player.scale = 0.3
        self.lista_player.append(self.player)

    
    def setup_enemy(self):
        self.enemy = arcade.Sprite("./assets/enemy.png")
        self.enemy.scale = 0.20
        self.enemy.center_x = screen_width + 50
        self.enemy.center_y = ground_y 
        self.enemy.change_x = -4
        self.enemy.change_y = 0
        self.enemy_list.append(self.enemy)

        
    def on_draw(self):
        self.clear()
        self.lista_player.draw ()
        if self.enemy:
            self.enemy_list.draw()
        
        arcade.draw_text(f"score: {int(self.score)}", 10, screen_height - 30, arcade.color.WHITE, 20)

        if self.game_over:
            arcade.draw_text("GAME OVER", screen_width // 2 - 135, screen_height // 2, arcade.color.DARK_RED, 40)
            


    def on_update(self, delta_time):
        if self.game_over:
            return
        
        self.score += abs(self.player.change_x) * delta_time * 10 # abs = removes the negative numbers
     
     #player movements
        if self.move_left:
            self.player.change_x = -player_speed
        elif self.move_right:
            self.player.change_x = player_speed
        else:
            self.player.change_x = 0
    
        self.player.center_x += self.player.change_
        self.player.change_y -= gravity
        self.player.center_y += self.player.change_y
        
    #stops player from falling below ground
        if self.player.center_y <= ground_y:
           self.player.center_y = ground_y
           self.player.change_y = 0
           self.on_ground = True

    #creates enemy if it doesn't exist
        if self.enemy is None:
            self.setup_enemy()

        if self.enemy:
            self.enemy.center_x += self.enemy.change_x

    #if enemy gets out of frame then remove it
        if self.enemy.right <0:
                self.enemy_list.remove(self.enemy)
                self.enemy = None
       
        if self.enemy and arcade.check_for_collision(self.player, self.enemy):
            self.game_over = True 
            print("GAME OVER")

    def on_key_press(self,key, modifiers):
        if key == arcade.key.A:
            self.move_left = True
        elif key == arcade.key.D:
            self.move_right = True
        elif key == arcade.key.W and self.on_ground:
            self.player.change_y = jump_speed
            self.on_ground = False

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.move_left = False
        elif key == arcade.key.D:
            self.move_right = False
        
        
def main():
    gioco = GAME(screen_width, screen_height, "GAME")
    arcade.run()

if __name__ == "__main__":
    main()