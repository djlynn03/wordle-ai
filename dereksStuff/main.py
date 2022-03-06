import random
from re import A
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

def maxTop(word_list, letter_dictionary):
    count = 0
    best_words = []
    for word in word_list:
        if count > 1000:
            break
        max_value = 0
        max_word = word_list[0]
        for word in word_list:
            if get_word_value(word, letter_dictionary) > max_value:
                max_value = get_word_value(word, letter_dictionary)
                max_word = word
        best_words.append(max_word)
        count += 1
    letter_dictionary = get_letter_dictionary(best_words)
    return max(best_words, key= lambda i=word, j=letter_dictionary: get_word_value(i, j))

def game_data_avg(game_data):
    try:
        return (game_data["1"] + 2 * game_data["2"] + 3 * game_data["3"] + 4 * game_data["4"] + 5 * game_data["5"] + 6 * game_data["6"]) / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"])
    except:
        return 0

def test_algorithm6(n):
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
    letter_dictionary = get_letter_dictionary(available_words)
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        available_words = filter_words(available_words, best_pair_first_word, test_word)
        # print(available_words)
        available_words = filter_words(available_words, best_pair_second_word, test_word)
        # print(available_words)
        steps = 2
        for int in range(4):
            if len(available_words) <= (5 - int):   #if the number of possible answers are less than the guesses left, it will randomly guess
                available_words = filter_words(available_words, random.choice(available_words), test_word)
                steps += 1
            else:
                min = len(available_words)
                letter_dictionary = get_letter_dictionary(available_words)
                for j in range(100):
                    guess = random.choice(available_words)
                    guess_words_length = len(filter_words(available_words, guess, maxTop(available_words, letter_dictionary)))
                    if guess_words_length < min:
                        highestReductionWord = guess
                        min = guess_words_length
                available_words = filter_words(available_words, highestReductionWord, test_word)
                steps += 1
            if len(available_words) == 1 and available_words[0] == test_word:
                # print(available_words[0], "steps:", steps)
                game_data.update({str(steps): game_data[str(steps)] + 1})
            elif test_word not in available_words:
                raise RuntimeError("Answer not in list")
        if len(available_words) != 1 and available_words[0] != test_word:
            game_data.update({"DNF": game_data["DNF"] + 1})
        success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
        print("6", game_data, success_rate, game_data_avg(game_data))

def test_bestFirstPairHighestReductionDynamicDictionary(n):
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    letter_dictionary = get_letter_dictionary(available_words)
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        available_words = filter_words(available_words, best_pair_first_word, test_word)
        # print(available_words)
        available_words = filter_words(available_words, best_pair_second_word, test_word)
        # print(available_words)
        steps = 2
        for int in range(4):
            if len(available_words) <= (5 - int):   #if the number of possible answers are less than the guesses left, it will randomly guess
                available_words = filter_words(available_words, random.choice(available_words), test_word)
                steps += 1
            else:
                min = len(available_words)
                letter_dictionary = get_letter_dictionary(available_words)
                for j in range(100):
                    guess = random.choice(available_words)
                    guess_words_length = len(filter_words(available_words, guess, max(available_words, key= lambda i=guess, j=letter_dictionary: get_word_value(i, j))))
                    if guess_words_length < min:
                        highestReductionWord = guess
                        min = guess_words_length
                available_words = filter_words(available_words, highestReductionWord, test_word)
                steps += 1
            if len(available_words) == 1 and available_words[0] == test_word:
                # print(available_words[0], "steps:", steps)
                game_data.update({str(steps): game_data[str(steps)] + 1})
            elif test_word not in available_words:
                raise RuntimeError("Answer not in list")
        if len(available_words) != 1 and available_words[0] != test_word:
            game_data.update({"DNF": game_data["DNF"] + 1})
        success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
        print("bestFirstPairHighestReductionDynamicDictionary", game_data, success_rate, game_data_avg(game_data))

