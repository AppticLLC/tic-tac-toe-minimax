""" A tic-tac-toe solver using minimax (without alpha-beta pruning). 

Example usage:
>>> game = GameTree()
>>> game.run_minimax_game()
"""

class GameTree:
    # A list to switch between players
    players = ["X", "O"]

    def __init__(self, value="         ", player_number=0):
        self.value = value
        self.children = []
        self.player_number = player_number
        self.generate_children()

    def print_tree(self):
        """ Print in a user-friendly way. """
        t = self.value
        print(t[0] + " | " + t[1] + " | " + t[2])
        print("---------")
        print(t[3] + " | " + t[4] + " | " + t[5])
        print("---------")
        print(t[6] + " | " + t[7] + " | " + t[8])

    def generate_children(self):
        """ Generate the children of this node. """
        if self.is_win(self.player_number) or self.is_win((self.player_number + 1) % 2) or " " not in self.value:
            return
        children_indices = [position[0] for position in enumerate(self.value) if position[1] == " "]
        child_trees = []
        for i in children_indices:
            child_tree = GameTree(self.value[:i] + GameTree.players[self.player_number] + self.value[i+1:], (self.player_number + 1) % 2)
            child_trees.append(child_tree)
        self.children = child_trees

    def is_win(self, player_number):
        """ Determine if the player has won the game. """
        player = GameTree.players[player_number]
        t = self.value
        return any([(t[3 * i] == player and t[3 * i + 1] == player and t[3 * i + 2] == player) for i in range(3)]) or \
            any([(t[i] == player and t[i + 3] == player and t[i + 6] == player) for i in range(3)]) or \
            (t[0] == player and t[4] == player and t[8] == player) or (t[2] == player and t[4] == player and t[6] == player)

    def probability_of_winning(self, player_number):
        """ Give the probability of player winning this game. """
        if self.is_win(player_number):
            return 1
        elif self.is_win((self.player_number + 1) % 2):
            return 0
        elif " " not in self.value:
            return .5
        return sum([child.probability_of_winning(player_number) for child in self.children]) / len(self.children)

    def minimax(self, depth=2):
        """ Run minimax with the current player as max. Decrement the depth for each
        minimizer. Return the appropriate child tree. """

        def maximize(tree, depth):
            # Return the maximum of all child minimizer values.
            if len(tree.children) == 0:
                return (tree.value, tree.probability_of_winning(self.player_number))
            child_values = [minimize(child, depth - 1) for child in tree.children]
            return (tree.value, max(child_values, key=lambda k: k[1])[1])

        def minimize(tree, depth):
            # Return the minimum of all child maximizer values.
            if depth == 0 or len(tree.children) == 0:
                return (tree.value, tree.probability_of_winning(self.player_number))
            child_values = [maximize(child, depth) for child in tree.children]
            return (tree.value, min(child_values, key=lambda k: k[1])[1])

        child_values = [minimize(child, depth) for child in self.children]
        child_index = max(enumerate(child_values), key=lambda k: k[1][1])[0]
        return self.children[child_index]

    def move_by_probability(self):
        """ Return the move that maximizes the probability of winning. """
        children_with_probabilities = [(child, child.probability_of_winning(self.player_number)) for child in self.children]
        return max(children_with_probabilities, key=lambda k: k[1])[0]

    def run_game_with_algorithm(self, tree_function):
        """ Automatically execute a game with a move selection function that takes a tree, and returns a child tree. """
        tree = self
        move = 0
        while not tree.is_win(self.player_number) and not tree.is_win((self.player_number + 1) % 2) and " " in tree.value:
            print("Move number: " + str(move))
            tree.print_tree()
            tree = tree_function(tree)
            move += 1
        print("Move number: " + str(move))
        tree.print_tree()

    def run_minimax_game(self, depth=2):
        """ Automatically execute a minimax game. """
        self.run_game_with_algorithm(lambda t: t.minimax(depth))

    def run_probability_game(self, depth=2):
        """ Automatically execute a game where each player maximizes the probability of winning. """
        self.run_game_with_algorithm(GameTree.move_by_probability)