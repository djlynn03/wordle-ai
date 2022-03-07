import random


best_pair_first_word = "starn"
best_pair_second_word = "louie"
best_first_word = "arose"
most_vowels_word = "adieu"

available_words = [i[:-1] for i in open("words.txt", "r").readlines()]

def get_letter_dictionary(word_list):
    letter_dictionary = {}
    for letter in "abcdefghijklmnopqrstuvwxyz":
        letter_dictionary.update({letter:0})
    for word in word_list:
        for letter in word:
            letter_dictionary.update({letter:(letter_dictionary[letter] + 1)})
    return letter_dictionary

letter_dictionary = get_letter_dictionary(available_words)

def run_game():
    available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
    steps = 0
    pass

def game_data_avg(game_data):
    try:
        return (game_data["1"] + 2 * game_data["2"] + 3 * game_data["3"] + 4 * game_data["4"] + 5 * game_data["5"] + 6 * game_data["6"]) / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"])
    except:
        return 0

def filter_words(available_words, guess, answer):
    return_list = [word for word in available_words]
    for int in range(len(answer)):
        if guess[int] == answer[int]:   #filters words with correct letter at specific location
            # print(guess[int], "at specific location")
            return_list = filter(guess[int], position=(int), wordList=return_list)
        if answer.count(guess[int]) > 1 and guess.count(guess[int]) > 1:    #filters words with same repetitions of letter
            # print(guess[int], "repeated", answer.count(guess[int]), "times")
            return_list = filter(guess[int], repetitions=answer.count(guess[int]), wordList=return_list)
        if guess[int] in answer:    #filters words with correct letter
            # print(guess[int], "in word")
            return_list = filter(guess[int], wordList=return_list)    
        if guess[int] not in answer:
            # print(guess[int], "not in word")
            return_list = inverseFilter(filterChar=guess[int], wordList=return_list)
    return return_list
        
def filter(filterChar, position="any", repetitions="any", wordList="none"):
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

def inverseFilter(filterChar, wordList="none"):
    returnList = []
    if wordList == "none":
        file = open("words.txt", "r")
        wordList = [line for line in file]
        file.close()
    for word in wordList:
        if filterChar not in word:
            returnList.append(word)
    return returnList

# def get_word_value(word, letter_dictionary, counted_word=""):
#     value = 0
#     counted_letters = [letter for letter in counted_word]
#     for letter in word:
#         if letter not in counted_letters:
#             value += letter_dictionary[letter]
#             counted_letters.append(letter)
#     return value

def has_common_letters(word_1, word_2):
    for letter in word_1:
        if letter in word_2:
            return True
    return False

# def get_word_value2(word, word_list):   #goes through all the combinations of letter states for the word and returns a score based on the weighted average (lower is better)
#     reset_list = [word for word in word_list]
#     resulting_words_list_lengths = []
#     for first_letter in range(3):
#         for second_letter in range(3):
#             for third_letter in range(3):
#                 for fourth_letter in range(3):
#                     for fifth_letter in range(3):
#                         if random_test == True:
#                             if random.random() < .9:    #added to speed things up
#                                 continue
#                         if first_letter == 0:
#                             word_list = inverseFilter(word[0], word_list)
#                         elif first_letter == 1:
#                             word_list = filter(word[0], wordList=word_list)
#                         elif first_letter == 2:
#                             word_list = filter(word[0], position=0, wordList=word_list)
#                         if second_letter == 0:
#                             word_list = inverseFilter(word[1], word_list)
#                         elif second_letter == 1:
#                             word_list = filter(word[1], wordList=word_list)
#                         elif second_letter == 2:
#                             word_list = filter(word[1], position=1, wordList=word_list)
#                         if third_letter == 0:
#                             word_list = inverseFilter(word[2], word_list)
#                         elif third_letter == 1:
#                             word_list = filter(word[2], wordList=word_list)
#                         elif third_letter == 2:
#                             word_list = filter(word[2], position=2, wordList=word_list)
#                         if fourth_letter == 0:
#                             word_list = inverseFilter(word[3], word_list)
#                         elif fourth_letter == 1:
#                             word_list = filter(word[3], wordList=word_list)
#                         elif fourth_letter == 2:
#                             word_list = filter(word[3], position=3, wordList=word_list)
#                         if fifth_letter == 0:
#                             word_list = inverseFilter(word[4], word_list)
#                         elif fifth_letter == 1:
#                             word_list = filter(word[4], wordList=word_list)
#                         elif fifth_letter == 2:
#                             word_list = filter(word[4], position=4, wordList=word_list) #returns length of resulting list multiplied by how likely it is to appear
#                         print("Testing word state", first_letter * 81 + second_letter * 27 + third_letter * 9 + fourth_letter * 3 + fifth_letter * 1)
#                         if random_test == True:
#                             resulting_words_list_lengths.append(len(word_list) * get_word_weighting_random(word, word_list, reset_list, 40))
#                         else:
#                             resulting_words_list_lengths.append(len(word_list) * get_word_weighting(word, word_list, reset_list))
#                         word_list = [word for word in reset_list]
#     return sum(resulting_words_list_lengths) / len(resulting_words_list_lengths)

