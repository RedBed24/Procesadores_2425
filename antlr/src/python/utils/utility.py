KEY_WORDS = [
    "fragmento",
    "obra",
    "clave",
    "compas",
    "armadura",
    "lig",
    "DO", "RE", "MI", "FA", "SOL", "LA", "SI",
    "sf", "f", "sc", "c", "n", "bl", "r",
    "b",
]

def is_key_word(word: str) -> bool:
    return word.lower() in (key_word.lower() for key_word in KEY_WORDS)
