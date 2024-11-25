import pygame
import cv2
import numpy as np
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Vowel Learning App")

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Load templates
TEMPLATE_DIR = "templates"
vowels = ['A', 'E', 'I', 'O', 'U']
templates = {vowel: cv2.imread(os.path.join(TEMPLATE_DIR, f"{vowel}.png"), cv2.IMREAD_GRAYSCALE) for vowel in vowels}

# Initial state
current_vowel_index = 0
drawing_surface = pygame.Surface((400, 400))  # Drawing canvas
drawing_surface.fill(WHITE)
score = 0  # Initialize the user's score

# Function to preprocess images
def preprocess_image(surface):
    """
    Convert Pygame surface to OpenCV format, preprocess, and make it easier to recognize drawings.
    """
    # Convert the Pygame surface to a NumPy array
    raw_str = pygame.image.tostring(surface, "RGB")
    img = np.frombuffer(raw_str, dtype=np.uint8).reshape((400, 400, 3))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    
    # Step 1: Apply Gaussian Blur to smooth the image
    img = cv2.GaussianBlur(img, (5, 5), 0)
    
    # Step 2: Apply Thresholding (simpler binary threshold instead of adaptive)
    _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)
    
    # Step 3: Dilate edges to make shapes more robust
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    
    # Step 4: Resize the image to match template size
    img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_AREA)
    
    return img

# Function to check similarity
def check_similarity(user_drawing, template):
    """
    Compare user drawing with the template using OpenCV.
    Adjust the threshold to make recognition easier.
    """
    similarity = cv2.matchShapes(user_drawing, template, cv2.CONTOURS_MATCH_I1, 0.0)
    
    # Set a higher threshold for easier matching
    if similarity < 0.25:  # Increase from the previous strict value (e.g., 0.1)
        return True
    return False

# Function to render text
def render_text(text, font, color, x, y):
    """Render text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to display the template alongside the canvas
def display_template(vowel):
    """Display the template image for the current vowel."""
    template_image = pygame.image.load(os.path.join(TEMPLATE_DIR, f"{vowel}.png"))
    template_image = pygame.transform.scale(template_image, (150, 150))  # Resize for display
    screen.blit(template_image, (650, 120))

# Main loop
running = True
is_drawing = False
while running:
    # Fill the screen with gray
    screen.fill(GRAY)

    # Display current vowel
    current_vowel = vowels[current_vowel_index]
    render_text(f"Current Vowel: {current_vowel}", font, BLUE, 50, 20)

    # Display score
    render_text(f"Score: {score}", font, GREEN, 800, 20)

    # Display buttons
    pygame.draw.rect(screen, WHITE, (50, 600, 100, 50))  # Previous button
    render_text("Prev", small_font, BLACK, 60, 610)

    pygame.draw.rect(screen, WHITE, (850, 600, 100, 50))  # Next button
    render_text("Next", small_font, BLACK, 870, 610)

    pygame.draw.rect(screen, WHITE, (400, 600, 200, 50))  # Check button
    render_text("Check", small_font, BLACK, 450, 610)

    # Draw the canvas border
    pygame.draw.rect(screen, BLACK, (100, 150, 400, 400), 2)
    screen.blit(drawing_surface, (100, 150))  # Render the drawing canvas

    # Display the template image
    display_template(current_vowel)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = event.pos
                if 100 <= x <= 500 and 150 <= y <= 550:  # Inside canvas
                    is_drawing = True
                elif 50 <= x <= 150 and 600 <= y <= 650:  # Prev button
                    current_vowel_index = (current_vowel_index - 1) % len(vowels)
                elif 850 <= x <= 950 and 600 <= y <= 650:  # Next button
                    current_vowel_index = (current_vowel_index + 1) % len(vowels)
                elif 400 <= x <= 600 and 600 <= y <= 650:  # Check button
                    user_drawing = preprocess_image(drawing_surface)
                    template = templates[current_vowel]
                    similarity = check_similarity(user_drawing, template)

                    # Dynamic threshold based on vowel complexity
                    if current_vowel in ['I', 'O', 'U']:
                        threshold = 0.15
                    else:
                        threshold = 0.1

                    # Check if the drawing matches the template
                    if similarity < threshold:
                        score += 10  # Increment score for a correct match
                        render_text("Good Job!", font, GREEN, 400, 500)
                    else:
                        render_text("Try Again!", font, RED, 400, 500)

                    # Clear the drawing surface after checking
                    drawing_surface.fill(WHITE)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                is_drawing = False

        elif event.type == pygame.MOUSEMOTION:
            if is_drawing:
                x, y = event.pos
                if 100 <= x <= 500 and 150 <= y <= 550:  # Inside canvas
                    pygame.draw.circle(drawing_surface, BLACK, (x - 100, y - 150), 5)

    # Update the display
    pygame.display.flip()

pygame.quit()