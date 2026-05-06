from pygame import Rect
from .entities.coin import Coin

# Platforms and simple world helpers

def default_platforms(WORLD_WIDTH, WORLD_HEIGHT):
    base = WORLD_HEIGHT - 40
    return [
        Rect(0, WORLD_HEIGHT - 40, 700, 40),
        Rect(800, WORLD_HEIGHT - 100, 200, 20),
        Rect(1100, WORLD_HEIGHT - 200, 200, 20),
        Rect(1400, WORLD_HEIGHT - 300, 200, 20),
        Rect(1700, WORLD_HEIGHT - 400, 200, 20),
        Rect(2000, WORLD_HEIGHT - 500, 200, 20),
        Rect(2300, WORLD_HEIGHT - 600, 200, 20),
        Rect(2600, WORLD_HEIGHT - 40, 8000, 40),
    ]


def place_coins_on_platforms(platforms, random):
    """Return a list of Coin objects placed on the provided platforms.

    Usage: coins = place_coins_on_platforms(platforms, random)
    """
    coins = []
    for plat in platforms[1:]:
        for _ in range(random.randint(1, 2)):
            x = random.randint(plat.left + 10, plat.right - 30)
            y = plat.top - 25
            coins.append(Coin(x, y))
    return coins
