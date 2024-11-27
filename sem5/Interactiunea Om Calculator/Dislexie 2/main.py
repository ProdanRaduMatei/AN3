import tkinter as tk
from tkinter import messagebox
import pygame
import os
import random
import sounddevice as sd
import numpy as np
import speech_recognition as sr

# Inițializează pygame pentru sunete
pygame.mixer.init()

# Funcție pentru a reda un fișier audio
def play_sound(file_name):
    file_name = file_name.upper()  # Convertim inputul la majuscule pentru consistență
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
    learn_window.configure(bg="#E0F7FA")

    vowels = [('A', 'a'), ('E', 'e'), ('I', 'i'), ('O', 'o'), ('U', 'u')]

    instruction_label = tk.Label(
        learn_window,
        text="Apasă pe fiecare vocală pentru a-i auzi sunetul!",
        font=("Arial", 16),
        bg="#E0F7FA",
        fg="black",
        pady=20,
    )
    instruction_label.pack()

    buttons_frame = tk.Frame(learn_window, bg="#E0F7FA")
    buttons_frame.pack()

    for big, small in vowels:
        row_frame = tk.Frame(buttons_frame, bg="#E0F7FA")
        row_frame.pack(pady=5)

        big_button = tk.Button(
            row_frame,
            text=big,
            font=("Arial", 20),
            bg="#B2EBF2",
            fg="black",
            command=lambda v=big: play_sound(v),
            width=5
        )
        big_button.pack(side=tk.LEFT, padx=5)

        small_button = tk.Button(
            row_frame,
            text=small,
            font=("Arial", 20),
            bg="#B2EBF2",
            fg="black",
            command=lambda v=small: play_sound(v),
            width=5
        )
        small_button.pack(side=tk.LEFT, padx=5)

# Joc interactiv pentru selectarea vocalei corecte
def play_game():
    global score
    game_window = tk.Toplevel(app)
    game_window.title("Joacă - Selectează vocala corectă")
    game_window.geometry("600x400")
    game_window.configure(bg="#D4F1B4")

    vowels = [('A', 'a'), ('E', 'e'), ('I', 'i'), ('O', 'o'), ('U', 'u')]
    correct_vowel = tk.StringVar()

    def update_question():
        selected_pair = random.choice(vowels)
        correct_vowel.set(random.choice(selected_pair))
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
        update_match_button()
        update_question()

    question_label = tk.Label(game_window, text="", font=("Arial", 20), bg="#D4F1B4", fg="black")
    question_label.pack(pady=20)

    buttons_frame = tk.Frame(game_window, bg="#D4F1B4")
    buttons_frame.pack()

    for big, small in vowels:
        row_frame = tk.Frame(buttons_frame, bg="#D4F1B4")
        row_frame.pack(pady=5)

        big_button = tk.Button(
            row_frame,
            text=big,
            font=("Arial", 20),
            bg="#8CD790",
            fg="black",
            command=lambda v=big: check_answer(v),
            width=5
        )
        big_button.pack(side=tk.LEFT, padx=5)

        small_button = tk.Button(
            row_frame,
            text=small,
            font=("Arial", 20),
            bg="#8CD790",
            fg="black",
            command=lambda v=small: check_answer(v),
            width=5
        )
        small_button.pack(side=tk.LEFT, padx=5)

    score_label = tk.Label(game_window, text=f"Scor: {score}", font=("Arial", 18), bg="#D4F1B4", fg="black")
    score_label.pack(pady=10)

    feedback_label = tk.Label(game_window, text="", font=("Arial", 16), bg="#D4F1B4", fg="black")
    feedback_label.pack(pady=10)

    update_question()

# Jocul de asociere a vocalelor cu cuvintele
def play_sound(file_name):
    file_name = file_name.upper()  # Convertim inputul la majuscule pentru consistență
    sound_path = os.path.join("sounds", f"{file_name}.mp3")
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    else:
        messagebox.showerror("Eroare", f"Fișierul audio {file_name}.mp3 nu a fost găsit!")

