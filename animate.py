import matplotlib.pyplot as plt
import matplotlib.animation as animation

from main import Game, Board, random_pattern


# ---------- ВЫБЕРИТЕ ПАТТЕРН ----------

# 1) случайный хаос 40×40 (тор — идеально для него)
PATTERN = random_pattern(40, 40, density=0.3, seed=42)

# 2) или готовый «зоопарк» 20×20
# PATTERN = [
#     "....................",
#     "..#...........#.....",
#     "...#.........#......",
#     ".###.........#......",
#     "............###.....",
#     "....................",
#     "....##..............",
#     "....##..............",
#     "....................",
#     ".........###........",
#     ".........###........",
#     ".........###........",
#     "....................",
#     "...........#........",
#     "..........#.#.......",
#     "..........#.#.......",
#     "...........#........",
#     "....................",
#     "..##..........##....",
#     "..##..........##....",
# ]

# 3) или один глайдер на маленьком торе — летает по кругу вечно
# PATTERN = [
#     "............",
#     ".#..........",
#     "..#.........",
#     "###.........",
#     "............",
#     "............",
#     "............",
#     "............",
#     "............",
#     "............",
#     "............",
#     "............",
# ]

# --------------------------------------

game = Game(Board(PATTERN))

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title("Game of Life — тор")
ax.set_xticks([])
ax.set_yticks([])

img = ax.imshow(
    [[int(cell.alive) for cell in row] for row in game.board.cells],
    cmap='binary',
    interpolation='nearest',
)

gen_text = ax.text(
    0.02, 1.02, "Поколение 0",
    transform=ax.transAxes, fontsize=10, va='bottom',
)


def update(frame):
    game.next_generation()
    img.set_data([[int(cell.alive) for cell in row] for row in game.board.cells])
    gen_text.set_text(f"Поколение {game.generation}")
    return img, gen_text


ani = animation.FuncAnimation(
    fig, update,
    interval=80,           # мс между кадрами
    blit=False,
    cache_frame_data=False,
)

plt.tight_layout()
plt.show()
