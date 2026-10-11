import random

# Глобальные переменные
WORDS_FILE = "words.txt"
GALLOWS_STAGES = [
    """
     ------
     |    |
     |
     |
     |
     |
    ---
    """,
    """
     ------
     |    |
     |    O
     |
     |
     |
    ---
    """,
    """
     ------
     |    |
     |    O
     |    |
     |
     |
    ---
    """,
    """
     ------
     |    |
     |    O
     |   /|
     |
     |
    ---
    """,
    """
     ------
     |    |
     |    O
     |   /|\
     |
     |
    ---
    """,
    """
     ------
     |    |
     |    O
     |   /|\
     |   /
     |
    ---
    """,
    """
     ------
     |    |
     |    O
     |   /|\
     |   / \
     |
    ---
    """
]
MAX_ATTEMPTS = len(GALLOWS_STAGES) - 1

def load_words():
    with open(WORDS_FILE, encoding='utf-8') as f:
        return [line.strip().split(';') for line in f]

def select_random_word():
    words = load_words()
    return random.choice(words)

def initialize_game():
    word, description = select_random_word()
    hidden_word = ['_' for _ in word]
    return {
        'word': word.upper(),
        'description': description,
        'hidden_word': hidden_word,
        'attempts_left': MAX_ATTEMPTS,
        'used_letters': set(),
        'game_over': False,
        'won': False
    }

def display_game_state(game_state):
    print(GALLOWS_STAGES[MAX_ATTEMPTS - game_state['attempts_left']])
    print(f"Описание: {game_state['description']}")
    print("Слово:", " ".join(game_state['hidden_word']))
    print("Использованные буквы:", " ".join(sorted(game_state['used_letters'])))
    print(f"Осталось попыток: {game_state['attempts_left']}")

def process_guess(game_state, letter):
    letter = letter.upper()
    if letter in game_state['used_letters']:
        print("Вы уже вводили эту букву!")
        return game_state
    
    game_state['used_letters'].add(letter)
    
    if letter in game_state['word']:
        for i, char in enumerate(game_state['word']):
            if char == letter:
                game_state['hidden_word'][i] = letter
    else:
        game_state['attempts_left'] -= 1
        print("Такой буквы нет в слове!")
    
    if '_' not in game_state['hidden_word']:
        game_state['game_over'] = True
        game_state['won'] = True
    elif game_state['attempts_left'] <= 0:
        game_state['game_over'] = True
    
    return game_state

def get_user_input():
    while True:
        guess = input("Введите букву: ").upper()
        if len(guess) == 1 and guess.isalpha():
            return guess
        print("Пожалуйста, введите одну русскую букву!")

def show_result(game_state):
    if game_state['won']:
        print("Поздравляем! Вы угадали слово:", game_state['word'])
    else:
        print("Игра окончена! Вы проиграли.")
        print("Загаданное слово было:", game_state['word'])

def play_game():
    while True:
        game_state = initialize_game()
        
        while not game_state['game_over']:
            display_game_state(game_state)
            guess = get_user_input()
            game_state = process_guess(game_state, guess)
        
        display_game_state(game_state)
        show_result(game_state)
        
        play_again = input("Хотите сыграть ещё раз? (да/нет): ").lower()
        if play_again != 'да':
            print("Спасибо за игру! До свидания!")
            break
