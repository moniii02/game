import arcade
import random
from sprite_animato import SpriteAnimato

screen_width = 900
screen_height = 450
screen_title = "GAME"

gravity = 1 
jump_speed = 18
player_speed = 6

class Player(SpriteAnimato):
    def __init__(self):
        super().__init__(scala = 2.0)
        file_animazione = {
            "destra": "./assets/run_player.png",
            "sinistra": "./assets/run_player.png"
        }

        for dir, percorso in file_animazione.items():
            self.aggiungi_animazione(
                nome = f"run_{dir}",
                percorso = percorso,
                frame_width = 48,
                frame_height = 64,
                num_frame = 8,
                colonne = 8,
                durata = 1,
                riga = 0
            )

        self.direzione = "destra"


    def update_animation(self, delta_time):
        if self.change_x > 0:
            self.direzione = "destra"
        elif self.change_x < 0:
            self.direzione = "sinistra"

        self.imposta_animazione(f"run_{self.direzione}")

        super().update_animation(delta_time)
        
class Enemy(SpriteAnimato):
    def __init__(self):
        super().__init__(scala = 1.5)
        file_animazione = {
            "destra": "./assets/run_slime.png",
            "sinistra": "./assets/run_slime.png"
        }

        for dir, percorso in file_animazione.items():
            self.aggiungi_animazione(
                nome = f"run_{dir}",
                percorso = percorso,
                frame_width = 31.5,
                frame_height = 25,
                num_frame = 8,
                colonne = 8,
                durata = 1,
                riga = 0
            )

        self.direzione = "destra"

        self.boundary_left = None
        self.boundary_right = None


    def update_animation(self, delta_time):
        if self.change_x > 0:
            self.direzione = "destra"
        elif self.change_x < 0:
            self.direzione = "sinistra"

        self.imposta_animazione(f"run_{self.direzione}")

        super().update_animation(delta_time)

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

        #coins
        self.coin_score = 0
        self.coin_list = arcade.SpriteList()

        self.setup()
        

    def setup(self):
        #player
        self.player = Player()
        self.player.center_x = 75
        self.player.center_y = 150  
        self.player_list.append(self.player)

        #ground
        ground = arcade.SpriteSolidColor(60000, 40)
        ground.center_x = 2500
        ground.center_y = 20
        ground.color = arcade.color.DARK_GREEN
        self.wall_list.append(ground)

        #first platfrom manually
        platform = arcade.SpriteSolidColor(135, 20, arcade.color.BROWN)
        platform.center_x = 115
        platform.center_y = 155
        platform.color = arcade.color.BROWN
        self.wall_list.append(platform)

        #initial platforms
        for _ in range (10):
            self.spawn_platform()

        #player on platform
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, gravity_constant=gravity)

    def spawn_platform(self):
        width = random.randint(120, 220)
        x = self.last_platform_x + random.randint(180, 300)
        y = random.randint(120, 300)

        platform = arcade.SpriteSolidColor(width, 20, arcade.color.BROWN)
        platform.center_x = x
        platform.center_y = y
        self.last_platform_x = x
        platform.color = arcade.color.BROWN
        self.wall_list.append(platform)

        #coins
        if random.random() < 0.5:
            coin = arcade.Sprite("./assets/coin.png", scale= 0.15)
            coin.center_x = x + random.randint(-60, 60)
            coin.bottom = y + random.randint(40, 120)
            self.coin_list.append(coin)

    def setup_enemy(self):
        enemy = Enemy()
        platform = random.choice(self.wall_list)
        enemy.center_x = platform.center_x 
        enemy.bottom = platform.top
        enemy.boundary_left = platform.left
        enemy.boundary_right = platform.right
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
            self.coin_list.draw()
        
        arcade.draw_text(f"score: {int(self.score)}", 10, screen_height - 30, arcade.color.WHITE, 20)

        if self.game_over:
            arcade.draw_text("GAME OVER", screen_width // 2 - 135, screen_height // 2, arcade.color.DARK_RED, 40)
            

    def on_update(self, delta_time):
        if self.game_over:
            return
        
        self.enemy_list.update_animation()
        self.player_list.update_animation()
        
        #score increases over time 
        self.score = self.player.center_x / 30 + self.coin_score

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
            if platform.right < self.player.center_x - screen_width:
                platform.remove_from_sprite_lists()

        #spawn enemies 
        self.spawn_timer += delta_time
        if self.spawn_timer > 3 and  len(self.enemy_list) < 3:
            self.setup_enemy()
            self.spawn_timer = 0
        
        #update enemies
        for enemy in self.enemy_list:
            if enemy.left < enemy.boundary_left:
                enemy.left = enemy.boundary_left
                enemy.change_x *= -1
            elif enemy.right > enemy.boundary_right:
                enemy.right = enemy.boundary_right
                enemy.change_x *= -1

            #remove off-screen enemies
            if enemy.right < 0:
                enemy.remove_from_sprite_lists()

            #collision
            if arcade.check_for_collision(self.player, enemy):
                self.game_over = True

        #Coin collection
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.coin_score += 20

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