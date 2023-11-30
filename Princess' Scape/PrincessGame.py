import pygame 
pygame.init()
from random import randint, random , choice
from sys import exit  #if you dont add this the game is not going to be able to be closed


class Player(pygame.sprite.Sprite):

    def __init__(self): #this is a method because is inside a class
        super().__init__()
        player_walk_1 = pygame.image.load("walking1.png").convert_alpha()
        player_walk_2 = pygame.image.load("walking2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("Jumping.png").convert_alpha()
        
        self.image =self.player_walk [self.player_index]
        self.rect = self.image.get_rect (midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("jump.mp3")
        self.jump_sound.set_volume(0.15)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = - 25
            self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: 
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else: 
            self.player_index += 0.1 
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)] 
        

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state( )

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "bee" :
            bee_frame1 = pygame.image.load("bee1.png").convert_alpha()
            bee_frame2 = pygame.image.load("bee2.png").convert_alpha()
            self.frames = [bee_frame1, bee_frame2]
            y_pos = 210
        else: 
            bear_frame1 = pygame.image.load("bear1.png").convert_alpha()
            bear_frame2 = pygame.image.load("bear2.png").convert_alpha()
            self.frames = [bear_frame1, bear_frame2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect (midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()  
        self.rect.x -= 6   
        self.destroy()  

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
         

def obstacle_movement(obstacle_list):
    if obstacle_list:    #if python finds the list empty, it will became false and it will not run
        for obstacle_rect in obstacle_list:  #its going to analize eacch rectangle in the list
            obstacle_rect.x -= 5  #it will move each rectangle by 5 to the left on every cicle. #thee five is speed
            
            if obstacle_rect.bottom == 300:
                screen.blit(bear_surf, obstacle_rect) #will move the rect. and the surface in the same position in one go
            else: 
                screen.blit(bee_surf,obstacle_rect)

        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []
def display_score():
    current_time = int (pygame.time.get_ticks()/ 1000) - start_time
    score_surf  = test_font.render(f'{current_time}', False, 'plum')
    score_rect = score_surf.get_rect(center =(400,50))
    screen.blit(score_surf, score_rect)
    return current_time 

def collisions(player,obstacles):
    if obstacles: 
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

def player_animation(): 
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]  
    #play walking animation if the player is on floor
    #display the jump surface when player is not on floor



screen= pygame.display.set_mode((800, 400)) #this is our surface (like the canvas) (with,height)
pygame.display.set_caption("Nef Nef's game") 
clock = pygame.time.Clock()
test_font =pygame.font.Font("Pixeltype.ttf", 80) # first is font type and then font size
game_active = False 
start_time = 0
score = 0
bg_Music = pygame.mixer.Sound("Back_music.wav")
bg_Music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load("fondo.png").convert()
ground_surface = pygame.image.load("ground.png").convert()

#score_surf= test_font.render(' my game ',False,'pink') #first is text, then if you want to anti-aliase it(smooth edges of the font), and then the color
#score_rect = score_surf.get_rect(center = (400, 50))

#Bear
bear_frame1 = pygame.image.load("bear1.png").convert_alpha()
bear_frame2 = pygame.image.load("bear2.png").convert_alpha()
bear_frames = [bear_frame1, bear_frame2]
bear_frames_index = 0
bear_surf = bear_frames[bear_frames_index]


#bee
bee_frame1 = pygame.image.load("bee1.png").convert_alpha()
bee_frame2 = pygame.image.load("bee2.png").convert_alpha()
bee_frames = [bee_frame1, bee_frame2]
bee_frames_index = 0
bee_surf = bee_frames[bee_frames_index]


obstacle_rect_list = []

player_walk_1 = pygame.image.load("walking1.png").convert_alpha()
player_walk_2 = pygame.image.load("walking2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("Jumping.png").convert_alpha()


player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (100,300))
player_gravity = 0

#Player screen
player_stand = pygame.image.load("front.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

#INTRO SCREEN
game_name = test_font.render ("Princess' scape", False, ('plum'))
game_name_rect = game_name.get_rect( center = (400, 75))

game_continue = test_font.render('Press space bar to continue', False, 'plum')
game_continue_rect = game_continue.get_rect( center= (400, 320))

#TIMMER
obstacle_timer= pygame.USEREVENT + 1 #there are some events that are assigned to python so you add +1 to not overwrite them
pygame.time.set_timer(obstacle_timer, 1500)

bear_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(bear_animation_timer, 500)

bee_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bee_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:    
            if event.type == pygame.MOUSEBUTTONDOWN:
                player_gravity = -25
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -25 
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time =  int (pygame.time.get_ticks()/ 1000)

        if game_active:
    
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["bee", "bear", "bear", "fly"])))
                # if randint(0,2):                                                                               |
                #     obstacle_rect_list.append(bear_surf.get_rect(bottomright = (randint(900, 1100),300)))      | added into
                # else:                                                                                          |  the classes
                #     obstacle_rect_list.append(bee_surf.get_rect(bottomright = (randint(900, 1100),210)))       |

            if event.type == bear_animation_timer:
                if bear_frames_index == 0: bear_frames_index = 1
                else: bear_frames_index = 0 
                bear_surf = bear_frames[bear_frames_index]

            if event.type == bee_animation_timer:
                if bee_frames_index == 0 : bee_frames_index = 1
                else: bee_frames_index = 0
                bee_surf = bee_frames[bee_frames_index]
                    




        

    if game_active:
        screen.blit(sky_surface,(0,0)) #block image transfer, adding one image to our surface
        screen.blit(ground_surface,(0,300))
        #pygame.draw.rect(screen, 'plum', score_rect,6,30) #where is goint to be shown, color, what is inside, the with of the line and the rounded corner
        #screen.blit(score_surf,(score_rect))
        score = display_score()
        
        


        # bear_rect.x -= 4               |
        # if bear_rect.right <= 0 :      | this is useful only if the snail is juts appearing in a loop and not animated 
        #     bear_rect.left = 800       |
        
        
        #player
        # player_gravity += 1                          |
        # player_rect.y += player_gravity              |
        # if player_rect.bottom >= 300:                | all of this was added into the classes
        #     player_rect.bottom = 300                 |
        # player_animation()                           |
        # screen.blit(player_surf,player_rect)         |
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()

        #OBSTACLE MOVEMENT
        #obstacle_rect_list =obstacle_movement(obstacle_rect_list)  added into the classes

        #COLLISION
        game_active = collision_sprite()
        # game_active = collisions(player_rect,obstacle_rect_list)  added into the classes
    else: 
        screen.fill('#1F9DCC')
        screen.blit(player_stand,player_stand_rect)
        score_message = test_font.render(f'Your score: {score}',False,'plum' )
        score_message_rect = score_message.get_rect(center = (400, 330))
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0 

        screen.blit (game_name, game_name_rect)
        if score == 0:
            screen.blit(game_continue, game_continue_rect)
        else:
            screen.blit(score_message,score_message_rect)

    

    #ANOTHER WAYS TO DO SOME OF THE ACTIONS THAT ARE IN THE LOOP
    #keys = (pygame.key.get_pressed())
    #if keys[pygame.K_SPACE]:
        #print("jump")

    #if player_rect.colliderect(bear_rect): #if there is a collicion we will get a 1 if not a 0
        #print("collision")
    #mouse_pos = pygame.mouse.get_pos()
    #if player_rect.collidepoint((mouse_pos)):
        #print(pygame.mouse.get_pressed()) #you can also do the 2nd if in the while loop
    
    pygame.display.update()
    clock.tick(60)