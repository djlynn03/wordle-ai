import random

game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}

def run_game():
    available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
    steps = 0
    pass

def test_run():
    available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
    test_word = random.choice(available_words)
    print(test_word)





def filter(self, filterChars: list | str, position="any", repetitions=1, wordList="none"):
    returnList = []
    for char in filterChars:
        if type(position) == int:
            if position < 1 or position > 5:
                raise RuntimeError("InvalidCharacterPosition")
        
        if wordList == "none":
            available_words = open("words.txt", "r")
            wordList = [word for word in available_words]
            available_words.close()
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