
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
PLAYER_SPEED = 5

# Define player class
class Player:
    def __init__(self, x, y, color, is_it=False):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.color = color
        self.is_it = is_it

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy
        # Keep player inside the screen bounds
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - PLAYER_SIZE, self.rect.y))

# Create players
player1 = Player(100, HEIGHT // 2, BLUE, is_it=False)  # Controlled by arrow keys
player2 = Player(WIDTH - 140, HEIGHT // 2, RED, is_it=True)  # AI controlled

clock = pygame.time.Clock()

def ai_move(it_player, target_player):
    # Simple AI: move towards the other player if not close enough
    if it_player.rect.x < target_player.rect.x:
        it_player.move(PLAYER_SPEED, 0)
    elif it_player.rect.x > target_player.rect.x:
        it_player.move(-PLAYER_SPEED, 0)
    if it_player.rect.y < target_player.rect.y:
        it_player.move(0, PLAYER_SPEED)
    elif it_player.rect.y > target_player.rect.y:
        it_player.move(0, -PLAYER_SPEED)

running = True
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys for player1 movement
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx = -PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        dx = PLAYER_SPEED
    if keys[pygame.K_UP]:
        dy = -PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        dy = PLAYER_SPEED
    player1.move(dx, dy)

    # AI moves player2 if they are "it"
    if player2.is_it:
        ai_move(player2, player1)
    else:
        # If player1 is "it", make player2 run away from player1
        if player1.is_it:
            # Move player2 away from player1
            if player2.rect.x < player1.rect.x:
                player2.move(-PLAYER_SPEED, 0)
            elif player2.rect.x > player1.rect.x:
                player2.move(PLAYER_SPEED, 0)
            if player2.rect.y < player1.rect.y:
                player2.move(0, -PLAYER_SPEED)
            elif player2.rect.y > player1.rect.y:
                player2.move(0, PLAYER_SPEED)

    # Check collision (tag)
    if player1.rect.colliderect(player2.rect):
        # Swap "it" status
        player1.is_it, player2.is_it = player2.is_it, player1.is_it
        # Update colors
        player1.color = RED if player1.is_it else BLUE
        player2.color = RED if player2.is_it else BLUE

    # Draw players
    player1.draw(screen)
    player2.draw(screen)

    # Display instructions
    font = pygame.font.SysFont(None, 24)
    text = font.render("Use arrow keys to move. Avoid the red player or tag if you are red!", True, (0,0,0))
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
