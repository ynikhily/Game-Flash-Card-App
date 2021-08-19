from tkinter import *
import pandas as pd
import random

# -----------------------------------------Important Variables----------------------------------------------

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ('Arial', 40, 'italic')
WORD_FONT = ('Arial', 60, 'bold')
COUNTDOWN = 4
COUNTDOWN_FONT = ('Arial', 25, 'normal')
timer = None
timer_time = None

# -----------------------------------Extracting Data from french_words CSV------------------------------------

data = pd.read_csv('./data/french_words.csv')
french_words = data['French'].tolist()
english_words = data['English'].tolist()
random_item = None

# -------------------------------------- Flash Card State Functions ---------------------------------------


def front_card():
    global timer_time
    global random_item
    timer_time = COUNTDOWN
    random_item = random.randint(0, len(french_words) - 1)
    canvas.itemconfig(card_image, image=card_front_image)
    canvas.itemconfig(language_text, text="French")
    canvas.itemconfig(word_text, text=f"{french_words[random_item]}")

    countdown(timer_time)


def back_card():
    canvas.itemconfig(card_image, image=card_back_image)
    canvas.itemconfig(language_text, text="English")
    canvas.itemconfig(word_text, text=f"{english_words[random_item]}")

# ----------------------------------Button Functions--------------------------------------------------------


def wrong_clicked():
    front_card()


def right_clicked():
    french_words.pop(random_item)
    english_words.pop(random_item)
    front_card()


# ------------------------------------------Countdown Functionality-----------------------------------------


def countdown(seconds):
    if seconds >= 0:
        global timer
        canvas.itemconfig(timer_text, text=f"{seconds:02d}")
        timer = canvas.after(1000, countdown, seconds - 1)
    else:
        canvas.itemconfig(timer_text, text="")
        back_card()

# ------------------------------------User-Interface-------------------------------------------------------


window = Tk()
window.title("Flash Card App")
window.config(padx=25, pady=25, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file='./images/card_front.png')
card_back_image = PhotoImage(file='./images/card_back.png')
card_image = canvas.create_image(400, 263, image=card_front_image)
language_text = canvas.create_text(400, 150, text="French", font=LANGUAGE_FONT)
word_text = canvas.create_text(400, 263, text="Word", font=WORD_FONT)
timer_text = canvas.create_text(700, 50, text=f"{COUNTDOWN:02d}", fill='grey', font=COUNTDOWN_FONT)
canvas.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file='./images/right.png')
wrong_image = PhotoImage(file='./images/wrong.png')

wrong_button = Button(image=wrong_image, highlightthickness=0, width=75, height=75, command=wrong_clicked)
wrong_button.grid(row=1, column=0)

right_button = Button(image=right_image, highlightthickness=0, width=75, height=75, command=right_clicked)
right_button.grid(row=1, column=1)

front_card()

window.mainloop()
