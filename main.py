from locale import currency
from os import curdir
import random
from tkinter import *
from tkinter import ttk

import re

from xarray import corr


class App:
    def __init__(self):
        self.word_list = [line[:-1] for line in open("words.txt", "r")]
        # print("fails" in self.word_list)
        self.root = Tk()
        self.root.geometry('500x500')
        self.frm = ttk.Frame(self.root, padding=10)
        self.root.config(bg="#f0f0f0")
        self.frm.grid(sticky="nsew")
        
        self.correct_style = ttk.Style(self.root)
        self.correct_style.configure("TEntry", background="green")
        
        self.focused_item = None
        self.current_row = 0
        self.create_table()
        
        self.current_word = self.generate_word()
        # self.current_word = "fails"
        print(self.current_word)
        
        self.check_btn = ttk.Button(self.frm, text="Check Word", command=lambda : self.check())
        self.check_btn.grid(column=2, row=6)
        
        self.cpu = Wordle_CPU(self)
        for _ in range(6):
            try:
                self.cpu.make_guess()
            except:
                break
        self.auto_btn = ttk.Button(self.frm, text="Run CPU", command=lambda: self.cpu.make_guess())
        self.auto_btn.grid(column=4, row=6)
        self.root.mainloop()

    
    def create_table(self):
        self.letters = []
        row = []
        
        for i in range(6):
            for j in range(5):
                txt = StringVar()
                txt.trace("w", lambda name, index, mode, sv=txt, r=i, c=j: self.next_entry(sv, r, c))
                item = Entry(self.frm, width=5, font=('Arial', 20), textvariable=txt, justify=CENTER)
                item.bind("<BackSpace>", lambda event, r=i, c=j: self.last_entry(r, c))
                item.bind("<FocusIn>", lambda event, r=i, c=j: self.set_focus_color(r, c, "in"))
                item.bind("<FocusOut>", lambda event, r=i, c=j: self.set_focus_color(r, c, "out"))

                if j == 4:
                    item.bind("<Return>", lambda event, r=i, c=j: self.check())
                item.grid(column=j, row=i)
                row.append((item, txt))
                
            self.letters.append(row)
            row = []
    
    def next_entry(self, e, row, col):
        if len(e.get()) > 0:
            e.set(e.get()[-1])
            
            if col < 4:
                self.set_focus(self.letters[row][col + 1][0])
                
            else:
                self.letters[row][col][0].focus_set()
                
        if not e.get().isalpha():
            e.set("")        
    
    def last_entry(self, row, col):
        if col == 0:
            return
        if self.letters[row][col][1].get() == "":
            self.letters[row][col-1][1].set("")
            
        self.letters[row][col][1].set("")
        self.letters[row][col-1][0].focus_set()
    
    def set_focus_color(self, row, col, type):
        if type == "in":
            self.letters[row][col][0].config(bg="#f0f0f0")
        else:
            self.letters[row][col][0].config(bg="#ffffff")
    
    def check(self):
        word = []
        
        for entry in self.letters[self.current_row]:
            word.append(str(entry[1].get()))
            
        word = ''.join(word)
        print(word)
        # if len(word) == 5 and word in self.word_list:
        if len(word) == 5:
            in_word = "_____"
            correct_pos = "_____"
            
            for i in range(len(word)):
                print(word[i], self.current_word[i])
                if word[i] == self.current_word[i]:
                    self.letters[self.current_row][i][0].configure(background="green")
                    correct_pos = '%s%s%s' % (correct_pos[:i], word[i], correct_pos[i+1:])
                    
            for i in range(len(word)):
                if word[i] in self.current_word:
                    if (in_word + correct_pos).count(word[i]) < self.current_word.count(word[i]):
                        self.letters[self.current_row][i][0].configure(background="yellow")
                        in_word = '%s%s%s' % (in_word[:i], word[i], in_word[i+1:])

            if correct_pos.count("_") == 0:
                self.end_game("win")
                return in_word, correct_pos
            
            if self.current_row == 5:
                self.end_game("loss")
                return in_word, correct_pos
            print(in_word, correct_pos)
            self.set_focus(self.letters[self.current_row+1][0][0])
            self.current_row += 1
            
            self.root.update_idletasks()
            return in_word, correct_pos
        return
    
    def end_game(self, state):
        for i in self.letters:
            for j in i:
                j[0].bind("<Key>", lambda event: "break")
        if state == "win":
            self.victory_label = ttk.Label(self.frm, text="You won")
            self.victory_label.grid(column=2, row=7)
        
          
    def set_focus(self, item):
        item.focus_set()
        self.focused_item = item

    def generate_word(self):
        return random.choice([line for line in open("words.txt", "r")])

