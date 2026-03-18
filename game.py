import arcade
import random

screen_width = 900
screen_height = 450
screen_title = "GAME"

gravity = 1 
jump_speed = 18
player_speed = 6


class GAME (arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.SKY_BLUE)
        
        self.player = None
        self.player_list = arcade.SpriteList()
        
        self.wall_list = arcade.SpriteList()

        self.enemy_list = arcade.SpriteList()
        self.spawn_timer = 0

        self.move_left = False
        self.move_right = False 

        self.score = 0
        self.game_over = False
        self.physics_engine = None
        
        self.setup()
        

    def setup(self):
        #player
        self.player = arcade.Sprite("./assets/player.png")
        self.player.center_x = 75
        self.player.center_y = 150

        self.player.scale = 0.3
        self.player_list.append(self.player)

        #ground
        ground = arcade.SpriteSolidColor(screen_width, 40, arcade.color.DARK_GREEN)
        ground.center_x = screen_width // 2
        ground.center_y = 20
        self.wall_list.append(ground)

        #platforms
        platform_positions = [(300, 150), (500, 220), (700, 150)]
        for x, y in platform_positions:
            platform = arcade.SpriteSolidColor(200, 20, arcade.color.BROWN)
            platform.center_x = x
            platform.center_y = y
            self.wall_list.append(platform)

        #physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, gravity_constant=gravity)

    def setup_enemy(self):
        enemy = arcade.Sprite("./assets/enemy.png")
        enemy.scale = 0.20
        enemy.center_x = screen_width + 50
        enemy.center_y = 60
        enemy.change_x = -2
        self.enemy_list.append(enemy)

        
    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.player_list.draw ()
        self.enemy_list.draw()
        
        arcade.draw_text(f"score: {int(self.score)}", 10, screen_height - 30, arcade.color.WHITE, 20)

        if self.game_over:
            arcade.draw_text("GAME OVER", screen_width // 2 - 135, screen_height // 2, arcade.color.DARK_RED, 40)
            

    def on_update(self, delta_time):
        if self.game_over:
            return

        screen_center_x = self.player.center_x - (screen_width / 2)
        
        if screen_center_x < 0:
            screen_center_x = 0


    #score increases over time 
        self.score += delta_time * 10

     #player movements
        if self.move_left:
            self.player.change_x = -player_speed
        elif self.move_right:
            self.player.change_x = player_speed
        else:
            self.player.change_x = 0
    
        self.physics_engine.update()

    #spawns enemies every 2 seconds
        self.spawn_timer += delta_time
        if self.spawn_timer > 3.5 and  len(self.enemy_list) < 2:
            self.setup_enemy()
            self.spawn_timer = 0
        
    #update enemies
        for enemy in self.enemy_list:
            enemy.center_x += enemy.change_x

            #remove off-screen enemies
            if enemy.right < 0:
                enemy.remove_from_sprite_lists()

            #collision
            if arcade.check_for_collision(self.player, enemy):
                self.game_over = True

    def on_key_press(self,key, modifiers):
        if key == arcade.key.A:
            self.move_left = True
        elif key == arcade.key.D:
            self.move_right = True
        elif key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = jump_speed

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