import random
import threading
import math

available_words = [i[:-1] for i in open("words.txt", "r").readlines()]  #list of all possible answers
wordsAllowed = [i[:-1] for i in open("wordsAllowed.txt", "r").readlines()]  #list of all possible entries

def get_letter_dictionary(word_list):   #gets a letter dictionary of the each letter and the number of times it appears in the word list
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

def repetition_filter(char, num_repetitions, wordList, exact):  #filters out words with incorrect number of character repetitions
    if exact:
        for word in wordList:
            if word.count(char) != num_repetitions:
                wordList.remove(word)
    else:
        for word in wordList:
            if word.count(char) < num_repetitions:
                wordList.remove(word)
    return wordList

def filter_words(return_list, guess, answer):   #returns a list of possible words left, given a guess and an answer
    for int in range(len(answer)):
        if guess[int] == answer[int]:   #filters words with correct letter at specific location
            # print(guess[int], "at specific location")
            return_list = filter(guess[int], position=(int), wordList=return_list)
        elif guess[int] in answer:    #filters words with correct letter present
            # print(guess[int], "in word")
            return_list = filter(guess[int], wordList=return_list)   
            return_list = wrongPositionFilter(guess[int], int, wordList=return_list) 
        elif guess[int] not in answer:  #filters out words with invalid letter in word
            # print(guess[int], "not in word")
            return_list = inverseFilter(filterChar=guess[int], wordList=return_list)
    for char in guess:
        if not guess.count(char) > 1 or not answer.count(char) > 1:
            continue
        if guess.count(char) <= answer.count(char): # "beers" "peees"
            return_list = repetition_filter(char, guess.count(char), return_list, False)  # we know the answer has at least guess.count(char) characters
        else: # guess count > answer count
            return_list = repetition_filter(char, answer.count(char), return_list, True) # answer count has the exact correct occurences of char
    return return_list

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

def word_state_repetition_filter(word, wordState, word_list):  #filters out words with incorrect number of character repetitions using a word state
    # 1 identify repetitions in word
    repeatedChars = {i: word.count(i) for i in list(set(word)) if word.count(i) > 1}
    charRepetitions = {i: 0 for i in repeatedChars.keys()}
    for char in repeatedChars.keys():
        for i in range(5):
            if word[i] == char and wordState[i] != "0":
                repeatedChars[char] -= 1
                charRepetitions[char] += 1
    for char in repeatedChars.keys():
        word_list = repetition_filter(char, charRepetitions[char], word_list, repeatedChars[char] != 0)
    return word_list

def get_word_value(word, letter_dictionary, counted_word=""):   #gets the word value based off of the frequency of the letters in the letter dictionary
    value = 0
    counted_letters = [letter for letter in counted_word]
    for letter in word:
        if letter not in counted_letters:
            value += letter_dictionary[letter]
            counted_letters.append(letter)
    return value

def isBlimp(wordList):   #returns whether or not a word list has the "blimp problem"
    if len(wordList) > 10 or len(wordList) < 3:
        return False
    threshold = math.floor(len(wordList)/2)
    commonLettersDict = {}
    for word1 in wordList:
        for word2 in wordList:
            if word2 == word1:
                continue
            if len(list(set(word1) & set(word2))) >= 3: # if words have at least 3 letters in common
                commonLetters = ""
                for letters in list(set(word1) & set(word2)):
                    commonLetters += letters
                commonLetters = "".join(sorted(commonLetters))
                try:
                    commonLettersDict[commonLetters] += 1
                    if commonLettersDict[commonLetters] >= threshold:
                        return True
                except:
                    commonLettersDict[commonLetters] = 1
    return False

def getBlimpMax(wordList, commonLetters, totalWords=wordsAllowed): #returns highest word by letter frequency, excluding letters in common with most possible answers
    letterDictionary = get_letter_dictionary(wordList)
    wordValues = {word:get_word_value(word, letterDictionary, commonLetters) for word in totalWords}
    return max(wordValues, key=wordValues.get)

