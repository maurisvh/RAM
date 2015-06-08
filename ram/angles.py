def rot0(p):   x, y = p; return x, y
def rot90(p):  x, y = p; return y, -x
def rot180(p): x, y = p; return -x, -y
def rot270(p): x, y = p; return -y, x

for t in (rot0, rot90, rot180, rot270):
    for mat in open('angles.txt').read().split('\n\n'):
        s = mat.replace('\n', '')
        assert len(s) == 16
        line = []
        # 0123
        # 4567
        # 89AB
        # CDEF
        order = [12, 8, 13, 4, 9, 14, 0, 5, 10, 15, 1, 6, 11, 2, 7, 3]
        for i in order:
            if s[i] == '#':
                x = i % 4
                y = 3 - i // 4
                line.append(t((x, y)))
        print(line)
