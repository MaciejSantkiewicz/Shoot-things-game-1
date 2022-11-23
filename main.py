import pygame, sys
from random import randint, uniform

WINDOW_WIDTH = 1280 
WINDOW_HEIGHT = 720
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000
pygame.init()
pygame.display.set_caption("Shoot things")
pygame.mouse.set_visible(False)
display_surface = pygame.display.set_mode ((WINDOW_WIDTH, WINDOW_HEIGHT))

global_volume = 0.3
arrow_sound = pygame.mixer.Sound('sounds/arrow_woosh.mp3')
arrow_sound.set_volume(global_volume)
hit_sound = pygame.mixer.Sound('sounds/hit.mp3')
hit_sound.set_volume(global_volume)

hit2_sound = pygame.mixer.Sound('sounds/dies.mp3')
hit2_sound.set_volume(0.04)

dies_sound = pygame.mixer.Sound('sounds/hit2.mp3')
dies_sound.set_volume(0.02)

get_hit_sound = pygame.mixer.Sound('sounds/get_hit.mp3')
get_hit_sound.set_volume(global_volume)


#-----------#


class Player(pygame.sprite.Sprite,):
    def __init__(self, groups, coins = 0, speed = 300, health = 3, attack_speed = 0):
        super().__init__(groups)
        self.image = pygame.image.load('sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.can_shoot = True
        self.shoot_time = None
        self.coins = coins
        self.health = health
        self.is_not_hit = True
        self.hit_timer = None
        self.flicker_timer = None
        self.attack_speed = attack_speed


    def avoid_damage(self):
        if not self.is_not_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_timer > 1500:
                self.is_not_hit = True




    def display_stat(self):
        self.font = pygame.font.Font('fonts/font.ttf',30)
        health_text = f"Health: {self.health}"
        text_surf3 = self.font.render(health_text, True ,"White" )
        text_rect3 = text_surf3.get_rect(center = (WINDOW_WIDTH/2,50))
        display_surface.blit(text_surf3, text_rect3)

        self.font = pygame.font.Font('fonts/font.ttf',30)

        score_text = f"Score: {self.coins}"
        text_surf = self.font.render(score_text, True ,"White" )
        text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-10))
        display_surface.blit(text_surf, text_rect)
        


    def game_over(self):
        if pygame.sprite.spritecollide(self, enemies_group, False, pygame.sprite.collide_mask) and self.is_not_hit:
            get_hit_sound.play()
            self.is_not_hit = False
            self.hit_timer = pygame.time.get_ticks()
            self.health -= 1
        if self.health == 0:
            pygame.quit()
            sys.exit() 
        if not self.is_not_hit:
            self.image = pygame.image.load('sprites/player_hit.png').convert_alpha()
        if self.is_not_hit:
            self.image = pygame.image.load('sprites/player.png').convert_alpha()



    def attack_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.attack_speed:
                self.can_shoot = True
        
    def actions(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.rect.y -= self.speed* dt #move up
        if key[pygame.K_s]:
            self.rect.y += self.speed * dt #move down
        if key[pygame.K_a]:
            self.rect.x -= self.speed * dt #move left
        if key[pygame.K_d]:
            self.rect.x += self.speed * dt #move right

        if key[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            arrow_sound.play()
            Arrows1(weapons_group, self.rect.midright)



    def restrictions(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WINDOW_WIDTH:
            self.rect.right= WINDOW_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
        
    def update(self):
        self.avoid_damage()
        self.game_over()
        self.display_stat()
        self.restrictions()
        self.actions()
        self.attack_timer()

class Arrows1(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        self.image = pygame.image.load('sprites/arrows.png').convert_alpha()
        self.rect = self.image.get_rect(midleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 400
        self.direction = pygame.math.Vector2(1, uniform(-0.07,0.07))
        self.rotation = 0
        self.pos = pygame.math.Vector2(self.rect.topleft)
        super().__init__(groups)


    def enemy_colision(self):
        if pygame.sprite.spritecollide(self, enemies_group, True, pygame.sprite.collide_mask):
            self.kill()


    def update(self):
        self.pos  += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        
        self.enemy_colision()
        self.rect.x  += self.speed * dt
        if self.rect.left > WINDOW_WIDTH:
            self.kill()


class Enemies(pygame.sprite.Sprite):
    def __init__(self, groups, speed, health):
        super().__init__(groups)
        self.image = pygame.image.load('sprites/enemy1.png').convert_alpha()
        spawn_point = randint(100, WINDOW_HEIGHT - 100)
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH,spawn_point))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.health = health
        self.max_health = health

    def movement(self):
        self.rect.x -= self.speed * dt

    def display_health(self):
        self.font = pygame.font.Font('fonts/font.ttf',20)
        health_text = f"{str(self.health)+ '/'+ str(self.max_health)}"
        text_surf3 = self.font.render(health_text, True ,"White" )
        text_rect3 = text_surf3.get_rect(midbottom = (self.rect.midtop))
        display_surface.blit(text_surf3, text_rect3)

    def kill_sprite(self):
        self.kill()

    def update(self):
        self.display_health()
        self.movement()
        if self.rect.left < 10:
            self.kill_sprite()
        if pygame.sprite.spritecollide(self, weapons_group, True, pygame.sprite.collide_mask):
            self.health -= 1
            hit2_sound.play()
            if self.health == 0:
                dies_sound.play()
                self.kill_sprite()



class Coursor(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('sprites/coursor.png').convert_alpha()
        self.rect = self.image.get_rect(center = (500,500))
        self.mask = pygame.mask.from_surface(self.image)
    
    def position(self):
        self.pos = pygame.mouse.get_pos()
        self.rect.center = self.pos
    
    def update(self):
        self.position()


player_group = pygame.sprite.GroupSingle()
weapons_group = pygame.sprite.Group()


button1_group = pygame.sprite.GroupSingle()
coursor_group = pygame.sprite.GroupSingle()
test_coursor = Coursor(coursor_group)

player = Player(player_group)

enemies_group = pygame.sprite.Group()

enemies_timer = pygame.event.custom_type() 
pygame.time.set_timer(enemies_timer, 1200)

coins_set = 0
speed_set = 400
attack_speed_set = 500
player.coins = coins_set
click_status = False
player.attack_speed = attack_speed_set

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == enemies_timer:
            Enemies(enemies_group, 60, health = 3)

    if pygame.sprite.groupcollide(weapons_group, enemies_group, False, False, pygame.sprite.collide_mask):
        coins_set += 1
    
    player.coins = coins_set


    display_surface.fill("grey24")

    enemies_group.draw(display_surface)
    player_group.draw(display_surface)
    weapons_group.draw(display_surface)
    button1_group.draw(display_surface)
    coursor_group.draw(display_surface)

    #------
    enemies_group.update()
    weapons_group.update()
    player_group.update()
    coursor_group.update()
    dt = clock.tick(60) / 1000
    pygame.display.update()

