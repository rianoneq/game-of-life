class Cell:
    def __init__(self, alive: bool = False):
        self.alive = alive

    def __mul__(self, n):
        if not isinstance(n, int):
            return NotImplemented
        return [Cell(self.alive) for _ in range(n)]

    def __rmul__(self, n):
        return self.__mul__(n)

    def __int__(self):
        return int(self.alive)

    def __bool__(self):
        return self.alive

    def __radd__(self, other):
        return int(self) + other

    def __add__(self, other):
        return int(self) + other

    def __repr__(self):
        return str(int(self.alive))

    __str__ = __repr__


class Board:
    def __init__(self, pattern: list[str] | None = None):
        if pattern is None:
            # дефолт: блок + блинкер (вечная конфигурация)
            pattern = [
                "........",
                "..##....",
                "..##....",
                "........",
                "...###..",
                "........",
                "........",
                "........",
            ]
        widths = {len(row) for row in pattern}
        if len(widths) > 1:
            raise ValueError(f"Строки разной длины: {widths}")
        self.cells = [
            [Cell(ch in ('#', '1')) for ch in row]
            for row in pattern
        ]

    @property
    def rows(self) -> int:
        return len(self.cells)

    @property
    def cols(self) -> int:
        return len(self.cells[0]) if self.cells else 0

    def __str__(self):
        return '\n'.join(' '.join(map(str, row)) for row in self.cells)

    def __repr__(self):
        return f'Board({self.cells!r})'


class Game:
    def __init__(self, board: Board | None = None):
        self.generation = 0
        self.board = board if board is not None else Board()

    def count_neighbours(self, r: int, c: int) -> int:
        """Соседи клетки (r,c) по СТАРОМУ полю. Модель — ТОР (заворот)."""
        cells = self.board.cells
        rows, cols = self.board.rows, self.board.cols
        n = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr = (r + dr) % rows
                nc = (c + dc) % cols
                n += int(cells[nr][nc])
        return n

    def next_generation(self):
        cells = self.board.cells
        rows, cols = self.board.rows, self.board.cols
        new_cells = [[Cell() for _ in range(cols)] for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                n = self.count_neighbours(r, c)
                alive = cells[r][c].alive
                new_cells[r][c].alive = (n == 3) or (alive and n == 2)

        self.board.cells = new_cells
        self.generation += 1
        return self


def random_pattern(rows: int = 40, cols: int = 40,
                   density: float = 0.3, seed: int = 42) -> list[str]:
    """Псевдослучайное поле. Воспроизводимо при фиксированном seed."""
    import random
    rng = random.Random(seed)
    random.randint
    return [
        ''.join('#' if rng.random() < density else '.' for _ in range(cols))
        for _ in range(rows)
    ]


if __name__ == "__main__":
    game = Game(Board(random_pattern(20, 20, 0.3)))
    print("Старт:")
    print(game.board)
    print()

    for _ in range(10):
        game.next_generation()
        print(f"Поколение {game.generation}:")
        print(game.board)
        print()
