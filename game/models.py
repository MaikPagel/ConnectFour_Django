from django.db import models

class Board(models.Model):
    rows = models.IntegerField(default=6)
    columns = models.IntegerField(default=7)
    board_state = models.TextField(default='_' * 42)

    def drop_disc(self, column, symbol):
        color_class = 'r' if symbol == 'X' else 'y'
        for row in range(self.rows - 1, -1, -1):
            if self.board_state[row * self.columns + column] == '_':
                self.board_state = self.board_state[:row * self.columns + column] + color_class + self.board_state[row * self.columns + column + 1:]
                self.save()
                return True
        return False

    def check_winner(self, symbol):
        board = [self.board_state[i:i+self.columns] for i in range(0, self.rows*self.columns, self.columns)]
        color_class = 'r' if symbol == 'X' else 'y'
        
        # Check horizontal
        for row in board:
            if self._check_four_in_a_row(row, color_class):
                return True
        
        # Check vertical
        for col in range(self.columns):
            if self._check_four_in_a_row([board[row][col] for row in range(self.rows)], color_class):
                return True
        
        # Check diagonals
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if self._check_four_in_a_row([board[row+i][col+i] for i in range(4)], color_class):
                    return True
                if self._check_four_in_a_row([board[row+3-i][col+i] for i in range(4)], color_class):
                    return True
        
        return False

    def _check_four_in_a_row(self, line, color_class):
        count = 0
        for cell in line:
            if cell == color_class:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

class Player(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=1)  # 'X' or 'O'
