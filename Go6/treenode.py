class TreeNode(object):
    """A node in the MCTS tree.
    """
    version = 0.1
    name = "MCTS Player"
    def __init__(self, parent, includePass=True):
        """
        parent is set when a node gets expanded
        """
        self._parent = parent
        self._children = {}  # a map from move to TreeNode
        self._n_visits = 0
        self._black_wins = 0
        self._expanded = False
        self._move = None
        self._prob_simple_feature = 1.0
        self.includePass = includePass

    def expand(self, board, color):
        if self.includePass:
            return self.expand_with_pass(board, color)
        else:
            return self.expand_without_pass(board, color)
    def expand_without_pass(self, board, color):
        """Expands tree by creating new children.
        """
        gammas_sum = 0.0
        moves = board.get_empty_points()
        all_board_features = Feature.find_all_features(board)
        for move in moves:
            if move not in self._children:
                if board.check_legal(move, color) and not board.is_eye(move, color):
                    self._children[move] = TreeNode(self)
                    self._children[move]._move = move
                    if len(Features_weight) != 0:
                        # when we have features weight, use that to compute knowledge (gamma) of each move
                        assert move in all_board_features
                        self._children[move]._prob_simple_feature = Feature.compute_move_gamma(Features_weight, all_board_features[move])
                        gammas_sum += self._children[move]._prob_simple_feature
        
        # Normalize to get probability
        if len(Features_weight) != 0 and gammas_sum != 0.0:
            for move in moves:
                if move in self._children:
                    if board.check_legal(move, color) and not board.is_eye(move, color):
                        self._children[move]._prob_simple_feature = self._children[move]._prob_simple_feature / gammas_sum
        
        self._expanded = True
        
    def expand_with_pass(self, board, color):
        """Expands tree by creating new children.
        """
        gammas_sum = 0.0
        moves = board.get_empty_points()
        all_board_features = Feature.find_all_features(board)
        for move in moves:
            if move not in self._children:
                if board.check_legal(move, color) and not board.is_eye(move, color):
                    self._children[move] = TreeNode(self)
                    self._children[move]._move = move
                    if len(Features_weight) != 0:
                        # when we have features weight, use that to compute knowledge (gamma) of each move
                        assert move in all_board_features
                        self._children[move]._prob_simple_feature = Feature.compute_move_gamma(Features_weight, all_board_features[move])
                        gammas_sum += self._children[move]._prob_simple_feature

        self._children[PASS] = TreeNode(self)
        self._children[PASS]._move = move
        
        # when we have features weight, use that to compute knowledge (gamma) of each move
        if len(Features_weight) != 0:
            self._children[PASS]._prob_simple_feature = Feature.compute_move_gamma(Features_weight, all_board_features["PASS"])
            gammas_sum += self._children[PASS]._prob_simple_feature
        
        # Normalize to get probability
        if len(Features_weight) != 0 and gammas_sum != 0.0:
            for move in moves:
                if move not in self._children:
                    if board.check_legal(move, color) and not board.is_eye(move, color):
                        self._children[move]._prob_simple_feature = self._children[move]._prob_simple_feature / gammas_sum
            self._children[PASS]._prob_simple_feature = self._children[PASS]._prob_simple_feature / gammas_sum
        self._expanded = True

    def select(self, exploration, max_flag):
        """Select move among children that gives maximizes UCT. 
        If number of visits are zero for a node, value for that node is infinity so definitely will  gets selected

        It uses: argmax(child_num_black_wins/child_num_vists + C * sqrt(2 * ln * Parent_num_vists/child_num_visits) )
        Returns:
        A tuple of (move, next_node)
        """
        return max(self._children.items(), key=lambda items:uct_val(self, items[1], exploration, max_flag))

    def update(self, leaf_value):
        """Update node values from leaf evaluation.
        Arguments:
        leaf_value -- the value of subtree evaluation from the current player's perspective.
        
        Returns:
        None
        """
        self._black_wins += leaf_value
        self._n_visits += 1

    def update_recursive(self, leaf_value):
        """Like a call to update(), but applied recursively for all ancestors.

        Note: it is important that this happens from the root downward so that 'parent' visit
        counts are correct.
        """
        # If it is not root, this node's parent should be updated first.
        if self._parent:
            self._parent.update_recursive(leaf_value)
        self.update(leaf_value)


    def is_leaf(self):
        """Check if leaf node (i.e. no nodes below this have been expanded).
        """
        return self._children == {}

    def is_root(self):
        return self._parent is None