def test_bestFirstPairHighestReduction(n):
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        available_words = filter_words(available_words, best_pair_first_word, test_word)
        # print(available_words)
        available_words = filter_words(available_words, best_pair_second_word, test_word)
        # print(available_words)
        steps = 2
        for int in range(4):
            if len(available_words) <= (5 - int):   #if the number of possible answers are less than the guesses left, it will randomly guess
                available_words = filter_words(available_words, random.choice(available_words), test_word)
                steps += 1
            else:
                min = len(available_words)
                for j in range(100):
                    guess = random.choice(available_words)
                    guess_words_length = len(filter_words(available_words, guess, max(available_words, key=get_word_value)))
                    if guess_words_length < min:
                        highestReductionWord = guess
                        min = guess_words_length
                available_words = filter_words(available_words, highestReductionWord, test_word)
                steps += 1
            if len(available_words) == 1 and available_words[0] == test_word:
                # print(available_words[0], "steps:", steps)
                game_data.update({str(steps): game_data[str(steps)] + 1})
            elif test_word not in available_words:
                raise RuntimeError("AnswerNotInList")
        if len(available_words) != 1 and available_words[0] != test_word:
            game_data.update({"DNF": game_data["DNF"] + 1})
        success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
        print("bestFirstPairHighestReduction", game_data, success_rate, game_data_avg(game_data))

def test_highestReduction(n):
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        steps = 0
        for int in range(6):
            if len(available_words) <= (5 - int):   #if the number of possible answers are less than the guesses left, it will randomly guess
                available_words = filter_words(available_words, random.choice(available_words), test_word)
            else:
                min = len(available_words)
                for i in range(10):
                    guess = random.choice(available_words)
                    guess_words_length = len(filter_words(available_words, guess, max(available_words, key= lambda guess, letter_dictionary: get_word_value(guess,letter_dictionary))))
                    if guess_words_length < min:
                        highestReductionWord = guess
                        min = guess_words_length
                available_words = filter_words(available_words, highestReductionWord, test_word)
                steps += 1
            if len(available_words) == 1 and available_words[0] == test_word:
                # print(available_words[0], "steps:", steps)
                game_data.update({str(steps): game_data[str(steps)] + 1})
            elif test_word not in available_words:
                raise RuntimeError("Answer not in list")
        if len(available_words) != 1 and available_words[0] != test_word:
            game_data.update({"DNF": game_data["DNF"] + 1})
        success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
        print("highestReduction", game_data, success_rate, game_data_avg(game_data))

def test_firstPairBest(n):
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        available_words = filter_words(available_words, best_pair_first_word, test_word)
        # print(available_words)
        available_words = filter_words(available_words, best_pair_second_word, test_word)
        # print(available_words)
        steps = 2
        for i in range(4):
            if len(available_words) <= (5 - int):   #if the number of possible answers are less than the guesses left, it will randomly guess
                available_words = filter_words(available_words, random.choice(available_words), test_word)
            else:
                available_words = filter_words(available_words, max(available_words, key=get_word_value), test_word)
                steps += 1
            if len(available_words) == 1 and available_words[0] == test_word:
                # print(available_words[0], "steps:", steps)
                game_data.update({str(steps): game_data[str(steps)] + 1})
            elif test_word not in available_words:
                raise RuntimeError("AnswerNotInList")
        if len(available_words) != 1 and available_words[0] != test_word:
            game_data.update({"DNF": game_data["DNF"] + 1})
        success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
        print("firstPairBest", game_data, success_rate, game_data_avg(game_data))

