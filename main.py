# TODO: check I did not make any mistake in what I did (j'avais pas trop le temps de vérifier)
class Puissance4:
    def __init__(self, nb_col=12, nb_row=6, win_cond=4, nb_token=42, board=None, player=1):
        self.nb_col = nb_col
        self.nb_row = nb_row
        self.win_cond = win_cond
        self.nb_token = nb_token
        self.player = player
        if board is None:
            self.board = [[0]*self.nb_col]*self.nb_row
        else:
            self.board = board

    def actions(self):
        actions = []
        if self.nb_token <= 0:
            return actions
        for col_nb in range(self.nb_col):
            row_nb = self.nb_row
            while row_nb >= 0 and self.board[row_nb][col_nb] != 0:
                row_nb -= 1
            if row_nb >= 0:
                actions.append(row_nb)
        return actions

    def result(self, action):
        result = Puissance4(nb_col=self.nb_col, nb_row=self.nb_row, win_cond=self.win_cond, board=[[value for value in row] for row in self.board])
        row_nb = self.nb_row
        while self.board[row_nb][action] != 0:
            row_nb -= 1
        result.board[row_nb][action] = self.player
        result.player = -self.player
        result.nb_token = self.nb_token - 1
        return result

    # TODO: diagonal and improve the way row and col are computed (it works right now but it checks way to many things)
    def terminal_test(self):
        col_values = [0]*self.nb_col
        for row_nb in range(self.nb_row):
            row_value = 0
            for col_nb in range(self.nb_col):
                if row_value == 0:
                    row_value = self.board[row_nb][col_nb]
                elif row_value/abs(row_value) == self.board[row_nb][col_nb]:
                    row_value += self.board[row_nb][col_nb]
                else:
                    row_value = self.board[row_nb][col_nb]

                if row_value >= self.win_cond:
                    return 1
                elif row_value <= -self.win_cond:
                    return -1

                if col_values[col_nb] == 0:
                    col_values[col_nb] = self.board[row_nb][col_nb]
                elif col_values[col_nb]/abs(col_values[col_nb]) == self.board[row_nb][col_nb]:
                    col_values[col_nb] += self.board[row_nb][col_nb]
                else:
                    col_values[col_nb] = self.board[row_nb][col_nb]

        for col_value in col_values:
            if col_value >= self.win_cond:
                return 1
            elif col_value <= -self.win_cond:
                return -1

        diag_values = [0, 0]
        for diag_nb in range(self.nb_row):
            diag_values[0] += self.board[diag_nb][diag_nb]
            diag_values[1] += self.board[diag_nb][-(diag_nb + 1)]
        if self.win_cond in diag_values:
            return 1
        elif -self.win_cond in diag_values:
            return -1

        if len(self.actions()) == 0:
            return 0
        return 2  # TODO: maybe evaluate unfinished board here?

    # TODO: I still do not really see what to do with this
    def utility(self, player):
        return self.terminal_test()*player

    def __str__(self):
        puissance4_str = ""
        for row_nb in range(self.nb_row):
            for col_nb in range(self.nb_col):
                puissance4_str += "|"
                if self.board[row_nb][col_nb] == 0:
                    puissance4_str += " "
                elif self.board[row_nb][col_nb] == 1:
                    puissance4_str += "X"
                else:
                    puissance4_str += "O"
            puissance4_str += "|\n"
        puissance4_str += "-"*self.nb_col*2 + "-\n"
        for col_nb in range(self.nb_col):
            puissance4_str += "|" + str(col_nb%10)
        puissance4_str += "|"
        return puissance4_str

    # TODO: Not sure if there actually is anything to change here
    def algo_decision(self, algo="minimax", max_depth=-1):
        best_action = None
        best_value = float("inf")*(-self.player)
        alpha = None
        beta = None
        if algo == "alpha-beta":
            alpha = -float("inf")
            beta = float("inf")
        for action in self.actions():
            value = self.result(action).decision_value(alpha, beta, max_depth)
            if self.player > 0:
                if value > best_value:
                    best_value = value
                    best_action = action
                    if algo == "alpha-beta":
                        alpha = max(alpha, best_value)
            elif value < best_value:
                best_value = value
                best_action = action
                if algo == "alpha-beta":
                    beta = min(beta, best_value)
        return best_action

    # TODO: Not sure if there actually is anything to change here again except for the max_depth part
    def decision_value(self, alpha, beta, max_depth):
        terminal_state = self.terminal_test()
        if terminal_state != 2:
            return terminal_state
        if max_depth == 0:
            return 0
        value = float("inf")*(-self.player)
        for action in self.actions():
            if self.player > 0:
                value = max(value, self.result(action).decision_value(alpha, beta, max_depth - 1))
                if alpha is not None:
                    if value >= beta:
                        return value
                    alpha = max(alpha, value)
            else:
                value = min(value, self.result(action).decision_value(alpha, beta, max_depth - 1))
                if beta is not None:
                    if value <= alpha:
                        return value
                    beta = min(beta, value)
        return value


if __name__ == '__main__':
    puissance4 = Puissance4()
    print(puissance4)
