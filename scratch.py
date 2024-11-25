import random
from random_word import RandomWords
from PyDictionary import PyDictionary
from spellchecker import SpellChecker
from wordfreq import word_frequency

# Initialize the spell checker, PyDictionary, and RandomWords
spell = SpellChecker()
dictionary = PyDictionary()
random_words = RandomWords()

# Loop to find a random word with a valid definition
rarity = None
attempts = 0
max_attempts = 0
random_word = None
definition = None

# Select difficulty level
difficulty = input("Select difficulty from 1 to 3: ")
if difficulty == '3':
    difficulty = 3
    max_attempts = 2
elif difficulty == '2':
    difficulty = 2
    max_attempts = 4
else:
    difficulty = 1
    max_attempts = 7

# Find a random word with a valid definition and matching difficulty
while definition is None:
    # Generate a random word
    random_word = random_words.get_random_word()
    frequency = word_frequency(random_word, 'en')

    # Determine the rarity of the word
    if frequency > 0.001:
        rarity = "Common"
    elif frequency > 0.00001:
        rarity = "Uncommon"
    else:
        rarity = "Rare"

    # Skip the word if its rarity does not match the selected difficulty
    if (rarity == "Rare" and difficulty < 3) or (rarity == "Uncommon" and difficulty < 2):
        continue

    # Get the definition of the random word
    definition = dictionary.meaning(random_word)

# Explain the rules of the game
print("You must guess a randomly selected word based on its dictionary definition.")

# Print the definition of the found word
print("Definition:")
for part_of_speech, meanings in definition.items():
    print(f"{part_of_speech}: {', '.join(meanings)}")

# Function to check the user's guess
def check_guess(guess):
    # Correct the spelling of the guess
    guess = spell.correction(guess)
    # Get synonyms for the guess
    synonyms = dictionary.synonym(guess)

    # Check if the corrected guess matches the random word
    if guess == random_word:
        return True

    # Check if the corrected guess matches any of the synonyms
    if synonyms is not None:
        for word in synonyms:
            if word == random_word:
                return True
    return False

# Set the amount of allowed given letters for hints
amount_of_allowed_given_letters = 5

# Start the guessing game
while attempts < max_attempts:
    # Get user input
    user_input = input("Enter the word you think matches the definition: ")

    # Check the user's guess
    if check_guess(user_input):
        print("You win!")
        break
    else:
        attempts += 1
        print(f"Incorrect guess. You have {max_attempts - attempts} attempts left.")

        # Provide a hint if attempts are within the allowed number of given letters
        if attempts <= amount_of_allowed_given_letters:
            print(f"Hint: The word starts with '{random_word[:attempts]}'")

# If the user runs out of attempts
if attempts == max_attempts:
    print(f"You lose! The correct word was '{random_word}'.")
