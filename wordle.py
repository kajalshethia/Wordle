import random

# Function to load words from a file
def load_words(filename):
    ## Reads words from a text file and returns them as a list
    try:
        with open(filename, 'r') as file:
            words = [line.strip().lower() for line in file if len(line.strip()) == 5 and line.strip().isalpha()]
        return words
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []

def get_feedback(secret_word, guess):
    ## Provides feedback for a guessed word against the secret word
    feedback = ["🟪"] * len(guess)
    secret_word_list = list(secret_word)
    
    # Check correct positions first (Green)
    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            feedback[i] = '🟩'
            secret_word_list[i] = None  # Remove matched letters

    # Check misplaced letters (Yellow)
    for i in range(len(guess)):
        if feedback[i] == '🟪' and guess[i] in secret_word_list:
            feedback[i] = '🟨'
            secret_word_list[secret_word_list.index(guess[i])] = None

    return "".join(feedback)

def update_letter_status(guess, secret_word, letter_status):
    ## Updates the dictionary to track used letters and their status
    for letter in guess:
        if letter in secret_word:
            if guess.count(letter) <= secret_word.count(letter):
                letter_status[letter] = "🟨" if guess.index(letter) != secret_word.index(letter) else "🟩"
        else:
            letter_status[letter] = "🟪"
    return letter_status

def display_letter_status(letter_status):
    ## Displays the letter status in an organized format
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    output = "Used letters: "
    for letter in alphabet:
        if letter in letter_status:
            output += f"{letter.upper()}({letter_status[letter]}) "
        else:
            output += f"{letter.upper()}(_) "
    print(output)

def wordle_game():
    words = load_words('five-letter-words.txt')
    if not words:
        print("No valid words found. Please check the five-letter-words.txt file.")
        return

    secret_word = random.choice(words)
    attempts = 6
    letter_status = {}

    print("Welcome to Wordle!")
    print("Guess the 5-letter word. You have 6 attempts.\n")

    while attempts > 0:
        guess = input("Enter your 5-letter guess: ").lower()

        if len(guess) != 5 or not guess.isalpha():
            print("Please enter a valid 5-letter word.")
            continue

        feedback = get_feedback(secret_word, guess)
        letter_status = update_letter_status(guess, secret_word, letter_status)
        
        print(f"Feedback: {feedback}")
        display_letter_status(letter_status)

        if guess == secret_word:
            print("🎉 Congratulations! You've guessed the word correctly!")
            break

        attempts -= 1
        print(f"You have {attempts} attempts left.\n")

    if attempts == 0:
        print(f"Game Over! The correct word was: {secret_word}")

if __name__ == "__main__":
    wordle_game()
