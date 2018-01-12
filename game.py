
from board import *
from config import *
import time

class Game:
    def __init__(self, brd: Board):
        self.board = brd

    def restart(self):
        self.board.reset_board()

    def start_self_play(self, player, is_shown=0, temp=1e-3):
        """ start a self-play game using a MCTS player, reuse the search tree
            store the self-play data: (state, mcts_probs, z)
        """
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board, temp=temp, return_prob=1)
            if move is not None:
                # store the data
                states.append(self.board.current_state())
                mcts_probs.append(move_probs)
                current_players.append(self.board.tomove)
                # perform a move
                self.board.makemove(move)
                if is_shown:
                    self.board.print_table()
            else:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                # reset MCTS root node
                player.reset_player()
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, zip(states, mcts_probs, winners_z)

    def self_play(self):
        self.restart()
        while True:
            moves = self.board.genmove()
            if moves:
                move = moves[0]
                self.board.makemove(move)
                #self.board.print_table()
            else:
                winner = self.get_winner()
                print('Game over! winner: %d'%(winner))
                print('steps:%d'%(self.board.step))
                break

    def get_winner(self, step=None):
        if step is None:
            step = self.board.step
        if self.board.full_board(step):
            b_count = self.board.states[step][BLACK].count(True)
            w_count = self.board.states[step][WHITE].count(True)
            if b_count > w_count:
                return BLACK
            elif b_count < w_count:
                return WHITE
            else:
                return -1
        else:
            return 1 - self.board.tomove

    def start_play(self, player1, player2, start_player=0, is_shown=1):
        """
            start a game between two players
        """
        if start_player not in (0, 1):
            raise Exception('start_player should be 0 (Black first) or 1 (White first)')
        self.board.reset_board(start_player)
        p1, p2 = self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2: player2}
        if is_shown:
            self.board.print_table()
        while True:
            current_player = self.board.tomove
            player_in_turn = players[current_player]
            move = player_in_turn.get_action(self.board)
            if move is not None:
                self.board.makemove(move)
                if is_shown:
                    self.board.print_table()
            else:
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is", players[winner])
                    else:
                        print("Game end. Tie")
                return winner

if __name__ == '__main__':
    test = Game()
    test.self_play()