class Wordle_CPU:
    def __init__(self, app: App):
        self.app = app
        self.available_words = self.app.word_list
        self.correct_letters = "_____"
        self.in_word = ""
        self.not_in_word = ""
        # self.incorrect_pos = "_____"
            
    def filter(self, filterChars: list | str, position="any", repetitions=1, wordList="none"):
        returnList = []
        for char in filterChars:
            if type(position) == int:
                if position < 1 or position > 5:
                    raise RuntimeError("InvalidCharacterPosition")
            
            if wordList == "none":
                file = open("words.txt", "r")
                wordList = [line for line in file]
                file.close()
            for word in wordList:
                if position != "any":
                    if word[position - 1] == char and word.count(char) == repetitions:
                        returnList.append(word[:-1])
                elif word.count(char) == repetitions:
                    if char in word:
                        returnList.append(word[:-1])
        return returnList

    def inverseFilter(self, filterChars: list, wordList="none"):
        returnList = []
        for char in filterChars:
            if wordList == "none":
                file = open("words.txt", "r")
                wordList = [line for line in file]
                file.close()
            for word in wordList:
                if char not in word:
                    returnList.append(word[:-1])
        return returnList

    def filter2(self, chars, is_fixed=False):
        '''
        chars is a string of format 'abcde', where a blank character is denoted as '_'
        '''
        returnv = []
        if chars == "_____":
            return
        if not is_fixed:
            chars = chars.replace('_', '')
            
            for char in chars:
                for word in self.available_words:
                    if char in word:
                        returnv.append(word)
                        
            self.available_words = returnv
        else:
            for word in self.available_words:
                if self.two_string(word, chars):
                    returnv.append(word)
                    
            print(returnv)
            self.available_words = list(set(returnv))
            
    def two_string(self, a,b):
        for i, (ca, cb) in enumerate(zip(a,b)):
            if ca==cb:
                return True
            
    def filter3(self):
        if self.correct_letters.count("_") < 5:
            
            pattern = r"\b"
            for char in self.correct_letters:
                if char == "_":
                    pattern += r"[a-zA-Z]"
                else:
                    pattern += char
            pattern += r"\b"
            print(pattern)
            self.available_words = re.findall(pattern, " ".join(self.available_words))
        
        if len(self.in_word) > 0:
            tmp = []
            for word in self.available_words:
                if self.containsAll(word, self.in_word):
                    tmp.append(word)
            self.available_words = tmp
            
        if len(self.not_in_word) > 0:
            for word in self.available_words:
                if self.containsAny(word, self.not_in_word):
                    self.available_words.remove(word)

    def containsAll(self, str, set):
        """ Check whether sequence str contains ALL of the items in set. """
        return all([c in str for c in set])
     
    def containsAny(self, str, set):
        """ Check whether sequence str contains ANY of the items in set. """
        return any([c in str for c in set])
    
    
    def make_guess(self):
        if self.app.current_row == 0:
            word = "crane"
        else:
            word = random.choice(self.available_words)
        self.available_words.remove(word)
        
        for i in range(5):
            self.app.letters[self.app.current_row][i][1].set(word[i])
        in_word, correct_pos = self.app.check()
        for i in range(5):
            if correct_pos[i] != "_" and self.correct_letters[i] == "_":
                self.correct_letters = '%s%s%s' % (self.correct_letters[:i], word[i], self.correct_letters[i+1:])
                
        self.in_word += in_word.replace("_", "")
        
        for letter in word:
            if letter not in self.not_in_word and letter not in correct_pos and letter not in in_word:
                self.not_in_word += letter
                
        print(self.in_word, self.not_in_word, self.correct_letters)
        self.filter3()
        print(self.available_words)
            
        self.app.root.update_idletasks()



if __name__ == "__main__":
    app = App()
    # print(filter('a',1,2))
