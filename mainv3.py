import random
import time

from cpuv2 import Wordle_CPU
import sys
sys.setrecursionlimit(10000)

game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}

class App:
    def __init__(self):
        self.word_list = [line[:-1] for line in open("words.txt", "r")]
        self.current_row = 0
        self.current_word = self.generate_word()
        self.state = "playing" # playing, win, loss

        
        self.cpu = Wordle_CPU(self)

        while True:
            if self.state == "playing":
                self.cpu.make_guess()
            else:
                self.reset()
            # print(game_data)
            # # self.cpu.make_guess()
            # try:
            #     self.cpu.make_guess()
            # except:
            #     self.reset()
                
            # time.sleep(0.5)
        

    
    def reset(self):
        pct = (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"]) / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"])
        print(str(game_data) + " " + str(pct))
        del self.cpu
        self.cpu = Wordle_CPU(self)
        self.word_list = [line[:-1] for line in open("words.txt", "r")]
        self.current_row = 0
        self.current_word = self.generate_word()
        self.state = "playing" # playing, win, loss
    
    
    def check(self, word):
        if len(word) == 5:
            in_word = "_____"
            correct_pos = "_____"
            
            for i in range(len(word)):
                if word[i] == self.current_word[i]:
                    correct_pos = '%s%s%s' % (correct_pos[:i], word[i], correct_pos[i+1:])
                    
            for i in range(len(word)):
                if word[i] in self.current_word:
                    if (in_word + correct_pos).count(word[i]) < self.current_word.count(word[i]):
                        in_word = '%s%s%s' % (in_word[:i], word[i], in_word[i+1:])

            if correct_pos.count("_") == 0:
                self.end_game("win")
                return in_word, correct_pos
            
            if self.current_row == 5:
                self.end_game("loss")
                return in_word, correct_pos
            self.current_row += 1
            
            return in_word, correct_pos
        return "_____", "_____"
    
    def end_game(self, state):
        # print(str(self.current_row + 1) + " guesses " + state)
        if state == "win":
            game_data[str(self.current_row + 1)] += 1
        else:
            game_data["DNF"] += 1
        self.state = "end"


    def generate_word(self):
        return random.choice([line for line in open("words.txt", "r")])

if __name__ == "__main__":
    app = App()