def blimpSearch(wordList):  #made to avoid the "blimp problem" where a search would be narrowed down best by a word already filtered out
    threshold = math.floor(len(wordList)/2) # ex: match, batch, latch are possible answers, blimp would be a good filter word
    commonLettersDict = {}
    blimpWords = {}
    for word1 in wordList:
        for word2 in wordList:
            if word2 == word1:
                continue
            if len(list(set(word1) & set(word2))) >= 3: # if words have at least 3 letters in common
                commonLetters = ""
                for letters in list(set(word1) & set(word2)):
                    commonLetters += letters
                commonLetters = "".join(sorted(commonLetters))
                try:
                    commonLettersDict[commonLetters] += 1
                except:
                    commonLettersDict[commonLetters] = 1
    for commonLetters in commonLettersDict:
        if commonLettersDict[commonLetters] >= threshold:
            blimpWord = getBlimpMax(wordList, commonLetters)
            blimpWords.update({blimpWord: get_word_value(blimpWord, get_letter_dictionary(wordList), commonLetters)})
    return max(blimpWords, key=blimpWords.get)

def get_word_value2(word, reset_list):   #goes through all the combinations of letter states for the word and returns a score based on the weighted average list reduction (lower is better)
    word_list = reset_list
    resulting_words_list_lengths = []
    lettersInWord = []
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
                            lettersInWord.append(word[0])
                        elif first_letter == 2:
                            word_list = filter(word[0], position=0, wordList=word_list)
                            lettersInWord.append(word[0])
                        if second_letter == 0:
                            if word[1] not in lettersInWord:
                                word_list = inverseFilter(word[1], word_list)
                        elif second_letter == 1:
                            word_list = filter(word[1], wordList=word_list)
                            word_list = wrongPositionFilter(word[1], 1, word_list)
                            lettersInWord.append(word[1])
                        elif second_letter == 2:
                            word_list = filter(word[1], position=1, wordList=word_list)
                            lettersInWord.append(word[1])
                        if third_letter == 0:
                            if word[2] not in lettersInWord:
                                word_list = inverseFilter(word[2], word_list)
                        elif third_letter == 1:
                            word_list = filter(word[2], wordList=word_list)
                            word_list = wrongPositionFilter(word[2], 2, word_list)
                            lettersInWord.append(word[2])
                        elif third_letter == 2:
                            word_list = filter(word[2], position=2, wordList=word_list)
                            lettersInWord.append(word[2])
                        if fourth_letter == 0:
                            if word[3] not in lettersInWord:
                                word_list = inverseFilter(word[3], word_list)
                        elif fourth_letter == 1:
                            word_list = filter(word[3], wordList=word_list)
                            word_list = wrongPositionFilter(word[3], 3, word_list)
                            lettersInWord.append(word[3])
                        elif fourth_letter == 2:
                            word_list = filter(word[3], position=3, wordList=word_list)
                            lettersInWord.append(word[3])
                        if fifth_letter == 0:
                            if word[4] not in lettersInWord:
                                word_list = inverseFilter(word[4], word_list)
                        elif fifth_letter == 1:
                            word_list = filter(word[4], wordList=word_list)
                            word_list = wrongPositionFilter(word[3], 3, word_list)
                            lettersInWord.append(word[4])
                        elif fifth_letter == 2:
                            word_list = filter(word[4], position=4, wordList=word_list)
                            lettersInWord.append(word[4])
                        wordState = str(first_letter) + str(second_letter) + str(third_letter) + str(fourth_letter) + str(fifth_letter)
                        if len(set(list(word))) != len(word):
                            word_list = word_state_repetition_filter(word, wordState, word_list)
                        # print("Testing word state", first_letter * 81 + second_letter * 27 + third_letter * 9 + fourth_letter * 3 + fifth_letter * 1)
                        # print(word, wordState, word_list)
                        if len(word_list) > 0:
                            resulting_words_list_lengths.append(0 - (len(reset_list) - len(word_list)) * get_list_matches(word, word_list, reset_list)) # made this negative so I didn't have to rewrite code
                        # print(resulting_words_list_lengths)
                        word_list = reset_list
    # print(word, weighted_value, resulting_words_list_lengths)
    if len(resulting_words_list_lengths) > 0:
        return sum(resulting_words_list_lengths) / len(reset_list)    #returns sum of weighted averages
    else:
        return 1   #returns -1 if there are no resulting word lists (all states are impossible to reach)