# def get_word_weighting(input_word, focused_list, main_list):    #iterates through the main list and returns the percent of filtered lists from the main list that match the focused list
#     reset_list = [word for word in main_list]
#     matches = 0
#     for word in main_list:
#         if word == input_word:
#             continue
#         main_list = filter_words(main_list, input_word, word)
#         if main_list == focused_list:
#             matches += 1
#             print("Matches found:", matches)
#         main_list = reset_list
#     return matches / len(main_list)

# def get_word_weighting_random(input_word, focused_list, main_list, n):    #randomly chooses a number of data points in the main list and returns the percent of filtered lists from the main list that match the focused list
#     reset_list = [word for word in main_list]
#     matches = 0
#     for int in range(n):
#         word = random.choice(main_list)
#         while word == input_word:
#             word = random.choice(main_list)
#         main_list = filter_words(main_list, input_word, word)
#         if main_list == focused_list:
#             matches += 1
#             print("Matches found:", matches)
#         main_list = reset_list
#     return matches / len(main_list)

# def get_best_next(available_words):
#     max = len(available_words)
#     max_word = available_words[0]
#     for guessWord in available_words:
#         word_value = getWordValue(getWordWeight(guessWord, ), wordScore)
#         if word_value < max:
#             max = word_value
#             max_word = guessWord
#             # print(min_word, min)
#     return max_word

def getNextBest(wordList):
    maxScore = 0
    bestNext = wordList[0]
    for word in wordList:
        print("Testing word", wordList.index(word))
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    for d in range(3):
                        for e in range(3):
                            tempScore = getWordValue(getWordWeight(word, [a, b, c, d, e], wordList), getWordScore([a, b, c, d, e]))
                            # print("Testing state", a*81+b*27+c*9+d*3+e*1)
                            if tempScore > maxScore:
                                print(word.upper(), maxScore)
                                maxScore = tempScore
                                bestNext = word
    return bestNext

def getNextBestRandom(wordList, n):
    maxScore = 0
    bestNext = wordList[0]
    for i in range(n):
        word = random.choice(wordList)
        # print("Testing word", wordList.index(word))
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    for d in range(3):
                        for e in range(3):
                            tempScore = getWordValue(getWordWeight(word, [a, b, c, d, e], wordList), getWordScore([a, b, c, d, e]))
                            # print("Testing state", a*81+b*27+c*9+d*3+e*1)
                            if tempScore > maxScore:
                                print(word.upper(), maxScore)
                                maxScore = tempScore
                                bestNext = word
    return bestNext

def test_highestReductionByValue(n):
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        available_words
        available_words = filter_words(available_words, "soare", test_word)
        steps = 1
        if len(available_words) == 1 and available_words[0] == test_word:
            # print(available_words[0], "steps:", steps)
            game_data.update({str(steps): game_data[str(steps)] + 1})
            continue
        elif test_word not in available_words:
            raise RuntimeError("Answer not in list")
        for j in range(5):
            print("Step 1:", j + 1, "Possible words:", len(available_words))
            available_words = filter_words(available_words, getNextBestRandom(available_words, 100), test_word)
            steps += 1
            if len(available_words) == 1 and available_words[0] == test_word:
                # print(available_words[0], "steps:", steps)
                game_data.update({str(steps): game_data[str(steps)] + 1})
                break
            elif test_word not in available_words:
                raise RuntimeError("Answer not in list")
            elif j == 4 and len(available_words) != 1 and available_words[0] != test_word:
                game_data.update({"DNF": game_data["DNF"] + 1})
                break
        print("Possible words:", len(available_words))
        success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
        print("hrbv", (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]), game_data, success_rate, game_data_avg(game_data))

def getWordState(guessWord, checkWord):
    returnv = [0,0,0,0,0]
    in_word = ""
    correct_pos = ""
    for i in range(5):
        if guessWord[i] == checkWord[i]:
            returnv[i] = 2
            correct_pos += guessWord[i]
    for i in range(5):
        if guessWord[i] in checkWord and (in_word + correct_pos).count(guessWord[i]) < checkWord.count(guessWord[i]):
            in_word += guessWord[i]
            returnv[i] = 1
    return returnv

def getWordWeight(guessWord, wordState, wordList):
    count = 0
    for checkWord in wordList:
        if getWordState(guessWord, checkWord) == wordState:
            count += 1
    return count / len(wordList)

def getWordScore(wordState):
    return sum(wordState)

def getWordValue(wordWeight, wordScore):
    return wordWeight * wordScore

# print(getWordWeight("soare", [0, 0, 0, 0, 0], available_words))

test_highestReductionByValue(100)
