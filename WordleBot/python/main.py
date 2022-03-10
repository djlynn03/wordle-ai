import random
import threading
import math

def get_letter_dictionary(word_list):   #gets a letter dictionary of the frequencies of each letter in the word list
    letter_dictionary = {}
    for letter in "abcdefghijklmnopqrstuvwxyz":
        letter_dictionary.update({letter:0})
    for word in word_list:
        for letter in word:
            letter_dictionary.update({letter:(letter_dictionary[letter] + 1)})
    return letter_dictionary

def game_data_avg(game_data):   #returns average steps to complete a game
    try:
        return (game_data["1"] + 2 * game_data["2"] + 3 * game_data["3"] + 4 * game_data["4"] + 5 * game_data["5"] + 6 * game_data["6"]) / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"])
    except:
        return 0

def filter_words(available_words, guess, answer):   #returns a list of possible words left, given a guess and an answer
    return_list = [word for word in available_words]
    for int in range(len(answer)):
        if guess[int] == answer[int]:   #filters words with correct letter at specific location
            # print(guess[int], "at specific location")
            return_list = filter(guess[int], position=(int), wordList=return_list)
        elif guess[int] in answer:    #filters words with correct letter present
            # print(guess[int], "in word")
            return_list = filter(guess[int], wordList=return_list)   
            return_list = wrongPositionFilter(guess[int], int, wordList=return_list) 
        elif guess[int] not in answer:
            # print(guess[int], "not in word")
            return_list = inverseFilter(filterChar=guess[int], wordList=return_list)
    return return_list


"""
repetition filter for filter_words, fix with duncan

elif answer.count(guess[int]) > 1 and guess.count(guess[int]) > 1:    #filters words with same repetitions of letter, mimicking the mechanic in the game
    difference = answer.count(guess[int]) - guess.count(guess[int])
    temp_list = return_list
    if difference > 0:
        for i in range(difference):
            for word in filter(guess[int], repetitions=guess.count(guess[int]) + i, wordList=temp_list):
                if word != temp_list:
                    temp_list.append(word)
    else:
        temp_list = filter(guess[int], repetitions=guess.count(guess[int]), wordList=temp_list)
    return_list = temp_list
"""


def filter(filterChar, position="any", repetitions="any", wordList="none"): #general purpose filter, covers correct letters, repetitions, and letters present
    returnList = []
    if type(position) == int:
        if position < 0 or position > 4:
            raise RuntimeError("InvalidCharacterPosition")
    if wordList == "none":
        available_words = open("words.txt", "r")
        wordList = [word for word in available_words]
        available_words.close()
    for word in wordList:
        if position != "any":
            if word[position] == filterChar:
                if word.count(filterChar) == repetitions or repetitions == "any":
                    returnList.append(word)
        elif repetitions != "any":
            if filterChar in word and word.count(filterChar) == repetitions:
                returnList.append(word)
        else:
            if filterChar in word:
                returnList.append(word)
    return returnList

def inverseFilter(filterChar, wordList="none"): #returns a list of words that do NOT contain the filter character
    returnList = []
    if wordList == "none":
        file = open("words.txt", "r")
        wordList = [line for line in file]
        file.close()
    for word in wordList:
        if filterChar not in word:
            returnList.append(word)
    return returnList

def wrongPositionFilter(filterChar, index, wordList="none"):    #returns a list of words that do not have the filter character at the specified index
    returnList = []
    if wordList == "none":
        file = open("words.txt", "r")
        wordList = [line for line in file]
        file.close()
    for word in wordList:
        if filterChar != word[index]:
            returnList.append(word)
    return returnList

def get_word_value(word, letter_dictionary, counted_word=""):   #gets the word value based off of frequency of letters in the letter dictionary
    value = 0
    counted_letters = [letter for letter in counted_word]
    for letter in word:
        if letter not in counted_letters:
            value += letter_dictionary[letter]
            counted_letters.append(letter)
    return value

