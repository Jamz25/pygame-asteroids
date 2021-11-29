import pygame
import math

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
    "Player": load_image("player.png", 4)
}

class Player:
    def __init__(self, position, speed, rot_speed):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.velocity = 0
        self.angle = 0
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

    def draw(self):
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        sprite_offset = pygame.Vector2(-rotated_sprite.get_size()[0] / 2, 
                            -rotated_sprite.get_size()[1] / 2)
        #pygame.draw.rect(screen, (255, 0, 0), (self.position + sprite_offset, rotated_sprite.get_size()))
        screen.blit(rotated_sprite, self.position + sprite_offset)

def clamp(val, minv, maxv):
    return min(max(val, minv), maxv)

def lerp(value, destination, weight):
    lerped = round(value + weight * (destination - value), 3)
    if lerped < destination + 0.01 and lerped > destination - 0.01:
        return destination
    else:
        return lerped

player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 3, 3)

running = True
while running:
    clock.tick(TICK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(1)
    player.update(pygame.key.get_pressed())
    player.draw()
    pygame.display.update()

pygame.quit()