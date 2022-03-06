import re
available_words = [i[:-1] for i in open("words2.txt", "r").readlines()]


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
        
# Prints the best possible word that doesn't include the letters in the first two words
available_words = filter3("_____", "", "aeros", available_words)
print(max(available_words, key=get_word_score))
