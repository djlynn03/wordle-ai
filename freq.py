# file = open("words.txt","r")
# letters = {letter: 0 for letter in 'abcdefghijklmnopqrstuvwxyz'}

# for word in file:
#     word = word[:-1]
#     for letter in word:
#         letters[letter] += 1


# [print(i) for i in dict(sorted(letters.items(), key=lambda x: x[1], reverse=True))]
# print(dict(sorted(letters.items(), key=lambda x: x[1], reverse=True)))

# file = open('lettersFreq.txt', 'w')
# file.write(str(dict(sorted(letters.items(), key=lambda x: x[1], reverse=True))))

from operator import not_
import re
available_words = [i[:-1] for i in open("words.txt", "r").readlines()]

def filter(filterChars: list | str, position="any", repetitions=1, wordList="none"):
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

def inverseFilter(filterChars: list, wordList="none"):
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

def filter3(correct_letters, in_word, not_in_word, available_words):
    '''
    correct_letters: '_____', 'abcde', 'ab_d_'
    in_word: 'fghijkl'
    not_in_word: 'abc'
    available_words: ['word1', 'word2', 'word3']
    '''
    returnv = [word for word in available_words]

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
            if containsAll(word, in_word):
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
            
    
    # if len(not_in_word) > 0:
    #     for word in returnv:
    #         if containsAny(word, not_in_word):
    #             print("REMOVED: " + word + ", " + not_in_word)
    #             returnv.remove(word)
    #         else:
    #             print(word, not_in_word)
    return returnv

def containsAll(str, set):
    """ Check whether sequence str contains ALL of the items in set. """
    return all([c in str for c in set])
 
def containsAny(str, set):
    """ Check whether sequence str contains ANY of the items in set. """
    return any([c in str for c in set])

def get_word_score(word):
    freq = {i[:-1][0]: i[:-1][2:] for i in open("lettersFreq.txt", "r").readlines()}
    return sum([int(freq[char.upper()]) for char in set(word)])
        


# available_words = filter("_____", "sort", "adieu", available_words)
# print(available_words)
# word_list = [line[:-1] for line in open("words.txt", "r")]
# available_words = filter()
# mx = 0
# mx_word = ""
# for word1 in available_words:
#     for word2 in available_words:
#         if get_word_score(word1+word2) > mx:
#             mx = get_word_score(word1+word2)
#             mx_word = word1 + ", " + word2
#             print(mx_word, mx)

# print(max(available_words, key=get_word_score))

# print(max(available_words, key=get_word_score))
available_words = filter3("_____", "", "seaoriltnd", available_words)
print(max(available_words, key=get_word_score))
# print(max(available_words, key=get_word_score))
# for word in available_words:
    
# print(get_word_score("sorts"))