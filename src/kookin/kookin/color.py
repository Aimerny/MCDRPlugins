
# === Color Format ===
def get_color(color: str) -> str:
    if color == 'black':
        return '§0'
    elif color == 'dark_blue':
        return '§1'
    elif color == 'dark_green':
        return '§2'
    elif color == 'dark_aqua':
        return '§3'
    elif color == 'dark_red':
        return '§4'
    elif color == 'dark_purple':
        return '§5'
    elif color == 'gold':
        return '§6'
    elif color == 'gray':
        return '§7'
    elif color == 'dark_gray':
        return '§8'
    elif color == 'blue':
        return '§9'
    elif color == 'green':
        return '§a'
    elif color == 'aqua':
        return '§b'
    elif color == 'red':
        return '§c'
    elif color == 'light_purple':
        return '§d'
    elif color == 'yellow':
        return '§e'
    elif color == 'white':
        return '§f'


def format_black() -> str:
    return get_color('black')


def format_dark_blue() -> str:
    return get_color('dark_blue')


def format_dark_green() -> str:
    return get_color('dark_green')


def format_dark_aqua() -> str:
    return get_color('dark_aqua')


def format_dark_red() -> str:
    return get_color('dark_red')


def format_dark_purple() -> str:
    return get_color('dark_purple')


def format_gold() -> str:
    return get_color('gold')


def format_gray() -> str:
    return get_color('gray')


def format_dark_gray() -> str:
    return get_color('dark_gray')


def format_blue() -> str:
    return get_color('blue')


def format_green() -> str:
    return get_color('green')


def format_aqua() -> str:
    return get_color('aqua')


def format_red() -> str:
    return get_color('red')


def format_light_purple() -> str:
    return get_color('light_purple')


def format_yellow() -> str:
    return get_color('yellow')


def format_white() -> str:
    return get_color('white')
