
from import_mod_const import *
import modules
import copy


SCREEN_TITLE = "SpaceShip1"
SPRITE_SCALING = 3
UPDATE_RATEHz = 1/90.1

ENEMY_COUNT = 0
BALL_COUNT = 1
BALL_RADIOS = 20
BALL_MOV = 300

GUN_FIRE_RATE = 1/15

GRAVITY = 0#700

PARTICLE_COUNT = 20

MOVEMENT_FORCE = 600

BALL_COLORS = [arcade.color.RED_BROWN,
               arcade.color.NAVY_BLUE,
               arcade.color.OLD_ROSE,
               arcade.color.PURPLE_HEART,
               arcade.color.DARK_YELLOW]

METEOR_SPRITE_SIZES = [ [],
                        [48,48],
                        [32,48],
                        [24,32],
                        [16,16],
                        [8,15],
                        [8,8] ]    

class Ball(arcade.SpriteCircle):
    """Create a Ball object"""
    def __init__(self,radius: int,color,soft:bool = False,density:int = 1/40):
        super().__init__(radius=radius,color=color,soft=soft)
        self.mass = density*math.pi*4/3*(radius/10)**2 #density*math.pi*4/3*(radius/10)**3
        self.radius = radius
        self.health = self.radius*20

    def update(self):
        pass

    def on_update(self, delta_time: float = 1/60):
        self.position = [self._position[0] + self.change_x*delta_time, self._position[1] + self.change_y*delta_time]
        self.angle += self.change_angle*delta_time

class Rigid(arcade.Sprite):
    def __init__(self,
                 filename: str = None,
                 scale: float = 1,
                 image_x: float = 0, image_y: float = 0,
                 image_width: float = 0, image_height: float = 0,
                 center_x: float = 0, center_y: float = 0,
                 _repeat_count_x=1, _repeat_count_y=1, radius: int = 55,mass: int = 0.2):

        super().__init__(filename=filename, scale=scale, image_x=image_x, image_y=image_y,
                         image_width=image_width, image_height=image_height,
                         center_x=center_x, center_y=center_y)
        
        self.mass = mass
        self.radius = radius
        self.speed_scalar: int = 0
        self.health = 500

    def update(self):
        pass

    def on_update(self, delta_time: float = 1/60):
        self.position = [self._position[0] + self.change_x*delta_time, self._position[1] + self.change_y*delta_time]
        self.angle += self.change_angle*delta_time
        self.speed_scalar = math.sqrt(self.change_x*self.change_x + self.change_y*self.change_y)

class Bullet(Rigid):
    def __init__(self,
                 filename: str = None,
                 scale: float = 1,
                 image_x: float = 0, image_y: float = 0,
                 image_width: float = 0, image_height: float = 0,
                 center_x: float = 0, center_y: float = 0,
                 _repeat_count_x=1, _repeat_count_y=1, radius: int = 5,mass: int = 0.002):

        super().__init__(filename=filename, scale=scale, image_x=image_x, image_y=image_y,
                         image_width=image_width, image_height=image_height,
                         center_x=center_x, center_y=center_y)
        
        self.health = 10

