import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importing PIL for image handling


class VowelLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Learn Vowels")
        self.root.geometry("600x700")

        # List of vowels to learn
        self.vowels = ['A', 'E', 'I', 'O', 'U']
        self.current_vowel = 0

        # Simple stories and colors for each vowel
        self.vowel_stories = {
            'A': "A is for Airplane! A vehicle that flies in the sky.",
            'E': "E is for Elephant! A big friend with a long trunk.",
            'I': "I is for Ice Cream! A sweet, cold treat on hot days.",
            'O': "O is for Owl! A wise bird that loves the night.",
            'U': "U is for Umbrella! It keeps you dry in the rain."
        }

        self.background_colors = {
            'A': "#FFDDC1",  # Light peach for A
            'E': "#C1FFD7",  # Light mint green for E
            'I': "#D1D1FF",  # Soft lavender for I
            'O': "#FFECB1",  # Light yellow for O
            'U': "#C1E1FF"  # Light blue for U
        }

        # Paths to images for each vowel
        self.image_paths = {
            'A': "images/airplane.png",
            'E': "images/elephant.png",
            'I': "images/ice_cream.png",
            'O': "images/owl.png",
            'U': "images/umbrella.png"
        }

        # Display area for vowels (reference at the top)
        self.vowel_label = tk.Label(root, text="", font=("Arial", 80), fg="blue")
        self.vowel_label.pack(pady=20)

        # Canvas for drawing the vowel
        self.canvas = tk.Canvas(root, width=400, height=150, bg="white", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)

        # Story label
        self.story_label = tk.Label(root, text="", font=("Arial", 14), wraplength=500, justify="center")
        self.story_label.pack(pady=10)

        # Image label to display the corresponding image
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Navigation and action buttons without borders
        self.next_button = tk.Button(root, text="Next", command=self.next_vowel, borderwidth=0, highlightthickness=0)
        self.next_button.pack(side="right", padx=20, pady=20)

        self.prev_button = tk.Button(root, text="Previous", command=self.prev_vowel, borderwidth=0,
                                     highlightthickness=0)
        self.prev_button.pack(side="left", padx=20, pady=20)

        self.clear_button = tk.Button(root, text="Clear Drawing", command=self.clear_canvas, borderwidth=0,
                                      highlightthickness=0)
        self.clear_button.pack(pady=10)

        # Button to check the drawing match
        self.check_button = tk.Button(root, text="Check Drawing", command=self.check_drawing, borderwidth=0,
                                      highlightthickness=0)
        self.check_button.pack(pady=10)

        # Display the initial vowel, story, and image
        self.display_vowel()

    def display_vowel(self):
        """Display the current vowel, story, background color, and image."""
        current_vowel = self.vowels[self.current_vowel]
        self.vowel_label.config(text=current_vowel, bg=self.background_colors[current_vowel])
        self.story_label.config(text=self.vowel_stories[current_vowel], bg=self.background_colors[current_vowel])
        self.root.config(bg=self.background_colors[current_vowel])
        self.clear_canvas()  # Clear canvas when changing vowels

        # Load and display the image corresponding to the current vowel
        image_path = self.image_paths[current_vowel]
        try:
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.ANTIALIAS)  # Resize image to fit the label
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo, bg=self.background_colors[current_vowel])
            self.image_label.image = photo  # Keep a reference to prevent garbage collection
        except Exception as e:
            print(f"Error loading image for {current_vowel}: {e}")
            self.image_label.config(image='', text="Image not available", bg=self.background_colors[current_vowel])

    def next_vowel(self):
        """Go to the next vowel."""
        self.current_vowel = (self.current_vowel + 1) % len(self.vowels)
        self.display_vowel()

    def prev_vowel(self):
        """Go to the previous vowel."""
        self.current_vowel = (self.current_vowel - 1) % len(self.vowels)
        self.display_vowel()

    def clear_canvas(self):
        """Clear the drawing canvas."""
        self.canvas.delete("all")

    def draw_on_canvas(self, event):
        """Draw on the canvas where the mouse moves with the left button held down."""
        x, y = event.x, event.y
        radius = 3  # Size of the drawn dot
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black")

    def check_drawing(self):
        """Check if the drawing resembles the current vowel (simple similarity check)."""
        current_vowel = self.vowels[self.current_vowel]
        drawn_items = self.canvas.find_all()

        if current_vowel == "A" and len(drawn_items) > 50:
            messagebox.showinfo("Good Job!", f"Your drawing looks like '{current_vowel}'!")
        elif current_vowel == "E" and len(drawn_items) > 40:
            messagebox.showinfo("Good Job!", f"Your drawing looks like '{current_vowel}'!")
        elif current_vowel == "I" and len(drawn_items) < 30:
            messagebox.showinfo("Good Job!", f"Your drawing looks like '{current_vowel}'!")
        elif current_vowel == "O" and len(drawn_items) > 60:
            messagebox.showinfo("Good Job!", f"Your drawing looks like '{current_vowel}'!")
        elif current_vowel == "U" and len(drawn_items) > 45:
            messagebox.showinfo("Good Job!", f"Your drawing looks like '{current_vowel}'!")
        else:
            messagebox.showerror("Try Again", f"Keep trying! Draw '{current_vowel}' clearly.")

# Main app loop
root = tk.Tk()
app = VowelLearningApp(root)
root.mainloop()