# Jocul de asociere a vocalelor cu cuvintele
def play_matching_game():
    match_window = tk.Toplevel(app)
    match_window.title("Joacă - Asociază vocala cu cuvântul")
    match_window.geometry("800x500")
    match_window.configure(bg="#FFE4B5")

    # Cuvintele asociate pentru fiecare vocală
    words = {
        "A": ["Ana"],
        "E": ["Elena"],
        "I": ["India"],
        "O": ["Oscar"],
        "U": ["Ungaria"],
        "a": ["aer", "arbore"],
        "e": ["energie", "efort"],
        "i": ["inel"],
        "o": ["ochi"],
        "u": ["urs"]
    }

    selected_vowel = tk.StringVar()  # Vocală selectată
    current_score = tk.IntVar(value=0)  # Scorul curent
    buttons_dict = {}  # Referințe la butoanele pentru cuvinte

    # Amestecăm cuvintele
    all_words = [(vowel, word) for vowel, word_list in words.items() for word in word_list]
    random.shuffle(all_words)

    def select_vowel(vowel):
        selected_vowel.set(vowel)
        feedback_label.config(text=f"Ai selectat vocala: {vowel}", fg="blue")
        play_sound(vowel)

    def select_word(word):
        vowel = selected_vowel.get()
        if not vowel:
            feedback_label.config(text="Te rog să selectezi mai întâi o vocală!", fg="red")
            play_sound("select_vowel")  # Mesaj audio pentru a selecta vocala
            return

        # Verificăm dacă prima literă a cuvântului corespunde cu vocala selectată
        if word.startswith(vowel):
            play_sound("correct")  # Mesaj audio pentru răspuns corect
            current_score.set(current_score.get() + 1)
            score_label.config(text=f"Scor: {current_score.get()}")
            feedback_label.config(text="Bravo! Ai făcut corect! Selectează o altă vocală.", fg="green")
            # Eliminăm butonul cuvântului corect
            if word in buttons_dict:
                buttons_dict[word].destroy()
                del buttons_dict[word]
            # Resetează selecția vocalei
            selected_vowel.set("")
        else:
            play_sound("wrong")
            feedback_label.config(text="Mai încearcă!", fg="red")

    # Layout-ul pentru vocale
    left_frame = tk.Frame(match_window, bg="#FFE4B5")
    left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

    right_frame = tk.Frame(match_window, bg="#FFE4B5")
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

    # Vocale grupate
    tk.Label(left_frame, text="Vocale", font=("Arial", 20), bg="#FFE4B5").pack(pady=10)
    vowels = [("A", "a"), ("E", "e"), ("I", "i"), ("O", "o"), ("U", "u")]

    for big, small in vowels:
        row_frame = tk.Frame(left_frame, bg="#FFE4B5")
        row_frame.pack(pady=5)

        tk.Button(
            row_frame,
            text=big,
            font=("Arial", 18),
            bg="#F4A460",
            fg="black",
            command=lambda v=big: select_vowel(v),
            width=5
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            row_frame,
            text=small,
            font=("Arial", 18),
            bg="#F4A460",
            fg="black",
            command=lambda v=small: select_vowel(v),
            width=5
        ).pack(side=tk.LEFT, padx=5)

    # Cuvinte în dreapta
    tk.Label(right_frame, text="Cuvinte", font=("Arial", 20), bg="#FFE4B5").pack(pady=10)
    words_frame = tk.Frame(right_frame, bg="#FFE4B5")
    words_frame.pack(pady=10)

    for i, (vowel, word) in enumerate(all_words):
        button = tk.Button(
            words_frame,
            text=word,
            font=("Arial", 18),
            bg="#87CEFA",
            fg="black",
            command=lambda w=word: select_word(w),
            width=10
        )
        button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
        buttons_dict[word] = button  # Salvăm referința la buton

    # Feedback și scor
    feedback_label = tk.Label(match_window, text="", font=("Arial", 16), bg="#FFE4B5", fg="black")
    feedback_label.pack(pady=10)

    score_label = tk.Label(match_window, text="Scor: 0", font=("Arial", 18), bg="#FFE4B5", fg="black")
    score_label.pack(pady=10)
# Funcție pentru acțiunea butonului blocat
def locked_button_action():
    play_locked_message()  # Redăm mesajul audio când jocul este blocat
    messagebox.showinfo("Lacăt",
                        "Trebuie să obții 30 de puncte în jocul de selectare a vocalelor pentru a debloca acest joc!")

# Funcție pentru actualizarea stării butonului de asociere
def update_match_button():
    if score < 2:
        match_button.config(
            text="🔒 Joacă un joc - Asociază cuvântul",
            bg="#FFA07A",
            command=locked_button_action
        )
    else:
        match_button.config(
            text="Joacă un joc - Asociază cuvântul",
            bg="#87CEFA",
            command=play_matching_game
        )