def get_list_matches(input_word, focused_list, main_list):    #iterates through the main list and returns the number of filtered lists from the main list that match the focused list
    reset_list = [word for word in main_list]
    matches = 0
    for word in main_list:
        main_list = filter_words(main_list, input_word, word)
        if main_list == focused_list:
            matches += 1
            # print("Matches found:", matches)
        main_list = reset_list
    # print(matches / len(main_list))
    return matches

def get_best_next_multithread(word_pool, totalWordList):    #multithreading-compatible method to get candidates for the best next word by weighted highest reduction average
    global min_word_dict
    minimum = get_word_value2(word_pool[0], totalWordList)
    min_word = word_pool[0]
    while len(word_pool) != 0:
        word = word_pool[0]
        # print("Testing word: " + word + "\n")
        word_value = get_word_value2(word, totalWordList)
        if word_value != 1 and word_value < min_word_dict[min(min_word_dict, key=min_word_dict.get)]:
            minimum = word_value
            min_word = word
        word_pool.remove(word)
    min_word_dict.update({min_word: minimum})

def chunks(list, n):
    """Yield successive n-sized chunks from list."""
    for i in range(0, len(list), n):
        yield list[i:i + n]

class Thread(threading.Thread): #custom thread class
   def __init__(self, targetMethod, name, wordList, totalWordList):
      threading.Thread.__init__(self)
      self.targetMethod = targetMethod
      self.name = name
      self.wordList = wordList
      self.totalWordList = totalWordList
   def run(self):
    #   print("Starting " + self.name + "\n")
      self.targetMethod(self.wordList, self.totalWordList)
    #   print("Exiting " + self.name + "\n")

def getMaxValue1(wordList): #returns highest word by letter frequency
    letterDictionary = get_letter_dictionary(wordList)
    wordValues = {word:get_word_value(word, letterDictionary) for word in wordList}
    return max(wordValues, key=wordValues.get)

