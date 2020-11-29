

import main 
from import_mod_const import *

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        pass
    def on_draw(self):
        arcade.start_render()
        pos = arcade.get_viewport()
        self.background = arcade.Sprite()
        self.background.texture = arcade.load_texture(PATH / "images/pause-game.jpg")
        self.background.scale = 2
        self.background.center_x = SCREEN_WIDTH//2 + pos[0]
        self.background.center_y = SCREEN_HEIGHT//2 +pos[2]
        self.background.draw()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            game = main.MyGame()
            game.setup()
            self.window.show_view(game)

class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.Sprite()
        self.background.center_x = SCREEN_WIDTH//2
        self.background.center_y = SCREEN_HEIGHT//2
        self.background.scale = 2
        self.background.texture = arcade.load_texture(PATH / "images/cloudy_sky_aerial_view-1296x728-header.jpg")

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        arcade.draw_text("Menu Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLUE, font_size=50, anchor_x="center")
        arcade.draw_text("Click para iniciar.", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.BLUE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = main.MyGame()
        game.setup()
        self.window.show_view(game)

class MyWindow(arcade.Window):
    def __init__(self, width, height, title, frame_rate ):
        """
        Initializer
        """
        # Call the parent class initializer
        super().__init__(width, height, title, update_rate = frame_rate)

class AnimatedTime(arcade.AnimatedTimeBasedSprite): 
    """ Change arcade.AnimatedTimeBasedSprite to Work with Animations with diferente number of Frames"""
    def __init__(self,
                 filename: str = None,
                 scale: float = 1,
                 image_x: float = 0, image_y: float = 0,
                 image_width: float = 0, image_height: float = 0,
                 center_x: float = 0, center_y: float = 0,
                 _repeat_count_x=1, _repeat_count_y=1):

        super().__init__(filename=filename, scale=scale, image_x=image_x, image_y=image_y,
                         image_width=image_width, image_height=image_height,
                         center_x=center_x, center_y=center_y)      

    def update_animation(self, delta_time: float = 1/60):
        """
        Logic for selecting the proper texture to use.
        """
        self.time_counter += delta_time
        # if put here to reset cur_frame_idx
        # cur_frame_idx need to be reseted in case another Animation is loaded
        if self.cur_frame_idx >= len(self.frames):
                self.cur_frame_idx = 0
        while self.time_counter > self.frames[self.cur_frame_idx].duration / 1000.0:
            self.time_counter -= self.frames[self.cur_frame_idx].duration / 1000.0
            self.cur_frame_idx += 1
            if self.cur_frame_idx >= len(self.frames):
                self.cur_frame_idx = 0
            # source = self.frames[self.cur_frame].texture.image.source
            cur_frame = self.frames[self.cur_frame_idx]
            # print(f"Advance to frame {self.cur_frame_idx}: {cur_frame.texture.name}")
            self.texture = cur_frame.texture        

class AnimatedTime_Enemy(AnimatedTime): 
    """Custom Class to Enemy Animations"""
    def __init__(self,
                 filename: str = None,
                 scale: float = 1,
                 image_x: float = 0, image_y: float = 0,
                 image_width: float = 0, image_height: float = 0,
                 center_x: float = 0, center_y: float = 0,
                 _repeat_count_x=1, _repeat_count_y=1):

        super().__init__(filename=filename, scale=scale, image_x=image_x, image_y=image_y,
                         image_width=image_width, image_height=image_height,
                         center_x=center_x, center_y=center_y)

        self.change_x = 0
        self.change_y = 0 
    '''
    def update(self):

        # Move the coin
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1
    '''

class Particle(arcade.SpriteCircle):

    """ Explosion particle """
    def __init__(self, my_list):

        color = random.choice(PARTICLE_COLORS)
        # Make the particle
        super().__init__(PARTICLE_RADIUS, color)

        # Track normal particle texture, so we can 'flip' when we sparkle.
        self.normal_texture = self.texture

        # Keep track of the list we are in, so we can add a smoke trail
        self.my_list = my_list

        # Set direction/speed
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        # Track original alpha. Used as part of 'sparkle' where we temp set the
        # alpha back to 255
        self.my_alpha = 255

        # What list do we add smoke particles to?
        self.my_list = my_list
    def update(self):
        """ Update the particle """
        if self.my_alpha <= PARTICLE_FADE_RATE:
            # Faded out, remove
            self.remove_from_sprite_lists()
        else:
            # Update
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= PARTICLE_GRAVITY

            # Should we sparkle this?
            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(self.width, arcade.color.WHITE)
            else:
                self.texture = self.normal_texture

            # Leave a smoke particle?
            if random.random() <= SMOKE_CHANCE:
                smoke = Smoke(3)
                smoke.position = self.position
                self.my_list.append(smoke)

class Smoke(arcade.SpriteCircle):
    """ This represents a puff of smoke """
    def __init__(self, size):
        super().__init__(size, arcade.color.LIGHT_GRAY, soft=True)
        
        self.change_y = SMOKE_RISE_RATE
        self.scale = SMOKE_START_SCALE

    def update(self):
        """ Update this particle """
        if self.alpha <= PARTICLE_FADE_RATE:
            # Remove faded out particles
            self.remove_from_sprite_lists()
        else:
            # Update values
            self.alpha -= SMOKE_FADE_RATE
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.scale += SMOKE_EXPANSION_RATE
