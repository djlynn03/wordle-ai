import random
import time

from cpuv2 import Wordle_CPU
import sys
sys.setrecursionlimit(10000)

game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}

class App:
    def __init__(self):
        self.word_list = [line[:-1] for line in open("words.txt", "r")]
        # self.root = Tk()
        # self.root.geometry('500x500')
        # self.frm = ttk.Frame(self.root, padding=10)
        # self.root.config(bg="#f0f0f0")
        # self.frm.grid(sticky="nsew")
        
        # self.correct_style = ttk.Style(self.root)
        # self.correct_style.configure("TEntry", background="green")
        
        # self.focused_item = None
        self.current_row = 0
        # self.create_table()
        self.current_word = self.generate_word()
        self.state = "playing" # playing, win, loss
        # self.current_word = "fails"
        
        # self.check_btn = ttk.Button(self.frm, text="Check Word", command=lambda : self.check())
        # self.check_btn.grid(column=2, row=6)
        
        self.cpu = Wordle_CPU(self)

        # self.auto_btn = ttk.Button(self.frm, text="Run CPU", command=lambda: self.cpu.make_guess())
        # self.auto_btn.grid(column=4, row=6)
        
        # self.reset_btn = ttk.Button(self.frm, text="Reset", command=lambda: self.reset())
        # self.reset_btn.grid(column=5, row=6)
        
        while True:
            print(game_data)
            self.cpu.make_guess()
            try:
                self.cpu.make_guess()
            except:
                self.reset()
                
            # time.sleep(0.5)
        
        # self.root.mainloop()

    
    def reset(self):
        # self.root.destroy()
        del self.cpu
        del self
        app = App()
    
    # def create_table(self):
    #     self.letters = []
    #     row = []
        
    #     for i in range(6):
    #         for j in range(5):
    #             txt = StringVar()
    #             txt.trace("w", lambda name, index, mode, sv=txt, r=i, c=j: self.next_entry(sv, r, c))
    #             item = Entry(self.frm, width=5, font=('Arial', 20), textvariable=txt, justify=CENTER)
    #             item.bind("<BackSpace>", lambda event, r=i, c=j: self.last_entry(r, c))
    #             item.bind("<FocusIn>", lambda event, r=i, c=j: self.set_focus_color(r, c, "in"))
    #             item.bind("<FocusOut>", lambda event, r=i, c=j: self.set_focus_color(r, c, "out"))

    #             if j == 4:
    #                 item.bind("<Return>", lambda event, r=i, c=j: self.check())
    #             item.grid(column=j, row=i)
    #             row.append((item, txt))
                
    #         self.letters.append(row)
    #         row = []
    
    # def next_entry(self, e, row, col):
    #     if len(e.get()) > 0:
    #         e.set(e.get()[-1])
            
    #         if col < 4:
    #             self.set_focus(self.letters[row][col + 1][0])
                
    #         else:
    #             self.letters[row][col][0].focus_set()
                
    #     if not e.get().isalpha():
    #         e.set("")        
    
    # def last_entry(self, row, col):
    #     if col == 0:
    #         return
    #     if self.letters[row][col][1].get() == "":
    #         self.letters[row][col-1][1].set("")
            
    #     self.letters[row][col][1].set("")
    #     self.letters[row][col-1][0].focus_set()
    
    # def set_focus_color(self, row, col, type):
    #     if type == "in":
    #         self.letters[row][col][0].config(bg="#f0f0f0")
    #     else:
    #         self.letters[row][col][0].config(bg="#ffffff")
    
    def check(self, word):
        print(word)

        if len(word) == 5:
            in_word = "_____"
            correct_pos = "_____"
            
            for i in range(len(word)):
                if word[i] == self.current_word[i]:
                    # self.letters[self.current_row][i][0].configure(background="green")
                    correct_pos = '%s%s%s' % (correct_pos[:i], word[i], correct_pos[i+1:])
                    
            for i in range(len(word)):
                if word[i] in self.current_word:
                    if (in_word + correct_pos).count(word[i]) < self.current_word.count(word[i]):
                        # self.letters[self.current_row][i][0].configure(background="yellow")
                        in_word = '%s%s%s' % (in_word[:i], word[i], in_word[i+1:])

            if correct_pos.count("_") == 0:
                self.end_game("win")
                return in_word, correct_pos
            
            if self.current_row == 5:
                self.end_game("loss")
                return in_word, correct_pos
            self.current_row += 1
            
            return in_word, correct_pos
        return
    
    def end_game(self, state):
        print(str(self.current_row + 1) + " guesses " + state)
        if state == "win":
            game_data[str(self.current_row + 1)] += 1
        else:
            game_data["DNF"] += 1
        # for i in self.letters:
        #     for j in i:
        #         j[0].bind("<Key>", lambda event: "break")
        # if state == "win":
        #     self.victory_label = ttk.Label(self.frm, text="You won")
        #     self.victory_label.grid(column=2, row=7)
        
          
    # def set_focus(self, item):
    #     item.focus_set()
    #     self.focused_item = item

    def generate_word(self):
        return random.choice([line for line in open("words.txt", "r")])

if __name__ == "__main__":
    app = App()