def get_word_value2(word, word_list):   #goes through all the combinations of letter states for the word and returns a score based on the weighted average list reduction (lower is better)
    reset_list = [word for word in word_list]
    resulting_words_list_lengths = []
    for first_letter in range(3):
        for second_letter in range(3):
            for third_letter in range(3):
                for fourth_letter in range(3):
                    for fifth_letter in range(3):
                        if first_letter == 0:
                            word_list = inverseFilter(word[0], word_list)
                        elif first_letter == 1:
                            word_list = filter(word[0], wordList=word_list)
                            word_list = wrongPositionFilter(word[0], 0, word_list)
                        elif first_letter == 2:
                            word_list = filter(word[0], position=0, wordList=word_list)
                        if second_letter == 0:
                            word_list = inverseFilter(word[1], word_list)
                        elif second_letter == 1:
                            word_list = filter(word[1], wordList=word_list)
                            word_list = wrongPositionFilter(word[1], 1, word_list)
                        elif second_letter == 2:
                            word_list = filter(word[1], position=1, wordList=word_list)
                        if third_letter == 0:
                            word_list = inverseFilter(word[2], word_list)
                        elif third_letter == 1:
                            word_list = filter(word[2], wordList=word_list)
                            word_list = wrongPositionFilter(word[2], 2, word_list)
                        elif third_letter == 2:
                            word_list = filter(word[2], position=2, wordList=word_list)
                        if fourth_letter == 0:
                            word_list = inverseFilter(word[3], word_list)
                        elif fourth_letter == 1:
                            word_list = filter(word[3], wordList=word_list)
                            word_list = wrongPositionFilter(word[3], 3, word_list)
                        elif fourth_letter == 2:
                            word_list = filter(word[3], position=3, wordList=word_list)
                        if fifth_letter == 0:
                            word_list = inverseFilter(word[4], word_list)
                        elif fifth_letter == 1:
                            word_list = filter(word[4], wordList=word_list)
                            word_list = wrongPositionFilter(word[3], 3, word_list)
                        elif fifth_letter == 2:
                            word_list = filter(word[4], position=4, wordList=word_list) #returns length of resulting list multiplied by how likely it is to appear
                        # print("Testing word state", first_letter * 81 + second_letter * 27 + third_letter * 9 + fourth_letter * 3 + fifth_letter * 1)
                        weighted_value = len(word_list) * get_word_weighting(word, word_list, reset_list)
                        if weighted_value > 0:
                            resulting_words_list_lengths.append(len(word_list) * get_word_weighting(word, word_list, reset_list))
                        word_list = [word for word in reset_list]
    # print(word, weighted_value, resulting_words_list_lengths)
    try:
        return sum(resulting_words_list_lengths) / len(resulting_words_list_lengths)
    except:
        return len(word_list)   #returns length of list if there are no resulting word lists (impossible state)

def get_word_weighting(input_word, focused_list, main_list):    #iterates through the main list and returns the percent of filtered lists from the main list that match the focused list
    reset_list = [word for word in main_list]
    matches = 0
    for word in main_list:
        if word == input_word:
            continue
        main_list = filter_words(main_list, input_word, word)
        if main_list == focused_list:
            matches += 1
            # print("Matches found:", matches)
        main_list = reset_list
    # print(matches / len(main_list))
    return matches / len(main_list)

def get_best_next(available_words): #gets the next best word by comparing word values
    min = len(available_words)
    min_word = available_words[0]
    for word in available_words:
        print("Testing word", available_words.index(word))
        word_value = get_word_value2(word, available_words)
        if word_value < min:
            min = word_value
            min_word = word
            # print(min_word, min)
    return min_word