def runMultithreadedHRBFR2(wordList, numberOfThreads):   #gets the next best word by highest reduction, using multithreading
    global min_word_dict
    min_word_dict = {"zzzzz": 9999}
    wordListList = []
    wordListList.append([wordList[i:i + math.ceil(len(wordList) / numberOfThreads)] for i in range(0, len(wordList), math.ceil(len(wordList) / numberOfThreads))])
    if len(wordListList[0]) < numberOfThreads:
        r = len(wordListList[0])
    else:
        r = numberOfThreads
    threads = [Thread(get_best_next_multithread, "Thread " + str(i + 1), wordListList[0][i], wordList) for i in range(r)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    if len(min_word_dict) > 1:  # returns the word with the lowest score out of all the local minimums
        print(min_word_dict)
        best_word_list = []
        min_value = min_word_dict[min(min_word_dict, key=min_word_dict.get)]
        # print(min_value)
        for word in min_word_dict.keys():
            if min_word_dict[word] == min_value:        
                best_word_list.append(word)
        best_word = getMaxValue1(best_word_list)
        # print(best_word, best_word_list)
    else:
        best_word = min(min_word_dict, key=min_word_dict.get)
    return best_word

def test_MultiThreadedHRBFR2(n):    #tests deep search by highest weighted average list reduction
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        print(test_word)
        steps = 1
        if test_word == "salet":
            print(steps, available_words)
            game_data.update({str(steps): game_data[str(steps)] + 1})
            success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
            print("MT_HRBFR2", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
            continue
        available_words = filter_words(available_words, "salet", test_word)
        if test_word not in available_words:
            raise RuntimeError("Answer not in list")
        if len(available_words) == 1 and available_words[0] == test_word:
            steps += 1
            # print(steps, available_words)
            game_data.update({str(steps): game_data[str(steps)] + 1})
            success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
            print("MT_HRBFR2", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
            continue
        for j in range(5):
            available_words = filter_words(available_words, runMultithreadedHRBFR2(available_words, 100), test_word)
            steps += 1
            # print(steps, available_words)
            if test_word not in available_words:
                raise RuntimeError("Answer not in list")
            if len(available_words) == 1 and available_words[0] == test_word:
                game_data.update({str(steps): game_data[str(steps)] + 1})
                success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
                print("MT_HRBFR2", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
                break     
        else:
            game_data.update({"DNF": game_data["DNF"] + 1})
            success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
            print("MT_HRBFR2", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))

# test_MultiThreadedHRBFR2(1)

def gameFilter(word, wordState, word_list):   #filters words using game output information
    first_letter = int(wordState[0])
    second_letter = int(wordState[1])
    third_letter = int(wordState[2])
    fourth_letter = int(wordState[3])
    fifth_letter = int(wordState[4])
    lettersInWord = [word[i] for i in range(0, 5) if wordState[i] == "1" or wordState[i] == "2"]
    if first_letter == 0:
        if word[0] not in lettersInWord:
            word_list = inverseFilter(word[0], word_list)
    elif first_letter == 1:
        word_list = filter(word[0], wordList=word_list)
        word_list = wrongPositionFilter(word[0], 0, word_list)
    elif first_letter == 2:
        word_list = filter(word[0], position=0, wordList=word_list)
    if second_letter == 0:
        if word[1] not in lettersInWord:
            word_list = inverseFilter(word[1], word_list)
    elif second_letter == 1:
        word_list = filter(word[1], wordList=word_list)
        word_list = wrongPositionFilter(word[1], 1, word_list)
    elif second_letter == 2:
        word_list = filter(word[1], position=1, wordList=word_list)
    if third_letter == 0:
        if word[2] not in lettersInWord:
            word_list = inverseFilter(word[2], word_list)
    elif third_letter == 1:
        word_list = filter(word[2], wordList=word_list)
        word_list = wrongPositionFilter(word[2], 2, word_list)
    elif third_letter == 2:
        word_list = filter(word[2], position=2, wordList=word_list)
    if fourth_letter == 0:
        if word[3] not in lettersInWord:
            word_list = inverseFilter(word[3], word_list)
    elif fourth_letter == 1:
        word_list = filter(word[3], wordList=word_list)
        word_list = wrongPositionFilter(word[3], 3, word_list)
    elif fourth_letter == 2:
        word_list = filter(word[3], position=3, wordList=word_list)
    if fifth_letter == 0:
        if word[4] not in lettersInWord:
            word_list = inverseFilter(word[4], word_list)
    elif fifth_letter == 1:
        word_list = filter(word[4], wordList=word_list)
        word_list = wrongPositionFilter(word[4], 4, word_list)
    elif fifth_letter == 2:
        word_list = filter(word[4], position=4, wordList=word_list)
    if len(set(list(word))) != len(word):
        word_list = word_state_repetition_filter(word, wordState, word_list)
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

def test_highestFrequency(n):   #tests search using letter frequencies
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        # print(test_word)
        steps = 1
        if test_word == "salet":
            # print(steps, available_words)
            game_data.update({str(steps): game_data[str(steps)] + 1})
            success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
            print("MT_HRBFR2", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
            continue
        available_words = filter_words(available_words, "salet", test_word)
        if test_word not in available_words:
            raise RuntimeError("Answer not in list")
        if len(available_words) == 1 and available_words[0] == test_word:
            steps += 1
            # print(steps, available_words)
            game_data.update({str(steps): game_data[str(steps)] + 1})
            success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
            print("highest_freq", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
            continue
        for j in range(5):
            if isBlimp(available_words):
                guessWord = blimpSearch(available_words)
            else:
                guessWord = getMaxValue1(available_words)
            available_words = filter_words(available_words, guessWord, test_word)
            steps += 1
            # print(steps, available_words)
            if test_word not in available_words:
                raise RuntimeError("Answer not in list")
            if len(available_words) == 1 and available_words[0] == test_word:
                game_data.update({str(steps): game_data[str(steps)] + 1})
                success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
                print("highest_freq", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
                break     
        else:
            game_data.update({"DNF": game_data["DNF"] + 1})
            success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
            print("highest_freq", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))
            
# test_highestFrequency(1000)