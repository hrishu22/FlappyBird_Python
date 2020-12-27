import pygame, sys, random
pygame.mixer.pre_init(frequency=44100,size=16, channels=1, buffer=512)
pygame.init()
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(600 ,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(600,random_pipe_pos-200))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx-=5
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=760:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def drawfloor():
    screen.blit(fl, (flpos, 600))
    screen.blit(fl, (flpos+576, 600))
def checkcollision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score=True
            return False
    if bird_rect.top<=-100 or bird_rect.bottom>=600:
        can_score=True
        return False
    return True
def rotate_bird(bird):
    newbird=pygame.transform.rotozoom(bird, bird_movement,1)
    return newbird
def birdanimation():
    newbird=bird_frames[bird_index]
    newbirdrect=newbird.get_rect(center=(100,bird_rect.centery))
    return newbird, newbirdrect
def display(game_state):
    if game_state=='main_game':
        score_surface = font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rect=score_surface.get_rect(center=(288,100))
        screen.blit(score_surface,score_rect)
    if game_state=='game_over':
        score_surface = font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = font.render(f'High Score:{int(score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 300))
        screen.blit(high_score_surface, high_score_rect)
def update(score,high_score):
    if score>high_score:
        high_score=score
    return high_score
def pipe_score():
    global score
    global can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95< pipe.centerx < 105 and can_score:
                score+=1
                score_sound.play()
                can_score=False
            if pipe.centerx < 0:
                can_score=True
screen = pygame.display.set_mode((576,760))
clock=pygame.time.Clock()
font=pygame.font.SysFont("comicsansms",40 )
gravity=0.25
bird_movement=0
gameactive=True
score=0
high_score=0
can_score=True
bgsurface= pygame.image.load('assets/background-day.png').convert()
bg=pygame.transform.scale(bgsurface,(576,760))
floor=pygame.image.load('assets/base.png').convert()
fl=pygame.transform.scale2x(floor)
bird_downflap=pygame.transform.scale2x((pygame.image.load('assets/bluebird-downflap.png').convert_alpha()))
bird_midflap=pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap=pygame.transform.scale2x((pygame.image.load('assets/bluebird-upflap.png').convert_alpha()))
bird_frames=[bird_downflap,bird_midflap,bird_upflap]
bird_index=0
bird_surface=bird_frames[bird_index]
bird_rect=bird_surface.get_rect(center=(100,380))
BIRDFLAP=pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,200)
#bird=pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird=pygame.transform.scale2x(bird)
#bird_rect=bird.get_rect(center=(100,380))
flpos=0
pipe_surface=pygame.image.load('assets/pipe-green.png').convert()
pipe_surface=pygame.transform.scale2x(pipe_surface)
pipe_list=[]
SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1500)
pipe_height=[300,450,500]
gameover_surface=pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
gameover_rect=gameover_surface.get_rect(center=(288,450))
flap_Sound=pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound=pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound=pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown=100
while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_SPACE and gameactive:
                bird_movement=0
                bird_movement -= 10
                flap_Sound.play()
            if event.key==pygame.K_SPACE and gameactive==False:
                gameactive=True
                pipe_list.clear()
                bird_rect.center=(100,380)
                bird_movement=0
                score=0

        if event.type==SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type==BIRDFLAP:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird_surface,bird_rect=birdanimation()
    screen.blit(bg,(0,0))
    if gameactive:
        bird_movement+=gravity
        rotatedbird=rotate_bird(bird_surface)
        bird_rect.centery+=bird_movement
        screen.blit(rotatedbird,bird_rect)
        gameactive=checkcollision(pipe_list)
        pipe_list=move_pipe(pipe_list)
        draw_pipes(pipe_list)
        pipe_score()
        display('main_game')
    else:
        screen.blit(gameover_surface,gameover_rect)
        high_score=update(score,high_score)
        display('game_over')
    flpos-=1
    drawfloor()
    if flpos<=-576:
        flpos=0
    pygame.display.update()
    clock.tick(100)