def test_BestFirst(n):
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        steps = 0
        for int in range(6):
            if len(available_words) <= (5 - int):   #if the number of possible answers are less than the guesses left, it will randomly guess
                available_words = filter_words(available_words, random.choice(available_words), test_word)
            available_words = filter_words(available_words, max(available_words, key=get_word_value), test_word)
            steps += 1
            if len(available_words) == 1 and available_words[0] == test_word:
                # print(available_words[0], "steps:", steps)
                game_data.update({str(steps): game_data[str(steps)] + 1})
            elif test_word not in available_words:
                raise RuntimeError("AnswerNotInList")
        if len(available_words) != 1 and available_words[0] != test_word:
            game_data.update({"DNF": game_data["DNF"] + 1})
        success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
        print("bestFirst", game_data, success_rate, game_data_avg(game_data))
        
    
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

def get_word_value(word, letter_dictionary, counted_word=""):
    value = 0
    counted_letters = [letter for letter in counted_word]
    for letter in word:
        if letter not in counted_letters:
            value += letter_dictionary[letter]
            counted_letters.append(letter)
    return value

def has_common_letters(word_1, word_2):
    for letter in word_1:
        if letter in word_2:
            return True
    return False

# test_highestReduction(1000)
# test_firstPairBest(1000)
# test_BestFirst(1000)
# test_bestFirstPairHighestReduction(1000)
# test_bestFirstPairHighestReductionDynamicDictionary(1000)
# test_algorithm6(1000)

def get_word_value2(word, word_list):   #lower is better
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
                        elif first_letter == 2:
                            word_list = filter(word[0], position=0, wordList=word_list)
                        if second_letter == 0:
                            word_list = inverseFilter(word[1], word_list)
                        elif second_letter == 1:
                            word_list = filter(word[1], wordList=word_list)
                        elif second_letter == 2:
                            word_list = filter(word[1], position=1, wordList=word_list)
                        if third_letter == 0:
                            word_list = inverseFilter(word[2], word_list)
                        elif third_letter == 1:
                            word_list = filter(word[2], wordList=word_list)
                        elif third_letter == 2:
                            word_list = filter(word[2], position=2, wordList=word_list)
                        if fourth_letter == 0:
                            word_list = inverseFilter(word[3], word_list)
                        elif fourth_letter == 1:
                            word_list = filter(word[3], wordList=word_list)
                        elif fourth_letter == 2:
                            word_list = filter(word[3], position=3, wordList=word_list)
                        if fifth_letter == 0:
                            word_list = inverseFilter(word[4], word_list)
                        elif fifth_letter == 1:
                            word_list = filter(word[4], wordList=word_list)
                        elif fifth_letter == 2:
                            word_list = filter(word[4], position=4, wordList=word_list)
                        resulting_words_list_lengths.append(len(word_list))
                        word_list = [word for word in reset_list]
    return sum(resulting_words_list_lengths) / 243

