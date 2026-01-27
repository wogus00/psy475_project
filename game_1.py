import pygame
import random
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Wizard Eldrin’s Lost Items")

instruction_image = pygame.image.load("assets/game1_intro.JPG")
instruction_image = pygame.transform.scale(instruction_image, (1200, 800))
background_image = pygame.image.load("assets/background_image.JPG")
end_image = pygame.image.load("assets/game1_end.JPG")
end_image = pygame.transform.scale(end_image, (1200, 800))

green_images = []
red_images = []
blue_images = []
for i in range(1, 11):
    green_images.append(pygame.image.load(f"assets/green/{i}.png"))
    red_images.append(pygame.image.load(f"assets/red/{i}.png"))
    blue_images.append(pygame.image.load(f"assets/blue/{i}.png"))


# Define colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER = (150, 150, 255)
GREEN = (0, 255, 0) 


# Define positions
left_pos = (300, 400)
right_pos = (800, 400)

# Set up variables
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
response_time_limit = 0.45
# 0.45: 4/6 for first person
# 0.45: 6/4 for first person
# 0.3: 0/10 for first person
feedback_delay = 2000  # Feedback delay in milliseconds

def countdown(screen, font):
    for i in range(3, 0, -1):
        screen.blit(background_image, (0, 0))  # Clear the screen with the background
        countdown_text = font.render(str(i), True, BLACK)
        screen.blit(countdown_text, (250, 250))
        pygame.display.update()
        time.sleep(1)


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
        
        # Display the instruction image on the screen
        screen.blit(instruction_image, (0, 0))
        
        
        pygame.display.flip()
        
        # Wait for any key press to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                screen.blit(background_image, (0, 0))
                return True  # Proceed to the game

def run_game():
    """Main game function for 10 trials."""
    success_count = 0
    fail_count = 0
    trial_count = 0
    response_times = {"congruent": [], "incongruent": []}
    running = True
    screen.blit(background_image, (0, 0))

    countdown(screen, font)
    
    while running and trial_count < 13:
        pygame.time.delay(feedback_delay)  # 2-second delay before next trial

        # Determine random color and position
        color = random.choice([RED, BLUE, GREEN])
        position = random.choice([left_pos, right_pos])
        
        # Determine congruency
        congruent = (color == RED and position == left_pos) or (color == BLUE and position == right_pos)
        
        # Select a random image based on color
        if color == RED:
            selected_image = random.choice(red_images)
        elif color == BLUE:
            selected_image = random.choice(blue_images)
        elif color == GREEN:
            selected_image = random.choice(green_images)
        
        # Draw the selected image at the specified position
        screen.blit(background_image, (0, 0))  # Clear the screen with the background
        screen.blit(selected_image, position)
        
        # Display current trial number
        if trial_count < 3:
            trial_text = font.render(f"Practice", True, BLACK)
        else:
            trial_text = font.render(f"Trial {trial_count - 2}", True, BLACK)
        screen.blit(trial_text, (250, 50))
        
        # # Display current score at the bottom
        # score_text = font.render(f"Current Score: {success_count}", True, BLACK)
        # screen.blit(score_text, (250, 700))  # Display the score at the bottom

        pygame.display.flip()
        
        # Record start time
        start_time = time.time()
        outcome = "Fail: wrong button!"
        disappeared = False
        
        # Clear the event queue to avoid processing old events
        pygame.event.get()
        
        # Wait for input
        waiting = True
        green_success = False
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    # Handle key press
                    if not disappeared:
                        # Calculate response time
                        response_time = time.time() - start_time
                        
                        # Check for correct response
                        if color != GREEN and response_time <= response_time_limit:
                            if ((color == RED and event.key == pygame.K_f) or (color == BLUE and event.key == pygame.K_j)):
                                outcome = "Success"
                                if trial_count > 2:
                                    success_count += 1
                            else:
                                outcome = "Fail: wrong button!"
                                if trial_count > 2:
                                    fail_count += 1
                        else:
                            outcome = "Fail: too slow!" if color != GREEN else "Fail: wrong button!"
                            if trial_count > 2:
                                fail_count += 1
                    
                        # Update success count
                        success_count = max(0, success_count)
                        waiting = False
                    else:
                        # After disappearance, any key press is a failure
                        outcome = "Fail: wrong button after disappearance!"
                        if trial_count > 2:
                            fail_count += 1
                        waiting = False
            
            # Handle green case: disappearance and idle success
            if color == GREEN and not disappeared:
                # Disappear the image after a brief display
                if time.time() - start_time > 0.5:  # Display for 0.5 seconds
                    screen.blit(background_image, (0, 0))  # Clear the screen
                    pygame.display.flip()
                    disappeared = True
            
            # End trial if time exceeds limit (e.g., 1 second)
            if time.time() - start_time > 1:
                if color == GREEN and not green_success:
                    outcome = "Success"
                    green_success = True
                    if trial_count > 2:
                        success_count += 1
                elif color != GREEN:
                    outcome = "Fail: too slow!"
                    if trial_count > 2:
                        fail_count += 1
                waiting = False

        # Show outcome (Success/Fail) with a blank screen
        screen.blit(background_image, (0, 0))
        outcome_text = font.render(f"{outcome}!", True, BLACK)
        screen.blit(outcome_text, (250, 200))
        pygame.display.flip()
        trial_count += 1

    return success_count, fail_count



def main():
    # Show the start screen first
    screen.blit(instruction_image, (0, 0))
    if not show_start_screen():
        return  # Exit if the player closes the window from the start screen
    while True:
        # Run the game and get success count
        success_count, fail_count = run_game()

        # Display results and buttons for restart/quit
        while True:
            screen.blit(end_image, (0, 0))
            
            # Display total success count
            result_text = font.render(f"Successes: {success_count}, Failures: {fail_count}", True, BLACK)
            new_lives_text = font.render(f"New Hearts Earned: {success_count}", True, BLACK)
            screen.blit(result_text, (60, 100))
            screen.blit(new_lives_text, (100, 550))
            
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
