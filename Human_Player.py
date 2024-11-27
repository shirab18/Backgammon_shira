'''Creates a class for Human backgammon pieces
Created 2024
@author: Anni Ainesaz
'''

import random

class Human_Player:
    def __init__(self):
        self._pieces = [1, 1,
                        12, 12, 12, 12, 12,
                        17, 17, 17,
                        19, 19, 19, 19, 19]

    def get_pieces(self):
        return self._pieces

    def set_pieces(self, list_of_pieces):
        self._pieces = list_of_pieces
        self.order()

    def move_piece(self, distance, piece, other, r):  # piece is where to move from
        if distance <= 0:
            raise ValueError('Distance must be greater than 0')
        if piece != 0 and self.capturedPiece():
            raise ValueError('You must move your captured piece first')
        if piece in self._pieces:
            idx = self._pieces.index(piece)
            if self.validMove(piece, piece + distance, other, r):
                self._pieces[idx] = piece + distance
            else:
                raise ValueError('That is an invalid place to move your piece')
        else:
            raise ValueError('The chosen piece is not valid')
        self.capture(other)
        self.order()

    def __str__(self):
        return 'Your pieces are at: ' + str(self._pieces)

    def order(self):
        self._pieces.sort()

    def capturedPiece(self):  # checks if I was eaten
        if 0 in self._pieces:
            return True
        else:
            return False

    def capture(self, other):  # I eat
        op = other.get_pieces()[:]
        for piece in self._pieces:
            if piece in op:
                op[op.index(piece)] = 25
        other.set_pieces(op)

    # def validMove(self, makor, yaad, other):
    #     res = 0
    #     #The following line was taken almost straight from stackoverflow (http://stackoverflow.com/questions/9542738/python-find-in-list)
    #     idx = [i for i,x in enumerate(other.get_pieces()) if (x == yaad and x != 0)]
    #     if len(idx) < 1:
    #         res += 1
    #     if yaad >= 25:
    #         distance = makor - yaad
    #         if self._pieces[0] >= 19 and not [x for x in self._pieces if  25 - distance <= x < makor]: #all pieces at home
    #             res += 1
    #     elif 0 < yaad < 25:
    #         res += 1
    #     if res == 2:
    #         return True
    #     else:
    #         return False

    def validMove(self, makor, yaad, other, r):

        idx = [i for i, x in enumerate(other.get_pieces()) if (x == yaad and x != 0 and x != 25)]
        no_oponent = len(idx) <= 1  # the oponent has max 1 pieces in yaad
        print("yaad - makor: ", str(yaad - makor))

        if str(yaad - makor) in r and 1 <= int(yaad) <= 24:
            return no_oponent

        elif yaad >= 25:  # the player wants to get piece out of home
            can_out = self._pieces[0] >= 19
            if str(abs(yaad - makor)) not in r:
                distance = max([x for x in r if int(x) <= int(makor)])
                # all pieces at home and there are no pieces between
                pieces_between = [x for x in self._pieces if (25 - int(distance) <= x < int(makor))]
                can_out = can_out and (not pieces_between)
            return can_out

        return no_oponent

    def win(self):
        return self._pieces == [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]

    def validMoveRandom(self, makor, position, other_pieces, r):  # Add required arguments
        res = 0

        # Check if there's no opposing piece in the position
        idx = [i for i, x in enumerate(other_pieces) if x == position]
        if len(idx) < 1:
            res += 1  # No opposing piece at position

        # Check if all pieces are at home for black
        if self.color == "black" and position <= 0:
            if self._pieces[14] <= 6:  # all pieces at home
                res += 1

        # Check if all pieces are at home for white
        elif self.color == "white" and position >= 25:
            if self._pieces[0] >= 19:  # all pieces at home
                res += 1

        # Check if position is within bounds
        elif 0 < position < 25:
            res += 1

        return res == 2

    def captureRandom(self):
        op = self.other_pieces[:]
        for piece in self._pieces:
            if piece in op:
                if self.color == "black":
                    op[op.index(piece)] = 0
                elif self.color == "white":
                    op[op.index(piece)] = 25
        self.other_pieces = op

    def move_piece_random(self, distance, piece):  # piece is where to move from
        if distance < 0:
            raise ValueError('Distance must be greater than 0')
        if ((self.color == "black" and piece != 25) or (self.color == "white" and piece != 0)) and self.capturedPiece():
            raise ValueError('You must move your captured piece first')
        if piece in self._pieces:
            idx = self._pieces.index(piece)
            if self.color == "black" and self.validMoveRandom(piece, piece - distance, self.other_pieces, distance):
                self._pieces[idx] = piece - distance

            elif self.color == "white" and self.validMoveRandom(piece, piece + distance, self.other_pieces, distance):
                self._pieces[idx] = piece + distance

            else:
                raise ValueError('That is an invalid place to move your piece')
        else:
            raise ValueError('The chosen piece is not valid')
        self.captureRandom()
        self.order()


    def generate_all_moves(self, r):
        self.all_moves = []

        # Ensure r is an integer
        r = int(r)

        for makor in set(self._pieces):
            # Compute target positions
            yaad_black = makor - r
            yaad_white = makor + r

            # Check moves for black
            if self.color == "black" and self.validMoveRandom(makor, yaad_black, self.other_pieces, r):
                if yaad_black < 0:
                    self.all_moves.append([makor, 0])
                else:
                    self.all_moves.append([makor, yaad_black])

            # Check moves for white
            elif self.color == "white" and self.validMoveRandom(makor, yaad_white, self.other_pieces, r):
                if yaad_white > 25:
                    self.all_moves.append([makor, 25])
                else:
                    self.all_moves.append([makor, yaad_white])

        print("all moves: ", self.all_moves)
        return self.all_moves

    def random_move(self, r):
        valid_moves = self.generate_all_moves(r)
        if not valid_moves:
            raise ValueError("No valid moves available.")  # Skip turn if no moves

        # Pick a move randomly (can replace with strategic selection)
        selected_move = random.choice(valid_moves)
        return selected_move

    def play_random(self, board, roll, color):
        """Get the board state, dice roll, and player color, and return the chosen move."""
        self.color = color
        self.roll = roll
        self.roll = [int(die) for die in roll]
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
            self.move_piece_random(abs(selected_move[1] - selected_move[0]), selected_move[0])

        return whole_move