def get_word_value4(word, word_list):   #lower is better
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
                        elif first_letter == 2:
                            word_list = filter(word[0], position=0, wordList=word_list)
                        if second_letter == 0:
                            word_list = inverseFilter(word[1], word_list)
                        elif second_letter == 1:
                            word_list = filter(word[1], wordList=word_list)
                        elif second_letter == 2:
                            word_list = filter(word[1], position=1, wordList=word_list)
                        if third_letter == 0:
                            word_list = inverseFilter(word[2], word_list)
                        elif third_letter == 1:
                            word_list = filter(word[2], wordList=word_list)
                        elif third_letter == 2:
                            word_list = filter(word[2], position=2, wordList=word_list)
                        if fourth_letter == 0:
                            word_list = inverseFilter(word[3], word_list)
                        elif fourth_letter == 1:
                            word_list = filter(word[3], wordList=word_list)
                        elif fourth_letter == 2:
                            word_list = filter(word[3], position=3, wordList=word_list)
                        if fifth_letter == 0:
                            word_list = inverseFilter(word[4], word_list)
                        elif fifth_letter == 1:
                            word_list = filter(word[4], wordList=word_list)
                        elif fifth_letter == 2:
                            word_list = filter(word[4], position=4, wordList=word_list)
                            for word2 in word_list:
                                for first_letter2 in range(3):
                                        for second_letter2 in range(3):
                                            for third_letter2 in range(3):
                                                for fourth_letter2 in range(3):
                                                    for fifth_letter2 in range(3):
                                                        if first_letter2 == 0:
                                                            word_list2 = inverseFilter(word2[0], word_list)
                                                        elif first_letter2 == 1:
                                                            word_list2 = filter(word2[0], wordList=word_list)
                                                        elif first_letter2 == 2:
                                                            word_list2 = filter(word2[0], position=0, wordList=word_list)
                                                        if second_letter2 == 0:
                                                            word_list2 = inverseFilter(word2[1], word_list)
                                                        elif second_letter2 == 1:
                                                            word_list2 = filter(word2[1], wordList=word_list)
                                                        elif second_letter2 == 2:
                                                            word_list2 = filter(word2[1], position=1, wordList=word_list)
                                                        if third_letter2 == 0:
                                                            word_list2 = inverseFilter(word2[2], word_list)
                                                        elif third_letter2 == 1:
                                                            word_list2 = filter(word2[2], wordList=word_list)
                                                        elif third_letter2 == 2:
                                                            word_list2 = filter(word2[2], position=2, wordList=word_list)
                                                        if fourth_letter2 == 0:
                                                            word_list2 = inverseFilter(word2[3], word_list)
                                                        elif fourth_letter2 == 1:
                                                            word_list2 = filter(word2[3], wordList=word_list)
                                                        elif fourth_letter2 == 2:
                                                            word_list2 = filter(word2[3], position=3, wordList=word_list)
                                                        if fifth_letter2 == 0:
                                                            word_list2 = inverseFilter(word2[4], word_list)
                                                        elif fifth_letter2 == 1:
                                                            word_list2 = filter(word2[4], wordList=word_list)
                                                        elif fifth_letter2 == 2:
                                                            word_list2 = filter(word2[4], position=4, wordList=word_list)
                                                            resulting_words_list_lengths.append(len(word_list2))
    return sum(resulting_words_list_lengths) / (243 ** 2)

def get_best_next(available_words):
    min = len(available_words)
    min_word = available_words[0]
    for word in available_words:
        word_value = get_word_value2(word, available_words)
        if word_value < min:
            min = word_value
            min_word = word
            # print(min_word, min)
        if available_words.index(word) % 100 == 0:
            print(available_words.index(word))
    print(min_word)
    return min_word

def test_highestReductionButForReal(n):
    game_data = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "DNF": 0}
    for i in range(n):
        available_words = [i[:-1] for i in open("words.txt", "r").readlines()]
        test_word = random.choice(available_words)
        available_words = filter_words(available_words, "toeas", test_word)
        steps = 1
        if len(available_words) == 1 and available_words[0] == test_word:
            # print(available_words[0], "steps:", steps)
            game_data.update({str(steps): game_data[str(steps)] + 1})
            continue
        elif test_word not in available_words:
            raise RuntimeError("Answer not in list")
        print(available_words)
        for int in range(5):
            available_words = filter_words(available_words, get_best_next(available_words), test_word)
            steps += 1
            if len(available_words) == 1 and available_words[0] == test_word:
                # print(available_words[0], "steps:", steps)
                game_data.update({str(steps): game_data[str(steps)] + 1})
            elif test_word not in available_words:
                raise RuntimeError("Answer not in list")
            # print(available_words)
        if len(available_words) != 1 and available_words[0] != test_word:
            game_data.update({"DNF": game_data["DNF"] + 1})
        success_rate = 1 - (game_data["DNF"] / (game_data["1"] + game_data["2"] + game_data["3"] + game_data["4"] + game_data["5"] + game_data["6"] + game_data["DNF"]))
        print("hrbfr", game_data, success_rate, game_data_avg(game_data))
        
test_highestReductionButForReal(100)