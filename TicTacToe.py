from abc import ABC, abstractmethod
import math
import random


class Board():
    def __init__(self):
        self.cells = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def display(self):
        print(" {}  |  {}  |  {}  ".format(
            self.cells[0][0], self.cells[0][1], self.cells[0][2]))
        print(" _____________")
        print('')
        print(" {}  |  {}  |  {} ".format(
            self.cells[1][0], self.cells[1][1], self.cells[1][2]))
        print(" _____________")
        print('')
        print(" {}  |  {}  |  {} ".format(
            self.cells[2][0], self.cells[2][1], self.cells[2][2]))

    def add_move(self, move):
        row = self.cells[move.x]
        row[move.y] = move.counter

    def isEmpty(self, row, column):
        if self.cells[row][column] == ' ':
            return True
        else:
            return False

    def cellContains(self, row, column, counter):
        if self.cells[row][column] == counter:
            return True
        else:
            return False

    def checkFull(self):
        for row in range(0, 3):
            for column in range(0, 3):
                if self.isEmpty(row, column):
                    return False
        return True

    def checkWinner(self, player, game):
        c = player.counter
        if player == game.human:
            otherplayer = game.ai
        elif player == game.ai:
            otherplayer = game.human

        check1 = (self.cellContains(0, 0, c) and self.cellContains(0, 1, c) and self.cellContains(0, 2, c) or self.cellContains(1, 0, c) and self.cellContains(1, 1, c) and self.cellContains(1, 2, c) or self.cellContains(2, 0, c) and self.cellContains(2, 1, c) and self.cellContains(2, 2, c) or self.cellContains(0, 0, c) and self.cellContains(1, 0, c) and self.cellContains(
            2, 0, c) or self.cellContains(0, 1, c) and self.cellContains(1, 1, c) and self.cellContains(2, 1, c) or self.cellContains(0, 2, c) and self.cellContains(1, 2, c) and self.cellContains(2, 2, c) or self.cellContains(0, 0, c) and self.cellContains(1, 1, c) and self.cellContains(2, 2, c) or self.cellContains(0, 2, c) and self.cellContains(1, 1, c) and self.cellContains(2, 0, c))

        c = otherplayer.counter
        check2 = (self.cellContains(0, 0, c) and self.cellContains(0, 1, c) and self.cellContains(0, 2, c) or self.cellContains(1, 0, c) and self.cellContains(1, 1, c) and self.cellContains(1, 2, c) or self.cellContains(2, 0, c) and self.cellContains(2, 1, c) and self.cellContains(2, 2, c) or self.cellContains(0, 0, c) and self.cellContains(1, 0, c) and self.cellContains(
            2, 0, c) or self.cellContains(0, 1, c) and self.cellContains(1, 1, c) and self.cellContains(2, 1, c) or self.cellContains(0, 2, c) and self.cellContains(1, 2, c) and self.cellContains(2, 2, c) or self.cellContains(0, 0, c) and self.cellContains(1, 1, c) and self.cellContains(2, 2, c) or self.cellContains(0, 2, c) and self.cellContains(1, 1, c) and self.cellContains(2, 0, c))

        if check1 is False:
            if check2 is False:
                if self.checkFull():
                    return 'tie'
                else:
                    return None
            else:
                return otherplayer.counter
        else:
            return player.counter


class Counter:

    def __init__(self, str):
        self.__label = str

    def __str__(self):
        return self.__label


X = Counter('X')
O = Counter('O')


class Move:
    def __init__(self, x, y, counter):
        self.x = x
        self.y = y
        self.counter = counter

    def __str__(self):
        return self.counter + " at " + str(self.x) + "," + str(self.y)


class Player:
    def __init__(self, board):
        self.board = board
        self._counter = None

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, counter):
        self._counter = counter

    @counter.getter
    def counter(self):
        return self._counter

    @abstractmethod
    def get_move(self):
        pass

    def __str__(self):
        return self.__class__.__name__ + "[" + str(self.counter) + "]"


