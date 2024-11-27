'''Creates a class for AI backgammon pieces
Created 2024
@author: Anni Ainesaz
'''
import random


class AI_Player:
    def __init__(self):
        self._pieces = [6, 6, 6, 6, 6,
                        8, 8, 8,
                        13, 13, 13, 13, 13,
                        24, 24]
        self.color = "black"

    def get_pieces(self):
        return self._pieces

    def set_pieces(self, list_of_pieces):
        self._pieces = list_of_pieces
        self.order()

    def move_piece(self, distance, piece):  # piece is where to move from
        if distance < 0:
            raise ValueError('Distance must be greater than 0')
        if ((self.color == "black" and piece != 25) or (self.color == "white" and piece != 0)) and self.capturedPiece():
            raise ValueError('You must move your captured piece first')
        if piece in self._pieces:
            idx = self._pieces.index(piece)
            if self.color == "black" and self.validMove(piece - distance):
                self._pieces[idx] = piece - distance

            elif self.color == "white" and self.validMove(piece + distance):
                self._pieces[idx] = piece + distance
            else:
                raise ValueError('That is an invalid place to move your piece')
        else:
            raise ValueError('The chosen piece is not valid')
        self.capture()
        self.order()

    def order(self):
        self._pieces.sort()

    def __str__(self):
        return 'Your pieces are at: ' + str(self._pieces)

    def capturedPiece(self):
        if ((self.color == "black") and (25 in self._pieces)) or ((self.color == "white") and (0 in self._pieces)):
            return True
        else:
            return False

    def capture(self):
        op = self.other_pieces[:]
        for piece in self._pieces:
            if piece in op:
                if self.color == "black":
                    op[op.index(piece)] = 0
                elif self.color == "white":
                    op[op.index(piece)] = 25
        self.other_pieces = op

    def validMove(self, position):  # position is where to move
        res = 0
        # The following line was taken almost straight from stackoverflow (http://stackoverflow.com/questions/9542738/python-find-in-list)
        idx = [i for i, x in enumerate(self.other_pieces) if x == position]
        if len(idx) < 1:
            res += 1  # there is no other piece in position
        if self.color == "black" and position <= 0:
            if self._pieces[14] <= 6:  # all pieces at home
                res += 1
        elif self.color == "white" and position >= 25:
            if self._pieces[0] >= 19:  # all pieces at home
                res += 1
        elif 0 < position < 25:
            res += 1
        if res == 2:
            return True
        else:
            return False

    def play(self, board, roll, color):
        """Get the board state, dice roll, and player color, and return the chosen move."""
        self.color = color
        self.roll = roll
        self._pieces = []  # Reset current player pieces
        self.other_pieces = []  # Reset opposing player pieces

        # Populate self._pieces and self.other_pieces based on board state
        # the first 24
        for i in range(len(board) - 4):
            if board[i] > 0:  # White pieces
                if color == "white":
                    self._pieces.extend([i + 1] * board[i])
                else:
                    self.other_pieces.extend([i + 1] * board[i])
            elif board[i] < 0:  # Black pieces
                if color == "black":
                    self._pieces.extend([i + 1] * abs(board[i]))
                else:
                    self.other_pieces.extend([i + 1] * abs(board[i]))

        # the last 4
        if self.color == "black":
            self._pieces.extend([0] * board[25])
            self._pieces.extend([25] * board[27])
            self.other_pieces.extend([25] * board[24])
            self.other_pieces.extend([0] * board[26])

        elif self.color == "white":
            self.other_pieces.extend([0] * board[25])
            self.other_pieces.extend([25] * board[27])
            self._pieces.extend([25] * board[24])
            self._pieces.extend([0] * board[26])

        self.order()  # Ensure pieces are ordered
        self.other_pieces.sort()

        print("len:", len(self._pieces))
        whole_move = []

        while self.roll:
            # Generate all valid moves
            r = self.roll.pop()
            selected_move = self.random_move(r)
            whole_move.append(selected_move)

            if self.win():
                return
            # Apply the move
            self.move_piece(abs(selected_move[1] - selected_move[0]), selected_move[0])

        return whole_move

    def generate_all_moves(self, r):
        self.all_moves = []

        for makor in set(self._pieces):
            # print("makor-r = ", makor - r)
            if self.color == "black" and self.validMove(makor - r):
                if makor - r < 0:
                    self.all_moves.append([makor, 0])
                else:
                    self.all_moves.append([makor, makor - r])
            elif self.color == "white" and self.validMove(makor + r):
                if makor + r > 25:
                    self.all_moves.append([makor, 25])
                else:
                    self.all_moves.append([makor, makor + r])
        print("all moves: ", self.all_moves)
        return self.all_moves

    def random_move(self, r):

        valid_moves = self.generate_all_moves(r)
        if not valid_moves:
            raise ValueError("No valid moves available.")  # Skip turn if no moves

        # Pick a move randomly (can replace with strategic selection)
        selected_move = random.choice(valid_moves)
        return selected_move

    def win(self):

        if (self.color == "black" and self._pieces == [0] * 15) or (
                self.color == "white" and self._pieces == [25] * 15):
            # print("comp won!!!")
            return True
        else:
            # print("comp lost!!!")
            return False


if __name__ == '__main__':
    # No tests here because all tests are in backgammon_white.py and almost all of it is the same
    a = AI_Player()
