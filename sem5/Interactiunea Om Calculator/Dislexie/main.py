import tkinter as tk
from tkinter import messagebox
import pygame
import os
import random
from gtts import gTTS

# Inițializează pygame pentru sunete
pygame.mixer.init()

# Funcție pentru a reda un fișier audio
def play_sound(file_name):
    sound_path = os.path.join("sounds", f"{file_name}.mp3")
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    else:
        messagebox.showerror("Eroare", f"Fișierul audio {file_name}.mp3 nu a fost găsit!")

# Funcție pentru a reda mesajul audio blocat
def play_locked_message():
    play_sound("locked_message")

# Mod de învățare: Ascultă vocalele
def learn_vowels():
    learn_window = tk.Toplevel(app)
    learn_window.title("Învățăm vocalele")
    learn_window.geometry("600x400")
    learn_window.configure(bg="#E0F7FA")  # Fundal albastru deschis

    vowels = ['A', 'E', 'I', 'O', 'U']

    instruction_label = tk.Label(
        learn_window,
        text="Apasă pe fiecare vocală pentru a-i auzi sunetul!",
        font=("Arial", 16),
        bg="#E0F7FA",
        fg="black",
        pady=20,
    )
    instruction_label.pack()

    for vowel in vowels:
        button = tk.Button(
            learn_window,
            text=vowel,
            font=("Arial", 20),
            bg="#B2EBF2",
            fg="black",
            command=lambda v=vowel: play_sound(v),
        )
        button.pack(pady=10)

# Jocul de asociere a vocalelor cu cuvintele
def play_matching_game():
    match_window = tk.Toplevel(app)
    match_window.title("Joacă - Asociază vocala cu cuvântul")
    match_window.geometry("800x500")
    match_window.configure(bg="#FFE4B5")  # Fundal portocaliu deschis

    words = {
        "A": ["Ana", "Ardei", "Apă"],
        "E": ["Elefant", "Elicopter", "Epavă"],
        "I": ["Iepure", "Insulă", "India"],
        "O": ["Om", "Oră", "Ochelari"],
        "U": ["Umbrelă", "Urs", "Ulei"]
    }

    selected_vowel = tk.StringVar()
    current_score = tk.IntVar(value=0)

    def select_vowel(vowel):
        selected_vowel.set(vowel)
        feedback_label.config(text=f"Ai selectat vocala: {vowel}", fg="blue")
        play_sound(vowel)

    def select_word(word):
        vowel = selected_vowel.get()
        if not vowel:
            feedback_label.config(text="Te rog să selectezi mai întâi o vocală!", fg="red")
            return

        if word in words[vowel]:
            play_sound("correct")
            current_score.set(current_score.get() + 1)
            score_label.config(text=f"Scor: {current_score.get()}")
            word_buttons[word].pack_forget()  # Eliminăm cuvântul selectat
            selected_vowel.set("")  # Resetăm selecția de vocală
            feedback_label.config(text="Alege o altă vocală!", fg="purple")
        else:
            play_sound("wrong")
            feedback_label.config(text="Nu ai ales corect. Încearcă din nou!", fg="red")

    left_frame = tk.Frame(match_window, bg="#FFE4B5")
    left_frame.pack(side=tk.LEFT, padx=20, pady=20)

    tk.Label(left_frame, text="Vocale", font=("Arial", 20), bg="#FFE4B5").pack(pady=10)

    for vowel in words.keys():
        button = tk.Button(
            left_frame,
            text=vowel,
            font=("Arial", 18),
            bg="#F4A460",
            fg="black",
            command=lambda v=vowel: select_vowel(v),
        )
        button.pack(pady=5)

    # Adăugăm un Frame cu scroll pentru cuvinte
    right_frame = tk.Frame(match_window, bg="#FFE4B5")
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

    tk.Label(right_frame, text="Cuvinte", font=("Arial", 20), bg="#FFE4B5", anchor="center").pack(pady=(0, 5))

    canvas = tk.Canvas(right_frame, bg="#FFE4B5", width=107, height=300, highlightthickness=0)
    scroll_bar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)

    scrollable_frame = tk.Frame(canvas, bg="#FFE4B5")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_bar.set)

    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    scroll_bar.pack(side=tk.LEFT, fill="y")  # Bara de scroll este lipită de canvas

    word_buttons = {}
    all_words = [word for word_list in words.values() for word in word_list]
    random.shuffle(all_words)

    for word in all_words:
        button = tk.Button(
            scrollable_frame,
            text=word,
            font=("Arial", 18),
            bg="#87CEFA",
            fg="black",
            command=lambda w=word: select_word(w),
        )
        button.pack(pady=5)
        word_buttons[word] = button

    feedback_label = tk.Label(match_window, text="", font=("Arial", 16), bg="#FFE4B5", fg="black")
    feedback_label.pack(pady=10)

    score_label = tk.Label(match_window, text="Scor: 0", font=("Arial", 18), bg="#FFE4B5", fg="black")
    score_label.pack(pady=10)