class Human(Player):
    def __init__(self, board):
        super().__init__(board)

    def get_user_input(self, prompt):
        invalid_input = True
        while invalid_input:
            print(prompt)
            user_input = input()
            if not user_input.isdigit():
                print("Input must be an integer")

            else:
                if int(user_input) < 1 or int(user_input) > 3:
                    print("Please enter a valid digit")

                else:
                    invalid_input = False
        return int(user_input) - 1

    def get_move(self):

        while True:
            row = self.get_user_input("Input row:")
            column = self.get_user_input("Input Column")

            if self.board.isEmpty(row, column):
                return Move(row, column, self.counter)

            else:
                print("That position is not free")
                print("try again")


class AI(Player):

    def __init__(self, board, game):
        super().__init__(board)
        self.game = game
        self.currentPlayer = self

    def switchPlayer(self):
        if self.currentPlayer == self.game.human:
            self.currentPlayer = self.game.human
        else:
            self.currentPlayer = self

    def minimax(self, board, depth, isMaximizing):

        alpha = -math.inf
        beta = math.inf

        scores = {
            self.counter: 1,
            self.game.human.counter: -1,
            'tie': 0
        }

        winnercheck = self.board.checkWinner(self.currentPlayer, self.game)

        if winnercheck != None:
            return scores[winnercheck]

        if isMaximizing:
            bestScore = -math.inf
            for row in range(0, 3):
                for column in range(0, 3):
                    if self.board.isEmpty(row, column):
                        self.switchPlayer()
                        self.board.add_move(Move(row, column, self.counter))

                        bestScore = max(self.minimax(
                            self.board, depth + 1, False), bestScore)
                        self.board.add_move(Move(row, column, ' '))
            return bestScore

        else:
            bestScore = math.inf
            for row in range(0, 3):
                for column in range(0, 3):
                    if self.board.isEmpty(row, column):
                        self.switchPlayer()
                        self.board.add_move(
                            Move(row, column, self.game.human.counter))

                        bestScore = min(self.minimax(
                            self.board, depth + 1, True), bestScore)
                        self.board.add_move(Move(row, column, ' '))

            return bestScore

    def get_move(self):

        bestScore = -math.inf

        for row in range(0, 3):
            for column in range(0, 3):
                if self.board.isEmpty(row, column):
                    self.board.add_move(Move(row, column, self.counter))

                    score = self.minimax(self.board, 0, False)
                    self.board.add_move(Move(row, column, ' '))

                    if score > bestScore:
                        bestScore = score
                        bestMove = [row, column]

        return Move(bestMove[0], bestMove[1], self.counter)


class Game:
    def __init__(self):
        self.board = Board()
        self.human = Human(self.board)
        self.ai = AI(self.board, self)
        self.nextPlayer = None
        self.winner = None

    def selectPlayerCounter(self):

        counter = ''

        while not (counter == 'X' or counter == 'O'):
            print("X or O?")
            counter = input().upper()

            if counter != 'X' and counter != 'O':
                print("Input must be X or O")

        if counter == 'X':
            self.human.counter = X
            self.ai.counter = O

        else:
            self.human.counter = O
            self.ai.counter = X

    def firstPlayer(self):
        if random.randint(0, 1) == 0:
            self.next_player = self.human

        else:
            self.next_player = self.ai

    def play(self):
        print("TicTacToe")
        self.selectPlayerCounter()
        self.firstPlayer()

        print(self.next_player, 'will play first')

        while self.winner is None:
            if self.next_player == self.human:
                self.board.display()
                print("your move")

                move = self.human.get_move()
                self.board.add_move(move)
                if self.board.checkWinner(self.human, self) == self.human.counter:
                    self.winner = self.human

                else:
                    self.next_player = self.ai

            else:
                move = self.ai.get_move()

                self.board.add_move(move)

                if self.board.checkWinner(self.ai, self) == self.ai.counter:
                    self.winner = self.ai

                else:
                    self.next_player = self.human

            if self.winner is not None:
                print(str(self.winner) + " wins")

            elif self.board.checkFull():
                print("Game is tie")
                break

        print("")
        self.board.display()


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
