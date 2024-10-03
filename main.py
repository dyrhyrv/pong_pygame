import pygame

pygame.init()

FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
PLAYER_WIDTH, PLAYER_HEIGHT = 30, 200
BALL_RADIUS = 20
FONT = pygame.font.Font("NEOPIXEL-Regular.otf", 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

class Player:
    def __init__(self, x_position):
        self.rect = pygame.Rect(x_position, SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = (0, 0, 0)
        self.speed = 0

    def update(self):
        self.rect.y -= self.speed
        self.speed = 0

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.color = (0, 0, 0)
        self.speed_x, self.speed_y = 3, 3

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
            return True
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y = -self.speed_y
        return False
    
    def respawn(self, surface):
        self.text = FONT.render("THE BALL IS OUT!", True, (0,0,0))
        surface.blit((self.text), (SCREEN_WIDTH // 2 - self.text.get_size()[0] / 2, SCREEN_HEIGHT / 2))
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        pygame.display.flip()
        pygame.time.wait(1500)
        

class Score:
    def __init__(self):
        self.count1, self.count2 = 0, 0

    def draw(self, surface):
        self.text1 = FONT.render(str(self.count1), True, (0, 0, 0))
        self.text2 = FONT.render(str(self.count2), True, (0, 0, 0))
        self.text2_width, self.text2_height = self.text2.get_size()
        surface.blit(self.text1, (10, SCREEN_HEIGHT - 50))
        surface.blit(self.text2, (SCREEN_WIDTH - 10 - self.text2_width, SCREEN_HEIGHT - 50))

player1 = Player(10)
player2 = Player(SCREEN_WIDTH - PLAYER_WIDTH - 10)
ball = Ball()
score = Score()

running = True

while running:
    screen.fill((255, 192, 203))

    keys = pygame.key.get_pressed()
    player1.speed = 10 if keys[pygame.K_w] else -10 if keys[pygame.K_s] else 0
    player2.speed = 10 if keys[pygame.K_UP] else -10 if keys[pygame.K_DOWN] else 0

    player1.update()
    player2.update()
    
    if ball.update():
        if ball.rect.right >= SCREEN_WIDTH:
            score.count1 += 1
            ball.respawn(screen)
        elif ball.rect.left <= 0:
            score.count2 += 1
            ball.respawn(screen)

    if player1.rect.colliderect(ball.rect) or player2.rect.colliderect(ball.rect):
        ball.speed_x = -ball.speed_x
        if ball.speed_x > 0:
            ball.speed_x += 1
            ball.speed_y += 1
        else:
            ball.speed_x -= 1
            ball.speed_y -= 1

    score.draw(screen)
    pygame.draw.rect(screen, player1.color, player1.rect)
    pygame.draw.rect(screen, player2.color, player2.rect)
    pygame.draw.circle(screen, ball.color, ball.rect.center, BALL_RADIUS)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.time.Clock().tick(FPS)

pygame.quit()