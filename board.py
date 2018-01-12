from config import *
from bitarray import bitarray
import copy



near_area = [bitarray('0' * 49)] * 49
far_area = [bitarray('0' * 49)] * 49
dx = [-1,-1,-1,0,0,1,1,1,-2,-2,-2,-2,-2,-1,-1,0,0,1,1,2,2,2,2,2]
dy = [-1,0,1,-1,1,-1,0,1,-2,-1,0,1,2,-2,2,-2,2,-2,2,-2,-1,0,1,2]
move_to_vertex = {}
vertex_to_move = {}

num = 0


def init_map():
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            for i in range(24):
                tempx = x + dx[i]
                tempy = y + dy[i]
                if 0 <= tempx < BOARD_SIZE and 0 <= tempy < BOARD_SIZE:
                    global num, move_to_vertex, vertex_to_move
                    fm = x * BOARD_SIZE + y
                    to = tempx * BOARD_SIZE + tempy
                    move_to_vertex[(fm, to)] = num
                    vertex_to_move[num] = (fm, to)
                    num += 1


def vertex_to_move_fn(vertexs):
    ret = []
    for vertex in vertexs:
        ret.append(vertex_to_move[vertex])
    return ret

class Board:
    def __init__(self):
        self.states = [[bitarray('0'*49), bitarray('0'*49)]]
        self.step = 0
        self.tomove = BLACK
        self.players = [BLACK, WHITE]  # player Black and player White
        init_map()
        self.init_area()
        self.reset_board()

    def get_availables(self, color=None, step=None):
        if color is None:
            color = self.tomove
        if step is None:
            step = self.step
        moves = self.genmove(color, step)
        ret = []
        for var in moves:
            ret.append(move_to_vertex[var])
        return ret

    def reset_board(self, start_player=0):
        self.step = 0
        self.tomove = BLACK
        self.states[0][BLACK][0] = '1'
        self.states[0][BLACK][48] = '1'
        self.states[0][WHITE][6] = '1'
        self.states[0][WHITE][42] = '1'
        self.tomove = self.players[start_player]  # start player

    def full_board(self, step=None):
        if step is None:
            step = self.step
        return (self.states[step][BLACK] | self.states[step][WHITE]).all()

    def procstep(self, move, step=None, color=None):
        if step is None:
            step = self.step
        if color is None:
            color = self.tomove
        mystate = copy.deepcopy(self.states[step][color])
        opstate = copy.deepcopy(self.states[step][1-color])

        fm = move[0]
        to = move[1]
        global far_area, near_area
        if far_area[fm][to]:
            mystate[fm] = False
        mystate[to] = True
        change = near_area[to] & opstate
        mystate |= change
        opstate ^= change
        if color is BLACK:
            self.states.append([opstate, mystate])
        else:
            self.states.append([mystate, opstate])

    def makemove(self, move, step=None, color=None):
        if step is None:
            step = self.step
        if color is None:
            color = self.tomove
        self.procstep(move, step, color)
        self.tomove = 1 - self.tomove
        self.step += 1

    def delmove(self):
        if self.step <= 0:
            return
        self.tomove = 1 - self.tomove
        self.step -= 1

    def inmap(self, x, y):
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

    def genmove(self, color=None, step=None):
        if color is None:
            color = self.tomove
        if step is None:
            step = self.step
        blank_pos = self.get_blank_pos()
        move = []
        for to in blank_pos:
            global near_area, far_area
            nearto = near_area[to] & self.states[step][color]
            nearto_pos = self.get_bitarray_pos(nearto)
            if nearto_pos:
                move.append((nearto_pos[0], to))
            farto = far_area[to] & self.states[step][color]
            farto_pos = self.get_bitarray_pos(farto)
            for frm in farto_pos:
                move.append((frm, to))
        return move

    def get_bitarray_pos(self, bitmask):
        ret = []
        while True:
            try:
                pos = bitmask.index(True)
                ret.append(pos)
                bitmask[pos] = False
            except ValueError:
                break
        return ret

    def mypopcount(self, color=None, step=None):
        if color is None:
            color = self.tomove
        if step is None:
            step = self.step
        return self.states[step][color].count(True)

    def get_number_pos(self, number):
        bitmask = self.number_to_bitarray(number)
        ret = []
        while True:
            try:
                pos = bitmask.index(True)
                ret.append(pos)
                bitmask[pos] = False
            except ValueError:
                break
        return ret

    def number_to_bitarray(self, number):
        return bitarray(str(bin(number))[2:][::-1])

    def get_blank_pos(self, step=None):
        if step is None:
            step = self.step
        blank = ~(self.states[step][BLACK] | self.states[step][WHITE])
        ret = []
        while True:
            try:
                pos = blank.index(True)
                ret.append(pos)
                blank[pos] = False
            except ValueError:
                break
        return ret

    def get_side_pos(self, color=None, step=None):
        if color is None:
            color = self.tomove
        if step is None:
            step = self.step
        state = self.states[step][color]
        ret = []
        while True:
            try:
                pos = state.index(True)
                ret.append(pos)
                state[pos] = False
            except ValueError:
                break
        return ret

    def init_area(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                global dx, dy
                temp = bitarray('0'*49)
                for i in range(8):
                    tempx = x + dx[i]
                    tempy = y + dy[i]
                    if self.inmap(tempx, tempy):
                        temp[tempx*BOARD_SIZE+tempy] = True
                global near_area
                near_area[x * BOARD_SIZE + y] = temp

                curr = bitarray('0'*49)
                for i in range(8, 24):
                    currx = x + dx[i]
                    curry = y + dy[i]
                    if self.inmap(currx, curry):
                        curr[currx*BOARD_SIZE+curry] = True
                global far_area
                far_area[x * BOARD_SIZE + y] = curr

    def check_pos(self, x, y, color=None, step=None):
        if color is None:
            color = self.tomove
        if step is None:
            step = self.step
        return self.states[step][color][x*BOARD_SIZE+y]

    def current_state(self):
        """
        return the board state from the perspective of the current player
        shape: 4*width*height
        """
        square_state = np.zeros((4, BOARD_SIZE, BOARD_SIZE))
        mypos = self.get_side_pos()
        oppos = self.get_side_pos(color=1-self.tomove)
        for pos in mypos:
            square_state[0][pos//BOARD_SIZE][pos%BOARD_SIZE] = 1.0
        for pos in oppos:
            square_state[1][pos//BOARD_SIZE][pos%BOARD_SIZE] = 1.0
        if self.tomove is BLACK:
            square_state[2][:, :] = 1.0
        else:
            square_state[3][:, :] = 1.0
        return square_state

    def print_table(self, step=None):
        if step is None:
            step = self.step
        _str = '  0 1 2 3 4 5 6\n'
        for x in range(BOARD_SIZE):
            _str += (str(x) + ' ')
            for y in range(BOARD_SIZE):
                if self.check_pos(x, y, BLACK, step):
                    _str += 'B '
                elif self.check_pos(x, y, WHITE, step):
                    _str += 'W '
                else:
                    _str += '  '
            _str += str(x)
            _str += '\n'
        _str += '  0 1 2 3 4 5 6\n'
        print(_str)

if __name__ == '__main__':
    init_map()
    print(num)
