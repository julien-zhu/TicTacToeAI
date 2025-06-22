#!/usr/bin/env python3

import numpy as np

TIE = "tie"

class Player:
    name: str
    cpu_lvl: int # 0 : player, 1 : random cpu, 2 : minimax cpu
    def __init__(self, name:str, cpu_lvl:int):
        assert cpu_lvl in (0, 1, 2)
        self.name = name
        self.cpu_lvl = cpu_lvl

def all_equal_to(list : list, elt) -> bool:
    # empty list doesnt count
    return bool(list) and len(set(list)) == 1 and list[0] == elt

def sign_of_bool(bool: bool) -> int:
    # false -> -1 and true -> 1
    return 2*bool - 1

def get_input() -> int:
    while True:
        try:
            return int(input("[Choose a cell between 1-9]: >>> ")) -1 # remap 1..9 ==> 0..8
        except ValueError:
            print("Invalid entry")
            continue

class Game:
    grid: list
    players: list[Player] #[X, O]
    playing_index: int #index of who is playing
    playing: Player

    def _sync_playing_(self): # should always be true
        self.playing = self.players[self.playing_index]

    def __init__(self, X_lvl:int, O_lvl:int):
        self.grid = ['.']*9
        self.players = [Player('X', X_lvl), Player('O', O_lvl)]
        self.playing_index = 0
        self._sync_playing_()
    
    def print_grid(self):
        print("------------")
        for i in reversed(range(3)):
            for j in range(3):
                print(f"{self.grid[i*3+j]} ", end='')
            print('\n', end='')
    
    def swap_player(self):
        self.playing_index += 1
        self.playing_index %= 2
        self._sync_playing_()
    
    def other_player(self) -> Player:
        return self.players[(self.playing_index+1)%2]
    
    def make_move(self, cell:int, letter:None|str = None):
        if letter is None:
            letter = self.playing.name
        self.grid[cell] = letter

    def undo_move(self, cell: int):
        self.grid[cell] = '.'
    
    def available_cells(self) -> list:
        out = []
        for i, v in enumerate(self.grid):
            if v == '.': 
                out.append(i)
        return out
    
    def is_game_over(self, winnerRef:list[str] = [""]) -> bool:
        """
            Winner is return as a parameter passed as reference
            *winnerRef = "X", "O" or "tie"
        """
        for players in self.players:
            letter = players.name
            for row in range(3):
                if all_equal_to(self.grid[3*row:3*(row+1)], letter):
                    winnerRef[0] = letter
                    return True
                col = row
                if all_equal_to(self.grid[col:9:3], letter): 
                    winnerRef[0] = letter
                    return True
            if all_equal_to(self.grid[0:9:4], letter):
                winnerRef[0] = letter
                return True
            if all_equal_to(self.grid[2:8:2], letter): 
                winnerRef[0] = letter
                return True
        if len(self.available_cells()) <= 0:
            winnerRef[0] = TIE
            return True
        return False

    def score(self) -> int:
        letter = [""]
        if self.is_game_over(letter):
            match letter[0]:
                case "tie": return 0
                case 'X': return 1
                case 'O': return -1
                case _: raise Exception("is_game_over function is not working properly")
        raise Exception("should not be called if game is not over")
        

    def human_turn(self):
        print(f"{self.playing.name}'s turn")
        while (v := get_input()) not in self.available_cells():
            print("Invalid.")
        self.make_move(v)
    
    def cpu_random_turn(self):
        v = np.random.choice(self.available_cells(), 1)[0]
        self.make_move(v)

    def minimax(self, isMaximizing:bool, depth: int, alpha: float, beta: float) -> dict[str, int]:
        """
        Minimax algorithm with alpha beta pruning
        """
        # return [cell, score], cell is the cell with the best score. if cell=-1 ==> cell not chosen
        # Terminal case
        winner = [""]
        if depth <= 0:
            raise Exception("Increase depth.")  # depth > 9, since game is at most 9 moves.
        if self.is_game_over(winner):
            return {"cell": -1, "score": depth*self.score()} # score is more important if win more early
        
        letter = "X" if isMaximizing else "O"
        
        if isMaximizing:
            best = {"cell": -1, "score": -np.inf}
        else:
            best = {"cell": -1, "score": np.inf}

        for cell in self.available_cells():

            self.make_move(cell, letter)
            result = self.minimax(not(isMaximizing), depth-1, alpha, beta)
            # maximizing the best, or minimizing the best
            if (    isMaximizing  and best["score"] < result["score"]) \
            or (not(isMaximizing) and best["score"] > result["score"]):
                best["score"] = result["score"]
                best["cell"] = cell
            self.undo_move(cell)
            # alpha-beta pruning
            if isMaximizing:
                alpha = max(result["score"], alpha) # alpha : best score for the maximizer
            else:
                beta = min(result["score"], beta) # beta : best score for the minimizer
            if beta <= alpha:
                break
        return best

    def cpu_ai_turn(self):
        # randomize starting position
        if len(self.available_cells()) >= 9:
            v = np.random.choice(self.available_cells(), 1)[0]
            assert v in self.available_cells()
            self.make_move(v)
        else:
            chosen_cell = self.minimax(isMaximizing = (self.playing.name == 'X'), depth = 10, alpha=-np.inf, beta=np.inf)["cell"]
            self.make_move(chosen_cell)

    def play(self):
        winner = [""]
        try:
            while not(self.is_game_over(winner)):
                self.print_grid()
                match self.playing.cpu_lvl:
                    case 0: #human
                        self.human_turn()
                    case 1: #cpu choose at random
                        self.cpu_random_turn()
                    case 2: #cpu choose with minimax algorithm
                        self.cpu_ai_turn()
                    case _: #human...
                        self.human_turn()
                self.swap_player()
        except KeyboardInterrupt:
            print("\nGame closed")
            exit(0)
        
        self.print_grid()
        if winner[0] == "tie":
            print("TIE")
        else:
            print(f"{winner[0]} won")

if __name__ == "__main__":
    print("X player: [1] Human, [2] Computer (Weak), [3] Computer (Strong) (Type 1, 2 or 3)")
    while (inputX := input(">>> ")) not in ("1", "2", "3"):
        print("Invalid value: Type 1, 2 or 3")
    print("O player: [1] Human, [2] Computer (Weak), [3] Computer (Strong) (Type 1, 2 or 3)")
    while (inputO := input(">>> ")) not in ("1", "2", "3"):
        print("Invalid value: Type 1, 2 or 3")
    is_cpu_X = int(inputX) - 1 # map 1, 2, 3 ==> 0, 1, 2
    is_cpu_O = int(inputO) - 1 # map 1, 2, 3 ==> 0, 1, 2
    game = Game(is_cpu_X, is_cpu_O)
    game.play()
