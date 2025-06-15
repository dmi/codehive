from pygame_emojis import load_emoji

emoji_cache = {}

def get_emoji(char, size=(32, 32)):
    if char not in emoji_cache:
        emoji_cache[char] = load_emoji(char, size)
    return emoji_cache[char]