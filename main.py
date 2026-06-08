
class Puissance4:
    def __init__(self, nb_row=6, nb_col=12, win_cond=4, nb_token=42, board=None, player=1):
        self.nb_row = nb_row
        self.nb_col = nb_col
        self.win_cond = win_cond
        self.nb_token = nb_token
        if board is None:
            self.board = [[0 for _ in range(self.nb_col)] for _ in range(self.nb_row)]
        else:
            self.board = board
        self.player = player

    def actions(self):
        """return all possible/valid actions."""
        actions = []
        if self.nb_token <= 0:
            return actions
        for col_nb in range(self.nb_col):
            if self.board[0][col_nb] == 0:
                actions.append(col_nb)
        return actions

    def result(self, action):
        """return the new state of the game after applying a valid action on it."""
        result = Puissance4(nb_row=self.nb_row, nb_col=self.nb_col, win_cond=self.win_cond, board=[[value for value in row] for row in self.board])
        row_nb = self.nb_row - 1
        while self.board[row_nb][action] != 0:
            row_nb -= 1
        result.board[row_nb][action] = self.player
        result.player = -self.player
        result.nb_token = self.nb_token - 1
        return result

    def terminal_test(self):
        directions = [
            (0, 1),  # →
            (1, 0),  # ↓
            (1, 1),  # ↘
            (-1, 1)  # ↗
        ]

        for row in range(self.nb_row):
            for col in range(self.nb_col):

                player = self.board[row][col]
                if player == 0:
                    continue
                # Select a direction to explore
                for dr, dc in directions:

                    count = 1
                    r = row + dr
                    c = col + dc
                    # Follow the current direction while the tokens match and we stay inside the board
                    while (
                            0 <= r < self.nb_row
                            and 0 <= c < self.nb_col
                            and self.board[r][c] == player
                    ):
                        count += 1
                        if count >= self.win_cond:
                            return player
                        r += dr
                        c += dc

        if len(self.actions()) == 0:
            return 0

        return 2

    '''# TODO: I still do not really see what to do with this
    def utility(self, player):
        return self.terminal_test()*player'''

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

    def algo_decision(self, algo="minimax", max_depth=-1):
        best_action = alpha = beta = None
        best_value = float("inf")*(-self.player)
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
    print("Joueur contre Joueur : 1")
    print("Joueur contre IA : 2")
    game_mode = 0
    while game_mode not in [1, 2]:
        try:
            game_mode = int(input("Choisissez l'option 1 ou 2 : "))
        except ValueError:
            print("Veuillez entrer un nombre.")
            continue
        if game_mode not in [1, 2]:
            print("Option invalide.")
            continue
    print()

    first_player = 0
    if game_mode == 2:
        print("Joueur commence en premier : 1")
        print("IA commence en premier : 2")
        while first_player not in [1, 2]:
            try:
                first_player = int(input("Choisissez l'option 1 ou 2 : "))
            except ValueError:
                print("Veuillez entrer un nombre.")
                continue
            if first_player not in [1, 2]:
                print("Option invalide.")
                continue
        print()

    game = Puissance4()
    while game.terminal_test() == 2:

        print(game)
        print()

        if game.player == 1:
            print("Tour du joueur X")
        else:
            print("Tour du joueur O")

        if game_mode == 1 or (first_player == 1 and game.player == 1) or (first_player == 2 and game.player == -1):
            try:
                action = int(input("Choisissez une colonne : "))
            except ValueError:
                print("Veuillez entrer un nombre.")
                continue

            if action not in game.actions():
                print("Colonne invalide.")
                continue
        else:
            from time import time
            t1 = time()
            action = game.algo_decision(algo="alpha-beta", max_depth=6)
            t2 = time()
            print(f"\n--IA décision prise en {t2-t1:.2f} secondes--")

        print()
        if game.player == 1:
            print("Choix du joueur X", end="")
            if first_player == 2:
                print(" (IA)", end="")
        else:
            print("Choix du joueur O", end="")
            if first_player == 1:
                print(" (IA)", end="")
        print(" :", action)

        game = game.result(action)

        result = game.terminal_test()

        if result == 1:
            print(game)
            print("Victoire de X")
        elif result == -1:
            print(game)
            print("Victoire de O")
        elif result == 0:
            print(game)
            print("Match nul")
            if game.nb_token == 0:
                print("Plus de pions disponibles (42 pions max par partie)")
