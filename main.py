import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Tag Game")

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BG_COLOR = (200, 200, 200)

# Player settings
PLAYER_SIZE = 40
MAX_SPEED = 5
ACCELERATION = 0.5
FRICTION = 0.2

# Define player class
class Player:
    def __init__(self, x, y, color, is_it=False):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.color = color
        self.is_it = is_it
        self.stun = 0

        # Velocity components for acceleration movement
        self.vel_x = 0
        self.vel_y = 0

    def update(self, surface):
        if self.stun > 0:
            self.stun -= 1
            # No movement if stunned, but still draw
            pygame.draw.rect(surface, self.color, self.rect)
            return

        # Move the player based on velocity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Keep player inside the screen bounds
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - PLAYER_SIZE, self.rect.y))

        pygame.draw.rect(surface, self.color, self.rect)

    def accelerate(self, dx, dy):
        if self.stun > 0:
            return  # Can't accelerate while stunned

        # Accelerate velocity by given direction * acceleration
        if dx != 0:
            self.vel_x += ACCELERATION * dx
            # Clamp velocity
            self.vel_x = max(-MAX_SPEED, min(MAX_SPEED, self.vel_x))
        else:
            # Apply friction to slow down velocity.x when no input
            if self.vel_x > 0:
                self.vel_x = max(0, self.vel_x - FRICTION)
            elif self.vel_x < 0:
                self.vel_x = min(0, self.vel_x + FRICTION)

        if dy != 0:
            self.vel_y += ACCELERATION * dy
            # Clamp velocity
            self.vel_y = max(-MAX_SPEED, min(MAX_SPEED, self.vel_y))
        else:
            # Apply friction to slow down velocity.y when no input
            if self.vel_y > 0:
                self.vel_y = max(0, self.vel_y - FRICTION)
            elif self.vel_y < 0:
                self.vel_y = min(0, self.vel_y + FRICTION)


# Create players
player1 = Player(100, HEIGHT // 2, BLUE, is_it=False)  # Controlled by arrow keys
player2 = Player(WIDTH - 140, HEIGHT // 2, RED, is_it=True)  # AI controlled

clock = pygame.time.Clock()

def ai_move(it_player, target_player):
    if it_player.stun > 0:
        return

    # Move towards target using acceleration logic:
    dx = 0
    dy = 0

    if it_player.rect.x < target_player.rect.x:
        dx = 1
    elif it_player.rect.x > target_player.rect.x:
        dx = -1

    if it_player.rect.y < target_player.rect.y:
        dy = 1
    elif it_player.rect.y > target_player.rect.y:
        dy = -1

    it_player.accelerate(dx, dy)


running = True
delay = 10
STUN_TIME = 60

while running:
    clock.tick(60)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys for player1 acceleration
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx = -1
    elif keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    elif keys[pygame.K_DOWN]:
        dy = 1

    player1.accelerate(dx, dy)

    # AI moves player2 if they are "it"
    if player2.is_it:
        ai_move(player2, player1)
    else:
        # If player1 is "it", make player2 run away from player1
        if player1.is_it and player2.stun == 0:
            # Run away by accelerating opposite direction
            dx = 0
            dy = 0
            if player2.rect.x < player1.rect.x:
                dx = -1
            elif player2.rect.x > player1.rect.x:
                dx = 1
            if player2.rect.y < player1.rect.y:
                dy = -1
            elif player2.rect.y > player1.rect.y:
                dy = 1

            player2.accelerate(dx, dy)

    delay -= 1
    # Check collision (tag)
    if player1.rect.colliderect(player2.rect) and delay <= 0:
        # Swap "it" status
        player1.is_it, player2.is_it = player2.is_it, player1.is_it
        # Update colors
        player1.color = RED if player1.is_it else BLUE
        player2.color = RED if player2.is_it else BLUE

        # Stun the tagged player (the one who just became "it")
        if player1.color == RED:
            player1.stun = STUN_TIME
            player1.vel_x = 0
            player1.vel_y = 0
        else:
            player2.stun = STUN_TIME
            player2.vel_x = 0
            player2.vel_y = 0

        delay = 100

    # Draw players
    player1.update(screen)
    player2.update(screen)

    # Display instructions
    font = pygame.font.SysFont(None, 24)
    text = font.render("Use arrow keys to move with acceleration. Avoid the red player or tag if you are red!", True, (0,0,0))
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
