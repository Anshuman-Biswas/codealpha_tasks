import random
import tkinter as tk
from tkinter import messagebox

class HangmanGUI:
    def __init__(self, root):
        """
        Initialize the Hangman game GUI.
        
        :param root: The root window of the application.
        """
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("500x400")

        # Word categories and difficulty levels
        self.categories = {
            "animals": ["elephant", "giraffe", "kangaroo", "penguin", "dolphin"],
            "countries": ["canada", "brazil", "japan", "germany", "australia"],
            "programming": ["python", "javascript", "algorithm", "function", "variable"]
        }
        self.difficulties = {
            "easy": {"max_attempts": 8, "word_length": "short"},
            "medium": {"max_attempts": 6, "word_length": "medium"},
            "hard": {"max_attempts": 4, "word_length": "long"}
        }

        # Initialize game variables
        self.secret_word = ""
        self.guessed_letters = set()
        self.attempts_left = 0
        self.score = 0
        self.current_state = []

        # GUI Elements
        self.category_var = tk.StringVar(value="animals")
        self.difficulty_var = tk.StringVar(value="medium")

        self.setup_menu()
        self.setup_game_ui()

    def setup_menu(self):
        """
        Set up the menu for category and difficulty selection.
        """
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=10)

        tk.Label(menu_frame, text="Choose Category:").grid(row=0, column=0, padx=5)
        self.category_menu = tk.OptionMenu(menu_frame, self.category_var, *self.categories.keys())
        self.category_menu.grid(row=0, column=1, padx=5)

        tk.Label(menu_frame, text="Choose Difficulty:").grid(row=1, column=0, padx=5)
        self.difficulty_menu = tk.OptionMenu(menu_frame, self.difficulty_var, *self.difficulties.keys())
        self.difficulty_menu.grid(row=1, column=1, padx=5)

        tk.Button(menu_frame, text="Start Game", command=self.start_game).grid(row=2, column=0, columnspan=2, pady=10)

    def setup_game_ui(self):
        """
        Set up the main game UI.
        """
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(pady=20)

        self.word_label = tk.Label(self.game_frame, text="", font=("Arial", 24))
        self.word_label.pack()

        self.attempts_label = tk.Label(self.game_frame, text="", font=("Arial", 14))
        self.attempts_label.pack()

        self.score_label = tk.Label(self.game_frame, text="Score: 0", font=("Arial", 14))
        self.score_label.pack()

        self.guess_entry = tk.Entry(self.game_frame, font=("Arial", 14))
        self.guess_entry.pack(pady=10)

        self.guess_button = tk.Button(self.game_frame, text="Guess", command=self.process_guess)
        self.guess_button.pack()

        self.restart_button = tk.Button(self.game_frame, text="Restart", command=self.restart_game, state=tk.DISABLED)
        self.restart_button.pack(pady=10)

    def start_game(self):
        """
        Start a new game with the selected category and difficulty.
        """
        category = self.category_var.get()
        difficulty = self.difficulty_var.get()

        # Filter words based on difficulty
        word_list = self.categories[category]
        if difficulty == "easy":
            word_list = [word for word in word_list if len(word) <= 4]
        elif difficulty == "medium":
            word_list = [word for word in word_list if 5 <= len(word) <= 7]
        elif difficulty == "hard":
            word_list = [word for word in word_list if len(word) >= 8]

        # Check if the word list is empty
        if not word_list:
            messagebox.showwarning("No Words Available", f"No words found for the selected category and difficulty. Please choose a different combination.")
            return

        self.secret_word = random.choice(word_list)
        self.attempts_left = self.difficulties[difficulty]["max_attempts"]
        self.score = 0
        self.guessed_letters = set()
        self.current_state = ['_' for _ in self.secret_word]

        self.update_ui()
        self.guess_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)

    def update_ui(self):
        """
        Update the game UI to reflect the current state.
        """
        self.word_label.config(text=" ".join(self.current_state))
        self.attempts_label.config(text=f"Attempts Left: {self.attempts_left}")
        self.score_label.config(text=f"Score: {self.score}")
        self.guess_entry.delete(0, tk.END)

    def process_guess(self):
        """
        Process the player's guess and update the game state.
        """
        guess = self.guess_entry.get().lower()

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single valid letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Already Guessed", f"You've already guessed '{guess}'. Try a different letter.")
            return

        self.guessed_letters.add(guess)

        if guess in self.secret_word:
            for i, letter in enumerate(self.secret_word):
                if letter == guess:
                    self.current_state[i] = guess
            self.score += 10
        else:
            self.attempts_left -= 1
            self.score -= 5

        self.update_ui()

        if '_' not in self.current_state:
            messagebox.showinfo("Congratulations!", f"You've guessed the word: {self.secret_word}\nFinal Score: {self.score}")
            self.end_game()
        elif self.attempts_left <= 0:
            messagebox.showinfo("Game Over", f"You've run out of attempts. The word was: {self.secret_word}\nFinal Score: {self.score}")
            self.end_game()

    def end_game(self):
        """
        End the game and disable the guess button.
        """
        self.guess_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)

    def restart_game(self):
        """
        Restart the game with the same category and difficulty.
        """
        self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGUI(root)
    root.mainloop()