# def test_highestReductionButForReal2(n):  #Single-threaded algorithm, only used for reference
#     game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
#     for i in range(n):
#         available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
#         test_word = random.choice(available_words)
#         available_words = filter_words(available_words, "salet", test_word)
#         steps = 1
#         if len(available_words) == 1 and available_words[0] == test_word:
#             # print(available_words[0], "steps:", steps)
#             game_data.update({str(steps): game_data[str(steps)] + 1})
#             continue
#         elif test_word not in available_words:
#             raise RuntimeError("Answer not in list")
#         else:
#             for j in range(5):
#                 print("Step:", j + 1, "Possible words:", len(available_words))
#                 available_words = filter_words(available_words, get_best_next(available_words), test_word)
#                 steps += 1
#                 if len(available_words) == 1 and available_words[0] == test_word:
#                     # print(available_words[0], "steps:", steps)
#                     game_data.update({str(steps): game_data[str(steps)] + 1})
#                     break
#                 elif test_word not in available_words:
#                     raise RuntimeError("Answer not in list")
#                 elif j == 4 and len(available_words) != 1 and available_words[0] != test_word:
#                     game_data.update({"DNF": game_data["DNF"] + 1})
#                     break
#         print("Possible words:", len(available_words))
#         success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
#         print("hrbfr2", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))

# def getWordState(guessWord, checkWord):
#     returnv = [0,0,0,0,0]
#     in_word = ""
#     correct_pos = ""
#     for i in range(5):
#         if guessWord[i] == checkWord[i]:
#             returnv[i] = 2
#             correct_pos += guessWord[i]
#     for i in range(5):
#         if guessWord[i] in checkWord and (in_word + correct_pos).count(guessWord[i]) < checkWord.count(guessWord[i]):
#             in_word += guessWord[i]
#             returnv[i] = 1
#     return returnv

# def getWordWeight(guessWord, wordState, wordList):
#     count = 0
#     for checkWord in wordList:
#         if getWordState(guessWord, checkWord) == wordState:
#             count += 1
#     return count / len(wordList)

# def getWordScore(wordState):
#     return sum(wordState)

# def getWordValue(wordWeight, wordScore):
#     return wordWeight * wordScore

# print(getWordWeight("soare", [0, 0, 0, 0, 0], available_words))


def get_best_next_multithread(word_pool):
    min = 9999
    min_word = ""
    while len(word_pool) != 0:
        word = word_pool[0]
        # print("Testing word: " + word + "\n")
        word_value = get_word_value2(word, word_pool)
        if word_value < min:
            min = word_value
            min_word = word
            # print(min_word, word_value)
        try:
            word_pool.remove(word)
        except:
            pass
    min_word_dict.update({min_word: min})

#Taken from stackoverflow
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class Thread(threading.Thread):
   def __init__(self, targetMethod, name, wordList):
      threading.Thread.__init__(self)
      self.targetMethod = targetMethod
      self.name = name
      self.wordList = wordList
   def run(self):
    #   print("Starting " + self.name + "\n")
      self.targetMethod(self.wordList)
    #   print("Exiting " + self.name + "\n")

