quadrant = [
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (0, 2), (1, 3)],
    [(0, 0), (0, 1), (1, 2), (1, 3)],
    [(0, 0), (1, 1), (1, 2), (1, 3)],
    [(0, 0), (1, 1), (1, 2), (2, 3)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 0), (1, 1), (2, 1), (3, 2)],
    [(0, 0), (1, 1), (2, 1), (3, 1)],
    [(0, 0), (1, 0), (2, 1), (3, 1)],
    [(0, 0), (1, 0), (2, 0), (3, 1)],
]

sight_lines = []
for line in quadrant:
    for i in range(4):
        sight_lines.append(line)
        line = [(p[1], -p[0]) for p in line]
