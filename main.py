import pygame
import math

from pygame.sprite import Sprite

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Asteroids"

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()
TICK = 60

def load_image(image, scale):
    img = pygame.image.load(image).convert_alpha()
    size = img.get_size()
    return pygame.transform.scale(img, (int(size[0] * scale), int(size[1] * scale)))

SPRITES = {
    "Player": load_image("player.png", 4),
    "Bullet": load_image("bullet.png", 4)
}

class Player:
    def __init__(self, position, speed, rot_speed):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.velocity = 0
        self.angle = 0
        self.bullet_pos = self._calc_bullet_pos()
        self.rot_speed = rot_speed
        self.sprite = SPRITES["Player"]
        #self.sprite_offset = pygame.Vector2(-self.sprite.get_size()[0] / 2, 
        #                    -self.sprite.get_size()[1] / 2)
    
    def update(self, keys):
        self.angle += (int(keys[pygame.K_a]) - int(keys[pygame.K_d])) * self.rot_speed
        if keys[pygame.K_w]:
            self.velocity = lerp(self.velocity, self.speed, 0.05)
        elif keys[pygame.K_s]:
            self.velocity = lerp(self.velocity, -self.speed, 0.05)
        else:
            self.velocity = lerp(self.velocity, 0, 0.05)
        self.angle  %= 360
        x_change = round((math.sin(math.radians(360-self.angle)) * self.velocity), 3)
        y_change = round((-math.cos(math.radians(360-self.angle)) * self.velocity), 3)
        print(self.velocity, x_change, y_change)
        self.position += pygame.Vector2(x_change, y_change)
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT
        self.bullet_pos = self._calc_bullet_pos()
        pygame.draw.rect(screen, (255, 0, 0), (self.bullet_pos, (1, 1)))

    def _calc_bullet_pos(self):
        return self.position + pygame.Vector2(math.sin(math.radians(360-self.angle)),
            -math.cos(math.radians(360-self.angle))).normalize() * 29

    def spawn_bullet(self):
        return Bullet(self.bullet_pos, self.angle, 5)

    def draw(self):
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        sprite_offset = pygame.Vector2(-rotated_sprite.get_size()[0] / 2, 
                            -rotated_sprite.get_size()[1] / 2)
        #pygame.draw.rect(screen, (255, 0, 0), (self.position + sprite_offset, rotated_sprite.get_size()))
        screen.blit(rotated_sprite, self.position + sprite_offset)

class Bullet:
    def __init__(self, position, angle, speed):
        self.position = pygame.Vector2(position)
        self.angle = angle
        self.speed = speed
        self.sprite = pygame.transform.rotate(SPRITES["Bullet"], self.angle)
        self.position.x -= self.sprite.get_size()[0] / 2
        self.position.y -= self.sprite.get_size()[1] / 2
        self.velocity = self._calc_vel()
    
    def _calc_vel(self):
        return pygame.Vector2(math.sin(math.radians(360-self.angle)),
            -math.cos(math.radians(360-self.angle))).normalize() * self.speed
    
    def update(self):
        self.position += self.velocity
        if self.position.x < 0 or self.position.x > SCREEN_WIDTH or self.position.y < 0 or self.position.y > SCREEN_HEIGHT:
            queued_delete_bullets.append(self)
    
    def draw(self):
        screen.blit(self.sprite, self.position)

def clamp(val, minv, maxv):
    return min(max(val, minv), maxv)

def lerp(value, destination, weight):
    lerped = round(value + weight * (destination - value), 3)
    if (lerped < destination + 0.01 and lerped > destination - 0.01): return destination
    return lerped

player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 3, 3)

bullets = []
queued_delete_bullets = []

running = True
while running:
    clock.tick(TICK)
    pygame.display.set_caption("Asteroids - " + str(int(clock.get_fps())) + "fps with " + str(len(bullets)) + " bullets")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(player.spawn_bullet())
    #bullets.append(player.spawn_bullet())
    screen.fill(1)
    for bullet in bullets:
        bullet.update()
        bullet.draw()
    for bullet in queued_delete_bullets:
        if bullet in bullets:
            bullets.remove(bullet)
        queued_delete_bullets.remove(bullet)
    player.update(pygame.key.get_pressed())
    player.draw()
    pygame.display.update()

pygame.quit()