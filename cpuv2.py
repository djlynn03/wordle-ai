import random
import re
class Wordle_CPU:
    def __init__(self, app):
        self.app = app
        self.available_words = [line[:-1] for line in open("words.txt", "r")]
        self.correct_letters = "_____"
        self.in_word = ""
        self.not_in_word = ""
        self.guessed_letters = ""
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
            self.available_words = re.findall(pattern, " ".join(self.available_words))
        
        if len(self.in_word) > 0:
            tmp = []
            for word in self.available_words:
                if self.containsAll(word, self.in_word):
                    tmp.append(word)
            self.available_words = tmp
            
        if len(self.not_in_word) > 0:
            tmp = []
            flag = 1
            for word in self.available_words:
                for char in self.not_in_word:
                    if char not in word:
                        flag = 1
                    else:
                        flag = 0
                        break
                if flag == 1:
                    tmp.append(word)
            self.available_words = tmp
            
    def filter4(self, correct_letters, in_word, not_in_word, word_list):
        returnv = word_list
        if correct_letters.count("_") < 5:
            pattern = r"\b"
            for char in correct_letters:
                if char == "_":
                    pattern += r"[a-zA-Z]"
                else:
                    pattern += char
            pattern += r"\b"
            returnv = re.findall(pattern, " ".join(returnv))
        
        if len(in_word) > 0:
            tmp = []
            for word in returnv:
                if self.containsAll(word, in_word):
                    tmp.append(word)
            returnv = tmp
            
        if len(not_in_word) > 0:
            tmp = []
            flag = 1
            for word in returnv:
                for char in not_in_word:
                    if char not in word:
                        flag = 1
                    else:
                        flag = 0
                        break
                if flag == 1:
                    tmp.append(word)
            returnv = tmp
        return returnv

    def containsAll(self, str, set):
        """ Check whether sequence str contains ALL of the items in set. """
        return all([c in str for c in set])
     
    def containsAny(self, str, set):
        """ Check whether sequence str contains ANY of the items in set. """
        return any([c in str for c in set])
    
    def get_word_score(self, word):
        freq = {i[:-1][0]: i[:-1][2:] for i in open("lettersFreq.txt", "r").readlines()}
        return sum([int(freq[char.upper()]) for char in set(word)])
        
    def make_guess(self):
        if self.app.current_row == 0:
            word = "stand"
        elif self.app.current_row == 1:
            word = "oiler"
        elif len(self.available_words) > 5 - self.app.current_row:
            try:
                word = max(self.filter4("_____", "", self.guessed_letters, self.app.word_list), key=self.get_word_score)
            except:
                word = random.choice(self.available_words)
        else:
            if len(self.available_words) == 0:
                self.available_words = [line[:-1] for line in open("words.txt", "r")]
            word = random.choice(self.available_words)
        
        try:
            len(word)
        except:
            word = random.choice(self.available_words)
        
        try:
            self.available_words.remove(word)
        except:
            1
        
        # if len(self.available_words) > 5 - self.app.current_row:
            
        
        self.guessed_letters += word
        self.guessed_letters = "".join(set(self.guessed_letters))

        in_word, correct_pos = self.app.check(word)
        for i in range(5):
            if correct_pos[i] != "_" and self.correct_letters[i] == "_":
                self.correct_letters = '%s%s%s' % (self.correct_letters[:i], word[i], self.correct_letters[i+1:])
                
        self.in_word += in_word.replace("_", "")
        
        for letter in word:
            if letter not in self.not_in_word and letter not in correct_pos and letter not in in_word:
                self.not_in_word += letter
                
        self.filter3()
