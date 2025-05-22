import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (45, 95, 115)
BUTTON_HOVER_COLOR = (65, 125, 145)
OVERLAY_COLOR = (0, 0, 0, 180)  # Semi-transparent black

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Fonts
pygame.font.init()
game_font = pygame.font.SysFont('Arial', 40)
menu_font = pygame.font.SysFont('Arial', 36)
restart_font = pygame.font.SysFont('Arial', 30)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Game variables
game_state = MENU
game_mode = None  # 'PVP' or 'AI'
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = 'X'  # X goes first
winner = None
ai_thinking = False
ai_move_time = 0

def draw_menu():
    screen.fill(BG_COLOR)
    
    # Title
    title_text = "Tic Tac Toe"
    title_surface = game_font.render(title_text, True, TEXT_COLOR)
    title_rect = title_surface.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title_surface, title_rect)
    
    # PVP Button
    pvp_button = pygame.Rect(WIDTH//4 - 100, HEIGHT//2 - 30, 200, 60)
    pvp_color = BUTTON_HOVER_COLOR if pvp_button.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, pvp_color, pvp_button, border_radius=10)
    pvp_text = menu_font.render("Player vs Player", True, TEXT_COLOR)
    pvp_rect = pvp_text.get_rect(center=pvp_button.center)
    screen.blit(pvp_text, pvp_rect)
    
    # AI Button
    ai_button = pygame.Rect(3*WIDTH//4 - 100, HEIGHT//2 - 30, 200, 60)
    ai_color = BUTTON_HOVER_COLOR if ai_button.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, ai_color, ai_button, border_radius=10)
    ai_text = menu_font.render("Player vs AI", True, TEXT_COLOR)
    ai_rect = ai_text.get_rect(center=ai_button.center)
    screen.blit(ai_text, ai_rect)
    
    return pvp_button, ai_button

def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                # Draw X
                pygame.draw.line(screen, CROSS_COLOR, 
                                (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                ((col + 1) * SQUARE_SIZE - SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                                CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                ((col + 1) * SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                (col * SQUARE_SIZE + SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                                CROSS_WIDTH)
            elif board[row][col] == 'O':
                # Draw O
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def get_available_moves():
    moves = []
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                moves.append((row, col))
    return moves

def check_win():
    global winner
    # Check horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            draw_horizontal_winning_line(row)
            winner = board[row][0]
            return True
    
    # Check vertical
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            draw_vertical_winning_line(col)
            winner = board[0][col]
            return True
    
    # Check diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        draw_diagonal_winning_line(0)
        winner = board[0][0]
        return True
    
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] is not None:
        draw_diagonal_winning_line(1)
        winner = board[2][0]
        return True
    
    return False

def draw_horizontal_winning_line(row):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, CIRCLE_COLOR, (15, posY), (WIDTH - 15, posY), 15)

def draw_vertical_winning_line(col):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, CIRCLE_COLOR, (posX, 15), (posX, HEIGHT - 15), 15)

def draw_diagonal_winning_line(direction):
    if direction == 0:
        pygame.draw.line(screen, CIRCLE_COLOR, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)
    else:
        pygame.draw.line(screen, CIRCLE_COLOR, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    global player, game_state, winner, ai_thinking
    player = 'X'
    game_state = PLAYING
    winner = None
    ai_thinking = False
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

def draw_game_over_screen():
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))
    
    # Display winner or draw message
    if winner:
        if game_mode == 'AI' and winner == 'O':
            text = "AI wins!"
        else:
            text = f"Player {winner} wins!"
    else:
        text = "Draw!"
    
    text_surface = game_font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(text_surface, text_rect)
    
    # Display restart message
    restart_text = "Press 'R' to restart or 'M' for menu"
    restart_surface = restart_font.render(restart_text, True, TEXT_COLOR)
    restart_rect = restart_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    screen.blit(restart_surface, restart_rect)

def ai_make_move():
    # Simple AI: First try to win, then block opponent, then take center, 
    # then take corners, then take any available move
    
    # Check if AI can win in the next move
    for row, col in get_available_moves():
        board[row][col] = 'O'  # Try the move
        if check_win():  # If this move wins
            board[row][col] = 'O'  # Keep the move
            return
        board[row][col] = None  # Undo the move
    
    # Check if player can win in the next move and block
    for row, col in get_available_moves():
        board[row][col] = 'X'  # Try the move as if player would make it
        if check_win():  # If this move would make player win
            board[row][col] = 'O'  # Block it
            winner = None  # Reset winner since we were just checking
            return
        board[row][col] = None  # Undo the move
    
    # Take center if available
    if board[1][1] is None:
        board[1][1] = 'O'
        return
    
    # Take corners if available
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    available_corners = [corner for corner in corners if board[corner[0]][corner[1]] is None]
    if available_corners:
        row, col = random.choice(available_corners)
        board[row][col] = 'O'
        return
    
    # Take any available edge
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    available_edges = [edge for edge in edges if board[edge[0]][edge[1]] is None]
    if available_edges:
        row, col = random.choice(available_edges)
        board[row][col] = 'O'
        return

def return_to_menu():
    global game_state, game_mode, player, winner
    game_state = MENU
    game_mode = None
    player = 'X'
    winner = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Menu state
        if game_state == MENU:
            pvp_button, ai_button = draw_menu()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_button.collidepoint(event.pos):
                    game_mode = 'PVP'
                    game_state = PLAYING
                    restart()
                elif ai_button.collidepoint(event.pos):
                    game_mode = 'AI'
                    game_state = PLAYING
                    restart()
        
        # Playing state
        elif game_state == PLAYING:
            if event.type == pygame.MOUSEBUTTONDOWN and not ai_thinking:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                
                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    draw_figures()
                    
                    if check_win():
                        game_state = GAME_OVER
                    elif is_board_full():
                        game_state = GAME_OVER
                        winner = None  # Ensure winner is None for a draw
                    else:
                        player = 'O' if player == 'X' else 'X'
                        
                        # AI's turn
                        if game_mode == 'AI' and player == 'O':
                            ai_thinking = True
                            ai_move_time = time.time() + 0.5  # Add a small delay for AI thinking
            
            # AI makes a move after a short delay
            if game_mode == 'AI' and player == 'O' and ai_thinking and time.time() > ai_move_time:
                ai_make_move()
                draw_figures()
                
                if check_win():
                    game_state = GAME_OVER
                elif is_board_full():
                    game_state = GAME_OVER
                    winner = None  # Ensure winner is None for a draw
                else:
                    player = 'X'
                
                ai_thinking = False
        
        # Game over state
        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                elif event.key == pygame.K_m:
                    return_to_menu()
        
        # Global key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m and game_state != MENU:
                return_to_menu()
    
    # Drawing
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        
        # Show whose turn it is
        if not ai_thinking:
            if game_mode == 'PVP':
                turn_text = f"Player {player}'s turn"
            else:
                turn_text = "Your turn" if player == 'X' else "AI is thinking..."
            
            turn_surface = restart_font.render(turn_text, True, TEXT_COLOR)
            turn_rect = turn_surface.get_rect(center=(WIDTH//2, 20))
            screen.blit(turn_surface, turn_rect)
    elif game_state == GAME_OVER:
        draw_game_over_screen()
    
    pygame.display.update()
    clock.tick(60)