def runMultithreadedHRBFR2(wordList, numberOfThreads):   #gets the next best word by highest reduction, using multithreading
    global min_word_dict
    min_word_dict = {}
    wordListList = []
    wordListList.append([wordList[i:i + math.ceil(len(wordList) / numberOfThreads)] for i in range(0, len(wordList), math.ceil(len(wordList) / numberOfThreads))])
    # print(wordListList)
    if len(wordListList[0]) < numberOfThreads:
        r = len(wordListList[0])
    else:
        r = numberOfThreads
    threads = [Thread(get_best_next_multithread, "Thread " + str(i + 1), wordListList[0][i]) for i in range(r)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    # print(min_word_dict)
    if len(min_word_dict) > 1:  # tie breaker for words with the same weighted average reduction, uses original word value evaluation
        best_word_list = []
        # print(min_word_dict)
        min_value = min_word_dict[min(min_word_dict, key=min_word_dict.get)]
        for word in min_word_dict.keys():
            # print(min_word_dict[word], word)
            if min_word_dict[word] == min_value:        
                best_word_list.append(word)
        best_word = max(best_word_list, key=lambda i=word, j=get_letter_dictionary(wordList): get_word_value(i, j))
    else:
        best_word = min(min_word_dict, key=min_word_dict.get)
    return best_word
    # print("Best word:", minWord, "\n")

def test_MultiThreadedHRBFR2(n):
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        available_words = filter_words(available_words, "salet", test_word)
        steps = 1
        if len(available_words) == 1 and available_words[0] == test_word:
            # print(available_words[0], "steps:", steps, "answer:", test_word)
            game_data.update({str(steps): game_data[str(steps)] + 1})
            success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
            print("MT_HRBFR2", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
            continue
        if test_word not in available_words:
            raise RuntimeError("Answer not in list")
        for j in range(5):
            # print("Step:", j + 1, "Possible words:", len(available_words))
            available_words = filter_words(available_words, runMultithreadedHRBFR2(available_words, len(available_words)), test_word)
            steps += 1
            if len(available_words) == 1 and available_words[0] == test_word:
                # print(available_words[0], "steps:", steps, "answer:", test_word)
                game_data.update({str(steps): game_data[str(steps)] + 1})
                success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
                print("MT_HRBFR2", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
                break
            elif test_word not in available_words:
                raise RuntimeError("Answer not in list")
            elif j == 4 and len(available_words) != 1 and available_words[0] != test_word:
                # print("Did not finish", "answer:", test_word)
                game_data.update({"DNF": game_data["DNF"] + 1})
                success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
                print("MT_HRBFR2", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
                break

test_MultiThreadedHRBFR2(1000)

def gameFilter(word, wordState, word_list):   #filters words using game output information
    first_letter = int(wordState[0])
    second_letter = int(wordState[1])
    third_letter = int(wordState[2])
    fourth_letter = int(wordState[3])
    fifth_letter = int(wordState[4])
    if first_letter == 0:
        word_list = inverseFilter(word[0], word_list)
    elif first_letter == 1:
        word_list = filter(word[0], wordList=word_list)
        word_list = wrongPositionFilter(word[0], 0, word_list)
    elif first_letter == 2:
        word_list = filter(word[0], position=0, wordList=word_list)
    if second_letter == 0:
        word_list = inverseFilter(word[1], word_list)
    elif second_letter == 1:
        word_list = filter(word[1], wordList=word_list)
        word_list = wrongPositionFilter(word[1], 1, word_list)
    elif second_letter == 2:
        word_list = filter(word[1], position=1, wordList=word_list)
    if third_letter == 0:
        word_list = inverseFilter(word[2], word_list)
    elif third_letter == 1:
        word_list = filter(word[2], wordList=word_list)
        word_list = wrongPositionFilter(word[2], 2, word_list)
    elif third_letter == 2:
        word_list = filter(word[2], position=2, wordList=word_list)
    if fourth_letter == 0:
        word_list = inverseFilter(word[3], word_list)
    elif fourth_letter == 1:
        word_list = filter(word[3], wordList=word_list)
        word_list = wrongPositionFilter(word[3], 3, word_list)
    elif fourth_letter == 2:
        word_list = filter(word[3], position=3, wordList=word_list)
    if fifth_letter == 0:
        word_list = inverseFilter(word[4], word_list)
    elif fifth_letter == 1:
        word_list = filter(word[4], wordList=word_list)
        word_list = wrongPositionFilter(word[3], 3, word_list)
    elif fifth_letter == 2:
        word_list = filter(word[4], position=4, wordList=word_list)
    return word_list

def validState(wordState):  #returns whether or not a word state is valid
    if len(wordState) != 5:
        return False
    else:
        try:
            for char in wordState:
                if int(char) < 0 or int(char) > 2:
                    return False
        except:
            return False
    return True

available_words = [i[:-1] for i in open("wordsAllowed.txt", "r").readlines()]

def gameSim(wordList=available_words):  #simulates a real game
    for i in range(6):
        word = input("Enter word: ")
        wordState = input("Enter word state: ")
        while not validState(wordState):
            word = input("Enter word: ")
            wordState = input("Enter word state: ")
        wordList = gameFilter(word, wordState, wordList)
        print(runMultithreadedHRBFR2(wordList, len(wordList)))
        gameStatus = input("Complete? (y/N): ")
        if gameStatus == 'Y' or gameStatus == 'y':
            break

# gameSim()