# Jocul în care utilizatorul trebuie să citească vocala folosind vocea
# Jocul de citit vocalele
import speech_recognition as sr

# Jocul de citit vocalele cu vocea
def read_vowel_game_with_voice():
    read_window = tk.Toplevel(app)
    read_window.title("Joacă - Citește vocala cu vocea")
    read_window.geometry("600x400")
    read_window.configure(bg="#FFEDCC")

    vowels = ["A", "E", "I", "O", "U"]  # Lista vocalelor
    current_vowel = tk.StringVar()

    # Funcție pentru generarea unei vocale noi
    def generate_new_vowel():
        current_vowel.set(random.choice(vowels))
        vowel_label.config(text=current_vowel.get())
        feedback_label.config(text="Vorbește clar și spune vocala!")

    # Funcție pentru înregistrare audio
    def record_audio(duration=3, samplerate=16000):
        try:
            feedback_label.config(text="Ascultând... Vorbește clar!", fg="blue")
            audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
            sd.wait()  # Așteaptă să termine înregistrarea
            return np.array(audio_data, dtype='int16').tobytes()
        except Exception as e:
            feedback_label.config(text="Eroare la înregistrare: Verifică microfonul!", fg="red")
            return None

    # Funcție pentru recunoașterea vocii
    def recognize_speech():
        audio_bytes = record_audio()
        if audio_bytes:
            try:
                recognizer = sr.Recognizer()
                audio_data = sr.AudioData(audio_bytes, 16000, 2)
                recognized_text = recognizer.recognize_google(audio_data, language="ro-RO").upper()
                check_reading(recognized_text)
            except sr.UnknownValueError:
                feedback_label.config(text="Nu am înțeles. Încearcă din nou!", fg="red")
                play_sound("wrong")
            except sr.RequestError:
                feedback_label.config(text="Eroare de conectare la serviciul de recunoaștere vocală.", fg="red")

    # Funcție pentru verificarea răspunsului
    def check_reading(user_input):
        if user_input == current_vowel.get():
            play_sound("correct")
            feedback_label.config(text="Bravo! Ai citit corect!", fg="green")
            generate_new_vowel()
        else:
            play_sound("wrong")
            feedback_label.config(
                text=f"Nu ai citit corect. Ai spus: {user_input}, dar vocala este: {current_vowel.get()}",
                fg="red"
            )

    # Eticheta cu vocala curentă
    vowel_label = tk.Label(
        read_window,
        text="",
        font=("Arial", 50),
        bg="#FFEDCC",
        fg="black",
        pady=20
    )
    vowel_label.pack()

    # Buton pentru a începe recunoașterea vocii
    start_button = tk.Button(
        read_window,
        text="Citește cu voce tare",
        font=("Arial", 16),
        bg="#87CEFA",
        fg="black",
        command=recognize_speech
    )
    start_button.pack(pady=20)

    # Eticheta pentru feedback
    feedback_label = tk.Label(
        read_window,
        text="",
        font=("Arial", 16),
        bg="#FFEDCC",
        fg="black"
    )
    feedback_label.pack(pady=20)

    # Generăm prima vocală
    generate_new_vowel()


