"""N-queens as a constraint-satisfaction problem; first-solution backtracking."""


def attacking_pairs(board):
    """board[row] is a column, or -1 for an empty row."""
    return [(a, b) for a in range(len(board)) for b in range(a + 1, len(board))
            if board[a] >= 0 and board[b] >= 0
            and (board[a] == board[b] or abs(board[a]-board[b]) == b-a)]


def solve(n=8):
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 10:
        raise ValueError('Choose an integer board size from 1 to 10.')
    board = [-1] * n
    columns, down, up = set(), set(), set()
    trace = []
    tested = backtracks = 0

    def record(action, row=None, col=None):
        trace.append(dict(board=board[:], action=action, row=row, col=col,
                          tested=tested, backtracks=backtracks))

    record('start')

    def visit(row):
        nonlocal tested, backtracks
        if row == n:
            record('solved')
            return True
        for col in range(n):
            tested += 1
            if col in columns or row-col in down or row+col in up:
                record('reject', row, col)
                continue
            board[row] = col
            columns.add(col); down.add(row-col); up.add(row+col)
            record('place', row, col)
            if visit(row+1):
                return True
            columns.remove(col); down.remove(row-col); up.remove(row+col)
            board[row] = -1
            backtracks += 1
            record('remove', row, col)
        return False

    solved = visit(0)
    if not solved:
        record('unsolved')
    return dict(n=n, solved=solved, trace=trace)