if __name__ == '__main__':
    player = Human_Player()
    p1 = Human_Player()
    p1.set_pieces([])
    assert player.get_pieces() == [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]
    player.move_piece(10, 1, p1)
    assert player.get_pieces() == [1, 11, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]
    print(player)
    try:
        player.move_piece(0, 1, p1)
        print('Error with move_piece')
    except:
        print('move_piece working well with distance')
    try:
        player.move_piece(1, 20, p1)
        print('Error with move_piece')
    except:
        print('move_piece working well with pieces')
    player.set_pieces([0, 0, 0, 1, 0, 0, 0])
    assert player.get_pieces() == [0, 0, 0, 0, 0, 0, 1]
    try:
        player.move_piece(1, 1)
    except:
        print('capturedPiece is working well')
    player.move_piece(1, 0, p1)
    assert player.get_pieces() == [0, 0, 0, 0, 0, 1, 1]
    p1.set_pieces([1, 3, 3, 4, 5])
    player.capture(p1)
    assert p1.get_pieces() == [3, 3, 4, 5, 25]
    p1.set_pieces([2, 2])
    assert player.validMove(2, p1) == False
    assert player.validMove(3, p1) == True
    p1.set_pieces([5, 5])
    try:
        player.move_piece(4, 1, p1)
    except:
        print('validMove is working inside of move_piece')
    player.move_piece(4, 0, p1)
    assert player.get_pieces() == [0, 0, 0, 0, 1, 1, 4]
    player.set_pieces([25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25])
    assert player.win() == True

    print('All tests passed')