def drag_and_drop_game():
    drag_window = tk.Toplevel(app)
    drag_window.title("Joacă - Drag and Drop")
    drag_window.geometry("800x600")
    drag_window.configure(bg="#FFFACD")

    # Lista vocalelor
    baskets = ["A", "E", "I", "O", "U"]
    vowels_to_drag = []  # Lista vocalelor de tras
    score = tk.IntVar(value=0)

    # Feedback și scor
    feedback_label = tk.Label(
        drag_window, text="Trage vocala în coșul corect!", font=("Arial", 16), bg="#FFFACD", fg="black"
    )
    feedback_label.pack(pady=10)

    score_label = tk.Label(
        drag_window, text="Scor: 0", font=("Arial", 16), bg="#FFFACD", fg="black"
    )
    score_label.pack(pady=10)

    # Frame pentru coșuri
    basket_frame = tk.Frame(drag_window, bg="#FFFACD")
    basket_frame.pack(side=tk.BOTTOM, pady=20)

    # Creăm coșurile și asociem fiecare cu vocala sa
    basket_labels = []  # Salvăm referințele la coșuri
    for basket in baskets:
        basket_label = tk.Label(
            basket_frame, text=basket, font=("Arial", 18), bg="#FFD700", width=10, height=2, relief="solid"
        )
        basket_label.pack(side=tk.LEFT, padx=10)
        basket_label.vowel = basket  # Asociem vocala coșului
        basket_labels.append(basket_label)

    # Generăm vocalele de tras
    def generate_vowels():
        for i in range(5):  # Creăm 5 vocale random
            vowel = random.choice(baskets)
            vowel_label = tk.Label(drag_window, text=vowel, font=("Arial", 20), bg="#ADD8E6", relief="raised")
            vowel_label.place(x=random.randint(50, 700), y=random.randint(50, 300))
            vowel_label.vowel = vowel  # Asociem vocala cu widgetul
            vowel_label.bind("<B1-Motion>", on_drag)  # Drag
            vowel_label.bind("<ButtonRelease-1>", lambda e, v=vowel_label: on_drop(e, v))  # Drop
            vowels_to_drag.append(vowel_label)

    # Funcție pentru drag
    def on_drag(event):
        # Mutăm widget-ul tras
        event.widget.place(x=event.x_root - drag_window.winfo_rootx(),
                           y=event.y_root - drag_window.winfo_rooty())

    # Funcție pentru drop
    def on_drop(event, vowel_widget):
        # Obținem vocala trasă
        dragged_vowel = vowel_widget.vowel

        # Verificăm plasarea widgetului în cadrul unui coș
        for basket_label in basket_labels:
            bx1, by1, bx2, by2 = (
                basket_label.winfo_x(),
                basket_label.winfo_y(),
                basket_label.winfo_x() + basket_label.winfo_width(),
                basket_label.winfo_y() + basket_label.winfo_height(),
            )
            # Coordonatele plasării
            x, y = event.x_root - drag_window.winfo_rootx(), event.y_root - drag_window.winfo_rooty()

            # Verificăm dacă widgetul este plasat în interiorul coșului
            if bx1 <= x <= bx2 and by1 <= y <= by2:
                # Comparăm vocala widgetului cu vocala coșului
                if basket_label.vowel == dragged_vowel:
                    feedback_label.config(text="Bravo! Ai plasat corect!", fg="green")
                    score.set(score.get() + 1)
                    score_label.config(text=f"Scor: {score.get()}")
                    vowel_widget.destroy()  # Eliminăm widgetul tras
                    vowels_to_drag.remove(vowel_widget)  # Scoatem widgetul din lista de tras
                    return
                else:
                    feedback_label.config(text="Mai încearcă! Vocala nu corespunde coșului.", fg="red")
                    return

        # Dacă widgetul nu a fost plasat într-un coș valid
        feedback_label.config(text="Nu ai plasat vocala în niciun coș!", fg="red")

    generate_vowels()

# Fereastra principală
app = tk.Tk()
app.title("Învățăm Vocalele")
app.geometry("600x400")
app.configure(bg="#BDE0FE")

score = 0

welcome_label = tk.Label(app, text="Bine ai venit! Să învățăm vocalele!", font=("Arial", 20), bg="#BDE0FE", fg="black")
welcome_label.pack(pady=10)

learn_button = tk.Button(app, text="Mod de învățare", font=("Arial", 16), bg="#87CEFA", fg="black",
                         command=learn_vowels)
learn_button.pack(pady=10)

game_button = tk.Button(app, text="Joacă un joc - Selectează vocala", font=("Arial", 16), bg="#90EE90", fg="black",
                        command=play_game)
game_button.pack(pady=10)

match_button = tk.Button(
    app,
    text="🔒 Joacă un joc - Asociază cuvântul",
    font=("Arial", 16),
    bg="#FFA07A",
    fg="black",
    command=locked_button_action
)
match_button.pack(pady=10)

read_vowel_voice_button = tk.Button(
    app,
    text="Joacă un joc - Citește vocala cu vocea",
    font=("Arial", 16),
    bg="#FFA07A",
    fg="black",
    command=read_vowel_game_with_voice
)
read_vowel_voice_button.pack(pady=10)

drag_and_drop_button = tk.Button(
    app,
    text="Joacă un joc - Drag & Drop",
    font=("Arial", 16),
    bg="#FFD700",
    fg="black",
    command=drag_and_drop_game
)
drag_and_drop_button.pack(pady=10)


exit_button = tk.Button(app, text="Ieși", font=("Arial", 16), bg="#FF6961", fg="black", command=app.quit)
exit_button.pack(pady=10)

update_match_button()

app.mainloop()
