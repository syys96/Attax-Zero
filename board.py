from config import *
from bitarray import bitarray

class Board:
    def __init__(self):
        self.states = [[0, 0]]
        self.states = [[bitarray('0'*49), bitarray('0'*49)]]
        self.near_area = [bitarray('0'*49)]*49
        self.far_area = [bitarray('0'*49)]*49
        self.dx = [-1,-1,-1,0,0,1,1,1,-2,-2,-2,-2,-2,-1,-1,0,0,1,1,2,2,2,2,2]
        self.dy = [-1,0,1,-1,1,-1,0,1,-2,-1,0,1,2,-2,2,-2,2,-2,2,-2,-1,0,1,2]
        self.step = 0
        self.tomove = BLACK
        self.init_area()
        self.reset_board()

    def reset_board(self):
        self.step = 0
        self.tomove = BLACK
        self.states[0][BLACK][0] = '1'
        self.states[0][BLACK][48] = '1'
        self.states[0][WHITE][6] = '1'
        self.states[0][WHITE][42] = '1'


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
            nearto = self.near_area[to] & self.states[step][color]
            nearto_pos = self.get_bitarray_pos(nearto)
            if nearto_pos:
                move.append((nearto_pos[0], to))
            farto = self.far_area[to] & self.states[step][color]
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
        return bitarray(str(bin(number))[2:])

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
                temp = bitarray('0'*49)
                for i in range(8):
                    tempx = x + self.dx[i]
                    tempy = y + self.dy[i]
                    if self.inmap(tempx, tempy):
                        temp[tempx*BOARD_SIZE+tempy] = True
                self.near_area[x * BOARD_SIZE + y] = temp

                curr = bitarray('0'*49)
                for i in range(8, 24):
                    currx = x + self.dx[i]
                    curry = y + self.dy[i]
                    if self.inmap(currx, curry):
                        curr[currx*BOARD_SIZE+curry] = True
                self.far_area[x * BOARD_SIZE + y] = curr

    def check_pos(self, x, y, color=None, step=None):
        if color is None:
            color = self.tomove
        if step is None:
            step = self.step
        return self.states[step][color][x*BOARD_SIZE+y]

    def print_table(self, step=None):
        if step is None:
            step = self.step
        _str = '  0 1 2 3 4 5 6\n'
        for x in range(BOARD_SIZE):
            _str += (str(x) + ' ')
            for y in range(BOARD_SIZE):
                if self.check_pos(x, y, BLACK):
                    _str += 'B '
                elif self.check_pos(x, y, WHITE):
                    _str += 'W '
                else:
                    _str += '  '
            _str += str(x)
            _str += '\n'
        _str += '  0 1 2 3 4 5 6\n'
        print(_str)


if __name__ == '__main__':

    test = Board()
    test.print_table()
    """
    #print(test.genmove(color=WHITE))
    for pair in test.genmove(color=WHITE):
        action = []
        action.append((pair[0]//BOARD_SIZE, pair[0]%BOARD_SIZE))
        action.append((pair[1]//BOARD_SIZE, pair[1]%BOARD_SIZE))
        print(action)



    #b = bitarray('1010011')
    #c = bitarray('0000000')
    #print(b ^ c)

    #c = bitarray('0' * 5)
    #c[0] = '1'
    #print(c)
    #print(c[1])
    #print(a.index(1, 1, None))
    """
    