class MyGame(arcade.View):
    """Need to be named MyGame to other classes work proporly, Game Class"""
    def __init__(self):
        """
        Initializer
        """
        # Call the parent class initializer
        super().__init__()

        #Screen update rate    
        self.update_rate = UPDATE_RATEHz

        # Player 
        self.player = None
        self.player_score = None
        self.player_list = None
        self.bullet_list = None
        self.bullet_s = None
        self.trigger_press = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.x_ini = 100

        # Enemy
        self.enemy_walking_tex_list = [None,None]
        self.enemy_walking_tex_list[0] =  modules.AnimatedTime()
        self.enemy_walking_tex_list[1] =  modules.AnimatedTime()

        self.enemy_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.objt_list = arcade.SpriteList()

        # Background
        self.background = arcade.Sprite()

        # Floor
        self.floor = None

        self.current_time = None
        self.delta_time = None
        self.mouse_x = None
        self.mouse_y = None

    def setup(self):
        """Set up initial assets"""

        self.current_time = 0.0
        self.delta_time = 0.0

        self.bullet_list = arcade.SpriteList()
        self.trigger_press = False
        self.bullet_s = 1
        self.fire_time = 0.0
        """Player set up"""
        self.player = Rigid()
        tex : arcade.Texture = arcade.load_texture(PATH / "images/ikaruga-sprite2.png", x = 0, y = 0, width = 282 ,height = 290)

        #self.player.alpha = 0
        self.player.center_x = SCREEN_WIDTH/2
        self.player.center_y = SCREEN_HEIGHT/2                                             
        self.player.texture = tex 
        #self.player.hit_box = arcade.calculate_hit_box_points_detailed(tex.image,30) 
        hitbox: arcade.Texture = arcade.make_circle_texture(self.player.radius * 2, arcade.color.BLACK)
        self.player.hit_box = hitbox.hit_box_points  
        #print(self.player.hit_box)
        self.player.scale = 1/2
        self.player.health = 10000
        self.objt_list.append(self.player)

        """Create Enemies"""
        for i in range(ENEMY_COUNT):
            self.create_enemy(self.enemy_list,self.get_enemy_sprites())
            
        """Create Floor"""
        #self.floor = arcade.SpriteSolidColor(SCREEN_WIDTH,SCREEN_HEIGHT//4,arcade.color.GRAY)
        #self.floor.center_x = SCREEN_WIDTH//2
        #self.floor.center_y = SCREEN_HEIGHT//8

        """Create Ball"""
        for ball in range(BALL_COUNT):
            color = random.choice(BALL_COLORS)
            ball = Ball(BALL_RADIOS,color, False)
            ball.center_x = SCREEN_WIDTH//2 + random.randrange(-4,5)*100
            ball.center_y = SCREEN_HEIGHT//1.5
            #ball.change_x = random.randrange(-4,5)*100
            #ball.change_y = random.randrange(-4,5)*100
            ball.health = 5000
            self.ball_list.append(ball)
            self.objt_list.append(ball) 
        


        # Background image
        self.background.texture = arcade.load_texture(PATH / "images/snes-contra-3-BackGround.png")
        self.background.scale = 3
        self.background.center_x = SCREEN_WIDTH//2 +1600 #-self.x_ini
        self.background.center_y = SCREEN_HEIGHT//2
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def get_enemy_sprites(self):

        d = 1/15
        f = (1/15)/(self.update_rate)/2
    
        enemy_walking_textures = [[],[]]
        enemy_walking_textures[0] =  modules.AnimatedTime()#Pode usar AnimatedTime no lugar 
        enemy_walking_textures[1] =  modules.AnimatedTime()
        for i in range(0,7):
            texE0 : arcade.Texture = arcade.load_texture(PATH / "Mecha-RunC.png", 
                                                         x=i*64,y=0,width=64,height=64)
            texE1 : arcade.Texture = arcade.load_texture(PATH / "Mecha-RunC.png", 
                                                         x=i*64,y=0,width=64,height=64,flipped_horizontally=True)                                                                                                
            enemy_walking_textures[1].frames.append(arcade.AnimationKeyframe(i, f*d*1000, texE1))
            enemy_walking_textures[0].frames.append(arcade.AnimationKeyframe(i, f*d*1000, texE0))

        self.enemy_walking_tex_list = enemy_walking_textures

        return enemy_walking_textures

    def create_enemy(self,enemy_list,enemy_walking_textures):
        """Create a enemy in a randow position, enemy has a animation, put on a list"""
        enemy =  modules.AnimatedTime_Enemy()

        enemy.center_x = random.randrange(100,SCREEN_WIDTH + 1000)
        enemy.center_y = random.randrange(50,SCREEN_HEIGHT//3 - 80)

        enemy.change_x = random.randrange(-1, 2,2) * MOVEMENT_FORCE * self.update_rate * 1.2
        #enemy.change_y = random.randrange(-10, 11)/10 * MOVEMENT_FORCE * self.update_rate
        enemy.change_y = 0

        # Getting first frame that will show on Screen
        randid = random.randrange(0,6)
        if enemy.change_x > 0:
            enemy.frames = enemy_walking_textures[1].frames
            enemy.texture = enemy.frames[randid].texture
        else:
            enemy.frames = enemy_walking_textures[0].frames  
            enemy.texture = enemy.frames[randid].texture 

        enemy.cur_frame_idx = randid
        enemy.scale = 2
        # Add the Enemy to the lists
        enemy_list.append(enemy)    

    def move_player(self,delta_time):
        # Move player not depending on Screen Frame Rate

        #Player Aceleration
        if self.up_pressed and not self.down_pressed and self.player.change_y < 500:
            self.player.change_y += 2*MOVEMENT_FORCE * delta_time
            
        elif self.down_pressed and not self.up_pressed and self.player.change_y > -500:
            self.player.change_y += -2*MOVEMENT_FORCE * delta_time
            
        if self.left_pressed and not self.right_pressed and self.player.change_x > -500:
            self.player.change_x += -2*MOVEMENT_FORCE * delta_time
            
        elif self.right_pressed and not self.left_pressed and self.player.change_x < 500:
            self.player.change_x += 2*MOVEMENT_FORCE * delta_time
            
        #Player Desaceleration
        #print(self.player.speed_scalar)
        if self.player.speed_scalar >5 and self.player.speed_scalar < 1050:
            if not self.up_pressed and self.player.change_y > 0:
                self.player.change_y += -2*MOVEMENT_FORCE * delta_time
            
            elif not self.down_pressed and self.player.change_y <0:
                self.player.change_y += 2*MOVEMENT_FORCE * delta_time
            
            if not self.left_pressed and self.player.change_x < 0:
                self.player.change_x += 2*MOVEMENT_FORCE * delta_time
            
            elif not self.right_pressed and self.player.change_x > 0:
                self.player.change_x += -2*MOVEMENT_FORCE * delta_time       

    def physics_objt(self,objt_list,dtime):
        """Ball physics"""
        
        for objt in objt_list:
            objt.change_y -= GRAVITY*dtime #pensar se colocar int(GRAVITY*dtime)
            #print(ball.change_y)

    def colision_ball_floor(self,ball_list,floor):
        """Colision with a Floor Sprite"""
        ball_hit_list = arcade.check_for_collision_with_list(floor, ball_list)

        for ball in ball_hit_list:
            ball.change_y = + abs(ball.change_y)
            ball.center_y = ball.radius + SCREEN_HEIGHT//4

        if len(ball_hit_list) > 0:    
            return True

    def colision_wall(self,objt_list):
        for ball in objt_list:
            if ball.center_x <= BALL_RADIOS:
                ball.center_x = BALL_RADIOS
                ball.change_x *= -1

            if ball.center_y <= BALL_RADIOS:
                ball.center_y = BALL_RADIOS
                ball.change_y *= -1

            if ball.center_x >= SCREEN_WIDTH - BALL_RADIOS:
                ball.center_x = SCREEN_WIDTH - BALL_RADIOS
                ball.change_x *= -1

            if ball.center_y >= SCREEN_HEIGHT - BALL_RADIOS:
                ball.center_y = SCREEN_HEIGHT - BALL_RADIOS
                ball.change_y *= -1

    def colision_player_ball(self,ball1,ball_list):
        if not ball1 == None:
            ball_hit_list = arcade.check_for_collision_with_list(ball1,ball_list)
            for ball2 in ball_hit_list:
                dif_y = ball2.center_y - ball1.center_y
                dif_x = ball2.center_x - ball1.center_x
                dist = math.sqrt(dif_y*dif_y + dif_x*dif_x) 
                mangle = math.atan2(dif_y, dif_x)
                               
                #Conservação de momento
                    
                sin =math.sin(mangle)
                cos= math.cos(mangle)
                #vli velocidade na linha de choque
                vl1 = ball1.change_x*cos + ball1.change_y*sin
                vl2 = ball2.change_x*cos + ball2.change_y*sin
                #vpi velocidade perpendicualr da linha de choque
                vp1 = - ball1.change_x*sin + ball1.change_y*cos
                vp2 = - ball2.change_x*sin + ball2.change_y*cos
                #print(ball1.change_y,ball2.change_y)
                     
                ball1.change_x =  (ball2.mass*vl2*cos - ball1.mass*vp1*sin) / ball1.mass
                ball1.change_y =  (ball2.mass*vl2*sin + ball1.mass*vp1*cos) / ball1.mass

                ball2.change_x =  (ball1.mass*vl1*cos - ball2.mass*vp2*sin) / ball2.mass
                ball2.change_y =  (ball1.mass*vl1*sin + ball2.mass*vp2*cos) / ball2.mass

                p_radius = self.player.radius*self.player.scale
                dis_r = ball2.radius + p_radius-dist
                if dis_r > 0:
                    a = 2
                    ball1.center_x -= (dis_r/2 + a)*cos
                    ball1.center_y -=(dis_r/2 + a)*sin

                    ball2.center_x += (dis_r/2 + a)*cos
                    ball2.center_y += (dis_r/2 + a)*sin

    
        for bullet in bullet_list:
            ball_hit_list = arcade.check_for_collision_with_list(bullet,ball_list)
            for ball in ball_hit_list:
                dif_y = ball.center_y - bullet.center_y
                dif_x = ball.center_x - bullet.center_x
                dist = math.sqrt(dif_y*dif_y + dif_x*dif_x) 
                mangle = math.atan2(dif_y, dif_x)

                # Conservação de momento                    
                sin =math.sin(mangle)
                cos= math.cos(mangle)
                #vli velocidade na linha de choque
                vl1 = bullet.change_x*cos + bullet.change_y*sin
                vl2 = ball.change_x*cos + ball.change_y*sin
                #vpi velocidade perpendicualr da linha de choque
                vp1 = - bullet.change_x*sin + bullet.change_y*cos
                vp2 = - ball.change_x*sin + ball.change_y*cos

                bchange_x =  (ball.mass*vl2*cos - bullet.mass*vp1*sin) / bullet.mass
                bchange_y =  (ball.mass*vl2*sin + bullet.mass*vp1*cos) / bullet.mass

                ball.change_x =  (bullet.mass*vl1*cos - ball.mass*vp2*sin) / ball.mass
                ball.change_y =  (bullet.mass*vl1*sin + ball.mass*vp2*cos) / ball.mass

                dis_r = bullet.radius*bullet.scale + ball.radius*ball.scale - dist
                if dis_r > 0:
                    a = 30
                    bullet.center_x -= (dis_r/2 + a)*cos
                    bullet.center_y -=(dis_r/2 + a)*sin

                    ball.center_x += (dis_r/2 + a)*cos
                    ball.center_y += (dis_r/2 + a)*sin

                # Mudar direção da bala
                bullet.radians +=math.atan2(bchange_y, bchange_x)
                bcx = bullet.change_x
                bcy = bullet.change_y
                bullet.change_x = bcx*math.cos(bullet.radians) - bcy*math.sin(bullet.radians)
                bullet.change_y = bcx*math.sin(bullet.radians) + bcy*math.cos(bullet.radians)
          
    def colision_list_list(self,ball1_list,ball2_list):
        for ball1 in ball1_list:
            ball_hit_list = arcade.check_for_collision_with_list(ball1,ball2_list)
            for ball2 in ball_hit_list:
                #print("hit"," - ", ball1.mass, ball2.mass)
                dif_y = ball2.center_y - ball1.center_y
                dif_x = ball2.center_x - ball1.center_x
                dist = math.sqrt(dif_y*dif_y + dif_x*dif_x) 
                mangle = math.atan2(dif_y, dif_x)
                
                # Conservação de momento                    
                sin =math.sin(mangle)
                cos= math.cos(mangle)
                #vli velocidade na linha de choque
                vl1 = ball1.change_x*cos + ball1.change_y*sin
                vl2 = ball2.change_x*cos + ball2.change_y*sin
                #vpi velocidade perpendicualr da linha de choque
                vp1 = - ball1.change_x*sin + ball1.change_y*cos
                vp2 = - ball2.change_x*sin + ball2.change_y*cos
                #print(ball1.change_y,ball2.change_y)
                v1 = ((ball1.mass - ball2.mass)*vl1 + 2*ball2.mass*vl2)/(ball1.mass + ball2.mass)
                v2 = ((ball2.mass - ball1.mass)*vl2 + 2*ball1.mass*vl1)/(ball1.mass + ball2.mass)

                ball1.change_x =  v1*cos - vp1*sin
                ball1.change_y =  v1*sin + vp1*cos

                ball2.change_x =  v2*cos - vp2*sin
                ball2.change_y =  v2*sin + vp2*cos

                dis_r = ball1.radius*ball1.scale + ball2.radius*ball2.scale - dist
                if dis_r > 0:
                    a = 3
                    if ball1.mass >= ball2.mass:
                        ball2.center_x += (dis_r + a)*cos
                        ball2.center_y += (dis_r + a)*sin
                    else:
                        ball1.center_x -= (dis_r + a)*cos
                        ball1.center_y -= (dis_r + a)*sin

                if ball1.__class__.__name__ == "Bullet":
                    ball1.radians = math.atan2(ball1.change_y,ball1.change_x)
                elif ball2.__class__.__name__ == "Bullet":
                    ball2.radians = math.atan2(ball2.change_y,ball2.change_x)

                """
                if ball1.__class__.__name__ == "Ball":
                    ball1.health -= 10
                elif ball2.__class__.__name__ == "Ball":
                    ball2.health -= 10
                """
                ball1.health -= 10
                ball2.health -= 10
                if ball1.health <= 0:
                    ball1.remove_from_sprite_lists()
                
                if ball2.health <= 0:
                    ball2.remove_from_sprite_lists()

                print("vida", ball1.health, ball2.health)
    
    def call_colisions(self):
        """
        Call functions for colision calculation
        """
        self.colision_wall(self.objt_list)
        self.colision_list_list(self.objt_list,self.objt_list)
        self.colision_list_list(self.bullet_list,self.ball_list)
        ##self.colision_ball_floor(self.ball_list,self.floor)
        ##self.colision_player_ball(self.player,self.ball_list)

    def funcname(self, parameter_list):
        """
        docstring
        """
        pass

    def bullet_fire(self, delta_time):
        if self.trigger_press and self.fire_time >= GUN_FIRE_RATE : 
            self.pos = arcade.get_viewport()
            # Create a bullet
            bullet = Bullet(PATH /"images/laserBlue01teste.png", 1)

            bullet.mass = self.player.mass / 1000
            #bullet.mass = 0.02
            bullet.radius = 7
            hitbox: arcade.Texture = arcade.make_circle_texture(bullet.radius * 2, arcade.color.BLACK)
            bullet.hit_box = hitbox.hit_box_points

            #pos = -20
            #bullet.hit_box = ((-5.0, -2.0 + pos), (-2.0, -5.0+ pos), (2.0, -5.0+ pos), (5.0, -2.0+ pos), (5.0, 2.0+ pos), (2.0, 5.0+ pos), (-2.0, 5.0+ pos), (-5.0, 2.0+ pos))  
            #print(bullet.hit_box)

            # Get from the mouse the destination location for the bullet
            # IMPORTANT! If you have a scrolling screen, you will also need
            # to add in self.view_bottom and self.view_left.
            dest_x = self.player.center_x + self.pos[0] 
            dest_y = self.player.center_y + self.pos[2] + 500

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - self.player.center_x
            y_diff = dest_y - self.player.center_y
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying
            # sideways.
            bullet.center_y = self.player.center_y + 150/2
            bulletcopy = copy.deepcopy(bullet)

            if self.bullet_s:
                bullet.center_x = self.player.center_x + 70/2
                bulletcopy.center_x = self.player.center_x - 70/2
                self.bullet_s = 0
            else:
                bullet.center_x = self.player.center_x + 45/2
                bulletcopy.center_x = self.player.center_x - 45/2
                self.bullet_s = 1

            anglec = math.degrees(angle) + random.randrange(-3,4)
            angleb = math.degrees(angle) + random.randrange(-3,4)    

            bulletcopy.angle = anglec
            bullet.angle = angleb
            
            #print(f"Bullet angle: {bullet.angle:.2f}")

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            modify = 100
            bullet.change_x = math.cos(bullet.radians) * delta_time*MOVEMENT_FORCE*modify
            bullet.change_y = math.sin(bullet.radians) * delta_time*MOVEMENT_FORCE*modify

            bulletcopy.change_x = math.cos(bulletcopy.radians) * delta_time * MOVEMENT_FORCE*modify
            bulletcopy.change_y = math.sin(bulletcopy.radians) * delta_time * MOVEMENT_FORCE*modify
            #print(bullet.change_x)

            # Add the bullet to the appropriate lists
            #self.bullet_list.append(bullet) 
            self.bullet_list.extend([bulletcopy,bullet])
            #self.objt_list.extend([bulletcopy,bullet])
            
            #print("Bullet Speed ",bullet.change_y,"  ",bullet.angle)
            self.fire_time = 0

    def bullet_physics(self,bullet_list):
        """Delete Bullets out of range"""
        for bullet in bullet_list:
            if bullet.center_x <= -60:
                bullet.remove_from_sprite_lists()

            if bullet.center_y <= -60:
                bullet.remove_from_sprite_lists()

            if bullet.center_x >= SCREEN_WIDTH + 60:
                bullet.remove_from_sprite_lists()

            if bullet.center_y >= SCREEN_HEIGHT + 60:
                bullet.remove_from_sprite_lists()

    def on_mouse_press(self, x, y, button, modifiers):
        if arcade.MOUSE_BUTTON_LEFT == button:
            self.trigger_press = True
         
    def on_mouse_release(self, x, y, button, modifiers):
        if arcade.MOUSE_BUTTON_LEFT == button:
            self.trigger_press = False           

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        #self.player.change_y = 0
        #self.player.change_x = 0

        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.F:
            # Choose a random color
            
            rand = random.randrange(-5,6)
            meteor = Rigid()
            density = 1/40
            rand_color = random.randrange(12)
            rand_size = random.randrange(1,7)
            rand_angv = random.randrange(-10,11) 

            x_m = METEOR_SPRITE_SIZES[rand_size][0]
            y_m = METEOR_SPRITE_SIZES[rand_size][1]

            image_name = "images/meteoros"
            image_num = str(rand_size)+"w"+str(x_m)+"h"+str(y_m) + ".png"

            tex : arcade.Texture = arcade.load_texture(PATH / (image_name+image_num), x = 0 , y = 48*rand_color, width = x_m ,height = y_m)
            meteor.texture = tex 
            meteor.radius = x_m//2 if x_m < y_m else y_m//2
            hitbox: arcade.Texture = arcade.make_circle_texture(meteor.radius * 2, arcade.color.BLACK)
            meteor.hit_box = hitbox.hit_box_points
            meteor.center_x = self.mouse_x
            meteor.center_y = self.mouse_y
            #meteor.change_y = random.randrange(-5,6)*200#-BALL_MOV*UPDATE_RATEHz
            #meteor.change_x = random.randrange(-5,f6)*200
            meteor.mass = density*math.pi*4/3*(meteor.radius/10)**2
            meteor.health = meteor.radius * 12
            meteor.change_y = 20/meteor.mass
            meteor.change_x = 0
            meteor.change_angle = 5*rand_angv
            meteor.angle = 10*rand_angv
            self.ball_list.append(meteor) 
            self.objt_list.append(meteor)
            #print("Ball Speed ",ball.change_y)

        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = modules.PauseView(self)
            self.pos = arcade.get_viewport()
            self.window.show_view(pause) 

    def on_key_release(self,key,modifiers):
        """Called whenever a key is released"""
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False  

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()
       
        # Draw the background texture loaded on self.background
        #self.background.draw()
        
        # Draw Player
        self.player.draw()
        #self.player.draw_hit_box(arcade.color.YELLOW)

        #for bullet in self.bullet_list:
        #    bullet.draw_hit_box(arcade.color.YELLOW)

        #for ball in self.ball_list:
        #    ball.draw_hit_box(arcade.color.YELLOW)
        # Draw Ball list
        self.ball_list.draw()

        self.bullet_list.draw()

        # Draw floor
        #self.floor.draw()

        # Draw Enemy no screen
        self.enemy_list.draw()

        start_y = 20
        start_x = 50
        # Draw Frames per second
        if not self.delta_time == 0.0 :
            arcade.draw_text(f"Frames per second: {1.0/self.delta_time:7.2f}",
                             start_x, start_y+50, arcade.color.BLACK, 20)

    def on_update(self, delta_time):
        """Update Everything that need to be updated."""
        self.delta_time = delta_time
        self.current_time += delta_time
        self.fire_time += delta_time

        #self.enemy_list.update()
        self.objt_list.on_update(delta_time)

        self.bullet_fire(delta_time)
        self.bullet_physics(self.bullet_list)
        self.bullet_list.on_update(delta_time)

        self.move_player(delta_time)
       
        self.call_colisions()

        self.physics_objt(self.objt_list, delta_time)

        #self.enemy_list.update_animation()
        
def main():
    """Create main"""
    window =  modules.MyWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,UPDATE_RATEHz)
    menu =  modules.MenuView()
    window.show_view(menu)
    arcade.run()    

if __name__ == "__main__":
    main()