# from classes.player import Player
import copy
from random import choice, randint
from classes.player import Player

MAX_SCORE = 999999
MIN_SCORE = -999999


class Graph():
 
    def __init__(self, vertices, graph):
        self.V = vertices
        self.graph = graph
        
    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])
 
    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet): 
        # Initialize minimum distance for next node
        min = 1e7
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):
 
        dist = [1e7] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)
 
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                   sptSet[v] == False and
                   dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]
 
        self.printSolution(dist)


class MinimaxPlayer(Player):
    def __init__(self, logic, ui, board_state, color, max_depth):
        super().__init__(logic, ui, color)
        self.root_state = copy.deepcopy(board_state)
        self.max_depth = max_depth
        self.players = [1, 2]
        self.players.remove(self.color)
        self.other_player = self.players[0]
        self.turn = {True: self.color, False: self.other_player}
        self.turn_state = True

    def eval_fn(self, color):
        """Evaluate board using a randomly generated number

        Returns:
            int: Assigned board score
        """
        # self.eval_count += 1
        return randint(0,self.ui.board_size*2) 
    
    def alpha_beta_result(self, board_state, max_depth, alpha, beta, maximizingPlayer): 
        # if board_state.is_over():                                   
        #     if board_state.winner() == board_state.next_player:      
        #         return MAX_SCORE                                   
        #     else:                                                  
        #         return MIN_SCORE                                   
        
        self.logic.is_over(board_state, False)
        if max_depth == 0 or self.logic.GAME_OVER:                                         
            return self.eval_fn(board_state)                             
        
        if maximizingPlayer:
            max_eval = MIN_SCORE
            for candidate_move in self.logic.get_possible_moves(board_state):  
                state = copy.deepcopy(board_state)          
                x,y = candidate_move
                state[x][y] = self.color
                opponent_best_result = self.alpha_beta_result(              
                    state, max_depth - 1,                         
                    alpha, beta, False)
                max_eval = max(alpha, opponent_best_result)  
                if beta <= alpha:
                    break
            return max_eval
        
        else:
            min_eval = MAX_SCORE
            for candidate_move in self.logic.get_possible_moves(board_state):    
                state = copy.deepcopy(self.root_state)        
                x,y = candidate_move
                state[x][y] = self.other_player
                our_best_result = self.alpha_beta_result(              
                    state, max_depth - 1,                         
                    alpha, beta, True)
                min_eval = min(beta, our_best_result)  
                if beta <= alpha:
                    break
            return min_eval

    def select_move(self, node):
        #select the best move
        best_moves = []
        best_score = MIN_SCORE
        alpha = MIN_SCORE
        beta = MAX_SCORE
        maximizingPlayer = True
        print("possible moves ", self.logic.get_possible_moves(self.root_state))
        # Loop over all legal moves.
        for possible_move in self.logic.get_possible_moves(self.root_state):
            state = copy.deepcopy(self.root_state)
            # Calculate the game state if we select this move.
            x,y = possible_move
            state[x][y] = self.turn[self.turn_state]
            # next_state = board_state.apply_move(possible_move)
            # Since our opponent plays next, figure out their best
            # possible outcome from there.
            our_best_outcome = self.alpha_beta_result(
                state, self.max_depth,
                alpha, beta, maximizingPlayer)
            # Our outcome is the opposite of our opponent's outcome.
            if (not best_moves) or our_best_outcome > best_score:
                # This is the best move so far.
                best_moves = [possible_move]
                best_score = our_best_outcome
            elif our_best_outcome == best_score:
                # This is as good as our previous best move.
                best_moves.append(possible_move)
        # For variety, randomly select among all equally good moves.
        return choice(best_moves)
    