# Joc interactiv pentru selectarea vocalei corecte
def play_game():
    global score
    game_window = tk.Toplevel(app)
    game_window.title("Joacă - Selectează vocala corectă")
    game_window.geometry("600x400")
    game_window.configure(bg="#D4F1B4")

    vowels = ['A', 'E', 'I', 'O', 'U']
    correct_vowel = tk.StringVar()

    def update_question():
        correct_vowel.set(random.choice(vowels))
        question_label.config(text=f"Alege vocala: {correct_vowel.get()}")
        feedback_label.config(text="")

    def check_answer(vowel):
        global score
        if vowel == correct_vowel.get():
            score += 1
            score_label.config(text=f"Scor: {score}")
            play_sound("correct")
            feedback_label.config(text="Bravo! Ai ales corect!", fg="green")
        else:
            play_sound("wrong")
            feedback_label.config(text="Mai încearcă! Nu ai ales corect.", fg="red")
        if score >= 2:
            unlock_button()
        update_question()

    question_label = tk.Label(game_window, text="", font=("Arial", 20), bg="#D4F1B4", fg="black")
    question_label.pack(pady=20)

    for vowel in vowels:
        button = tk.Button(
            game_window,
            text=vowel,
            font=("Arial", 20),
            bg="#8CD790",
            fg="black",
            command=lambda v=vowel: check_answer(v),
        )
        button.pack(pady=5)

    score_label = tk.Label(game_window, text=f"Scor: {score}", font=("Arial", 18), bg="#D4F1B4", fg="black")
    score_label.pack(pady=10)

    feedback_label = tk.Label(game_window, text="", font=("Arial", 16), bg="#D4F1B4", fg="black")
    feedback_label.pack(pady=10)

    update_question()

# Funcție pentru acțiunea butonului blocat
def locked_button_action():
    if score < 2:
        play_locked_message()
        messagebox.showinfo("Lacăt", "Trebuie să obții 30 de puncte în jocul de selectare a vocalelor pentru a debloca acest joc!")
    else:
        play_matching_game()

# Deblochează butonul jocului de asociere
def unlock_button():
    match_button.config(text="Joacă un joc - Asociază cuvântul", command=play_matching_game)

# Fereastra principală
app = tk.Tk()
app.title("Învățăm Vocalele")
app.geometry("600x400")
app.configure(bg="#BDE0FE")

# Variabilă globală pentru scor
score = 0

welcome_label = tk.Label(app, text="Bine ai venit! Să învățăm vocalele!", font=("Arial", 20), bg="#BDE0FE", fg="black")
welcome_label.pack(pady=10)

learn_button = tk.Button(app, text="Mod de învățare", font=("Arial", 16), bg="#87CEFA", fg="black", command=learn_vowels)
learn_button.pack(pady=10)

game_button = tk.Button(app, text="Joacă un joc - Selectează vocala", font=("Arial", 16), bg="#90EE90", fg="black", command=play_game)
game_button.pack(pady=10)

# Butonul jocului de asociere, cu lacăt, dar activ
match_button = tk.Button(
    app,
    text="🔒 Joacă un joc - Asociază cuvântul",
    font=("Arial", 16),
    bg="#FFA07A",
    fg="black",
    command=locked_button_action
)
match_button.pack(pady=10)

exit_button = tk.Button(app, text="Ieși", font=("Arial", 16), bg="#FF6961", fg="black", command=app.quit)
exit_button.pack(pady=10)

app.mainloop()
