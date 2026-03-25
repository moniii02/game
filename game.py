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
        
        #player
        self.player = None
        self.player_list = arcade.SpriteList()
        
        #World
        self.wall_list = arcade.SpriteList()

        #Enemies
        self.enemy_list = arcade.SpriteList()
        self.spawn_timer = 0

        #Movements
        self.move_left = False
        self.move_right = False 

        #Game state
        self.score = 0
        self.game_over = False

        #Physics
        self.physics_engine = None

        #camera
        self.camera = arcade.Camera2D()

        #Platform generation
        self.last_platform_x = 200

        self.setup()
        

    def setup(self):
        #player
        self.player = arcade.Sprite("./assets/player.png")
        self.player.center_x = 75
        self.player.center_y = 150

        self.player.scale = 0.3
        self.player_list.append(self.player)

        #ground
        ground = arcade.SpriteSolidColor(5000, 40, arcade.color.DARK_GREEN)
        ground.center_x = 2500
        ground.center_y = 20
        self.wall_list.append(ground)

        #initial platforms
        for _ in range (10):
            self.spawn_platform()

        #physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, gravity_constant=gravity)

    def spawn_platform(self):
        width = random.randint(120, 220)
        x = self.last_platform_x + random.randint(180, 300)
        y = random.randint(120, 300)

        platform = arcade.SpriteSolidColor(width, 20, arcade.color.BROWN)
        platform.center_x = x
        platform.center_y = y

        self.wall_list.append(platform)
        self.last_platform_x = x

    def setup_enemy(self):
        enemy = arcade.Sprite("./assets/enemy.png")
        enemy.scale = 0.2
        enemy.center_x = self.player.center_x + screen_width
        enemy.center_y = 60
        enemy.change_x = -2
        self.enemy_list.append(enemy)

    def center_camera_to_player(self):
        self.camera.position = (self.player.center_x, screen_height / 2)
        
    def on_draw(self):
        self.clear()

        #World
        with self.camera.activate():
            self.wall_list.draw()
            self.player_list.draw ()
            self.enemy_list.draw()
        
        arcade.draw_text(f"score: {int(self.score)}", 10, screen_height - 30, arcade.color.WHITE, 20)

        if self.game_over:
            arcade.draw_text("GAME OVER", screen_width // 2 - 135, screen_height // 2, arcade.color.DARK_RED, 40)
            

    def on_update(self, delta_time):
        if self.game_over:
            return
        
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

        #Generate new platform
        if self.last_platform_x < self.player.center_x + screen_width:
            self.spawn_platform()

        #remove old paltform
        for platform in self.wall_list:
            if platform.width < 4000:
                if platform.right < self.player.center_x - screen_width:
                    platform.remove_from_sprite_lists()

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

        self.center_camera_to_player()


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