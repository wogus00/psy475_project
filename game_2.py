import pygame
import random
import sys
from collections import Counter

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Wizard Eldrin’s Test")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 74)
task_font = pygame.font.Font(None, 50)
feedback_font = pygame.font.Font(None, 50)

# Load background image
background_image = pygame.image.load('assets/background_image.JPG')
success_image = pygame.image.load('assets/success.JPG')
failure_image = pygame.image.load('assets/failure.png')

success_image = pygame.transform.scale(success_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
failure_image = pygame.transform.scale(failure_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock
clock = pygame.time.Clock()
FPS = 60

# Generate random number and task
def generate_task():
    p2_target_number = random.choice(["1", "2", "3", "4"])
    while True:
        row1 = ''.join([str(random.randint(1, 4)) for _ in range(10)])  # Generate first row of 10 digits using digits 1-4
        row2 = ''.join([str(random.randint(1, 4)) for _ in range(10)])  # Generate second row of 10 digits using digits 1-4
        combined = row1 + row2
        count = Counter(combined)
        if len(count) >= 2 and p2_target_number in combined:
            min_digit = min(count, key=count.get)
            max_digit = max(count, key=count.get)
            if list(count.values()).count(count[min_digit]) == 1 and list(count.values()).count(count[max_digit]) == 1:
                # Count occurrences of p2_target_number in black font color
                row1_color = [random.choice([BLUE, RED, BLACK]) for _ in range(10)]  # Randomly choose color for each digit in row1
                row2_color = [random.choice([BLUE, RED, BLACK]) for _ in range(10)]  # Randomly choose color for each digit in row2
                p2_answer = sum(1 for i in range(10) if row1[i] == p2_target_number and row1_color[i] == BLACK) + \
                            sum(1 for i in range(10) if row2[i] == p2_target_number and row2_color[i] == BLACK)
                if p2_answer < 5 and p2_answer > 0:
                    break
    
    p1_task_type = random.choice(["BLUE", "RED"])
    p1_task_color = random.choice(["BLUE", "RED"])
    display_answer = p2_answer
    display_task = "UP" if p1_task_type == "BLUE" else "DOWN"
    if p1_task_type == "RED":
        if p2_answer == 1:
            p2_answer = 'q'
        elif p2_answer == 2:
            p2_answer = 'w'
        elif p2_answer == 3:
            p2_answer = 'e'
        elif p2_answer == 4:
            p2_answer = 'r'
    return combined, p1_task_type, p1_task_color, p2_target_number, p2_answer, row1_color, row2_color, display_answer, display_task


# Start screen
def start_screen():
    screen.blit(background_image, (0, 0))  # Display the background image
    start_text = font.render("Press any key to start", True, BLACK)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
# Display buttons and handle events
def display_buttons(score):
    
    button_font = pygame.font.Font(None, 50)
    try_again_text = button_font.render("Try Again", True, BLACK)
    quit_text = button_font.render("Proceed", True, BLACK)
    try_again_rect = try_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

    # Choose background image based on score
    if score > 7:
        screen.blit(success_image, (0, 0))
    else:
        screen.blit(failure_image, (0, 0))

    # Draw buttons
    pygame.draw.rect(screen, WHITE, try_again_rect.inflate(20, 20))
    pygame.draw.rect(screen, BLACK, try_again_rect.inflate(20, 20), 2)
    screen.blit(try_again_text, try_again_rect)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)  
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - final_score_text.get_height() // 2))


    if score > 7:
        pygame.draw.rect(screen, WHITE, quit_rect.inflate(20, 20))
        pygame.draw.rect(screen, BLACK, quit_rect.inflate(20, 20), 2)
        screen.blit(quit_text, quit_rect)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_rect.collidepoint(event.pos):
                    waiting = False
                    main()  # Restart the game
                elif score > 8 and quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


# Main game loop
def main():
    start_screen()  # Show the start screen

    score = 0
    time_limit = 3000  # 3 seconds per task

    for trial in range(10):
        pygame.event.clear()
        current_time = pygame.time.get_ticks()
        combined, p1_task_type, p1_task_color, p2_target_number, correct_answer, row1_color, row2_color, display_answer, display_task = generate_task()
        row1, row2 = combined[:10], combined[10:]
        user_input = ""
        trial_running = True
        feedback = ""

        while trial_running:
            screen.blit(background_image, (0, 0))  # Display the background image
            target_digit_text = font.render(f"{p2_target_number}", True, BLACK)
            task_text = task_font.render(f"{p1_task_type}", True, p1_task_color)
            screen.blit(target_digit_text, (330, 200))
            screen.blit(task_text, (800, 100))
            for i in range(10):
                row1_text = font.render(row1[i], True, row1_color[i])
                row2_text = font.render(row2[i], True, row2_color[i])
                screen.blit(row1_text, (200 + i * 30, 350))
                screen.blit(row2_text, (200 + i * 30, 400))
            
            # Display user input
            input_text = font.render(user_input, True, BLACK)
            screen.blit(input_text, (250, 250))
            
            # Display feedback
            pygame.display.update()

            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isalnum():  # Accept alphanumeric input
                        user_input += event.unicode
                        if p1_task_type == "BLUE" and user_input == str(correct_answer):
                            score += 1
                            feedback = "Correct!"
                        elif p1_task_type == "RED" and user_input == correct_answer:
                            score += 1
                            feedback = "Correct!"
                        else:
                            feedback = f"Wrong, correct answer:"
                        trial_running = False  # Move to the next trial


            # Check if time limit is exceeded
            if pygame.time.get_ticks() - current_time > time_limit:
                feedback = f"Time's up, correct answer:"
                trial_running = False

        # Display feedback for a short periodd;
        screen.blit(background_image, (0, 0))  # Display the background image
        feedback_text = feedback_font.render(feedback, True, BLACK if "Wrong" in feedback or "Time's up" in feedback else GREEN)
        answer_display_text = feedback_font.render(f"{display_task} {display_answer}", True, BLACK)
        screen.blit(feedback_text, (150, 350))
        screen.blit(answer_display_text, (150, 450))
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds before the next trial

    # Display final score
    screen.blit(background_image, (0, 0))  # Display the background image
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - final_score_text.get_height() // 2))
    pygame.display.update()
    display_buttons(score)
    # End of trials
    pygame.quit()

if __name__ == "__main__":
    main()