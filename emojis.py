from pygame_emojis import load_emoji

emoji_cache = {}

def get_emoji(char, size=(32, 32)):
    key = f'{char} {size}'
    if key not in emoji_cache:
        emoji_cache[key] = load_emoji(char, size)
    return emoji_cache[key]