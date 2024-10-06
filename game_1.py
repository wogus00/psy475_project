import pygame
import random
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Game_1")

# Define colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER = (150, 150, 255)

# Define positions
left_pos = (150, 200)
right_pos = (450, 200)

# Set up variables
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
response_time_limit = 0.3  # Time limit in milliseconds
feedback_delay = 2000  # Feedback delay in milliseconds

def draw_button(text, rect, color, hover_color):
    """Draws a button with text and returns whether it is hovered."""
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, hover_color if is_hovered else color, rect)
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)
    return is_hovered

def show_start_screen():
    """Displays the start screen with instructions and waits for any key press to start."""
    while True:
        screen.fill(WHITE)
        
        # Display instructions
        instructions = [
            "Simon Effect Game",
            "Instructions:",
            " - A red box will appear on either side of the screen.",
            " - Press 'F' for red and 'J' for blue, regardless of the box position.",
            " - You have 0.5 seconds to respond. If you exceed this time, it counts as a fail.",
            "Try to respond as quickly and accurately as possible!",
            "",
            "Press any key to start!"
        ]
        
        # Render instructions text
        y_offset = 50
        for line in instructions:
            instruction_text = font.render(line, True, BLACK)
            screen.blit(instruction_text, (50, y_offset))
            y_offset += 30  # Line spacing
        
        pygame.display.flip()
        
        # Wait for any key press to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                return True  # Proceed to the game

def run_game():
    """Main game function for 10 trials."""
    success_count = 0
    trial_count = 0
    response_times = {"congruent": [], "incongruent": []}
    running = True
    
    while running and trial_count < 13:

        screen.fill(WHITE)
        
        # Determine random color and position
        color = random.choice([RED, BLUE])
        position = random.choice([left_pos, right_pos])
        
        # Determine congruency
        congruent = (color == RED and position == left_pos) or (color == BLUE and position == right_pos)
        
        # Draw shape and display current trial number
        pygame.draw.rect(screen, color, (*position, 50, 50))
        if trial_count < 3:
            trial_text = font.render(f"Practice", True, BLACK)
        else:
            trial_text = font.render(f"Trial {trial_count - 2}", True, BLACK)
        screen.blit(trial_text, (250, 50))
        pygame.display.flip()
        
        # Record start time
        start_time = time.time()
        outcome = "Fail: wrong button!"
        
        # Clear the event queue to avoid processing old events
        pygame.event.get()
        
        # Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    # Calculate response time
                    response_time = time.time() - start_time
                    # Check if response is correct and within the time limit
                    if ((color == RED and event.key == pygame.K_f) or (color == BLUE and event.key == pygame.K_j)) and response_time <= response_time_limit:
                        outcome = "Success"
                        if trial_count > 2:
                            success_count += 1
                    
                    waiting = False
            # Fail if response time exceeds the limit
            if time.time() - start_time > response_time_limit:
                waiting = False
                outcome = f"Fail: too slow!"
        # Show outcome (Success/Fail) with a blank screen
        screen.fill(WHITE)
        outcome_text = font.render(f"{outcome}!", True, BLACK)
        screen.blit(outcome_text, (250, 200))
        pygame.display.flip()
        trial_count += 1
        pygame.time.delay(feedback_delay)  # 2-second delay before next trial

    return success_count

def main():
    # Show the start screen first
    if not show_start_screen():
        return  # Exit if the player closes the window from the start screen

    while True:
        # Run the game and get success count
        success_count = run_game()

        # Display results and buttons for restart/quit
        while True:
            screen.fill(WHITE)
            
            # Display total success count
            result_text = font.render(f"Total successful responses: {success_count} out of 10 trials", True, BLACK)
            screen.blit(result_text, (60, 100))
            
            # Define button areas
            restart_button_rect = pygame.Rect(200, 250, 100, 50)
            quit_button_rect = pygame.Rect(350, 250, 100, 50)
            
            # Draw buttons
            restart_hovered = draw_button("Restart", restart_button_rect, BUTTON_COLOR, BUTTON_HOVER)
            quit_hovered = draw_button("Quit", quit_button_rect, BUTTON_COLOR, BUTTON_HOVER)
            
            pygame.display.flip()
            
            # Handle button clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_hovered:
                        main()  # Restart the game
                        return
                    elif quit_hovered:
                        pygame.quit()
                        return

# Start the main loop
main()
