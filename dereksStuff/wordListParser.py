# This file is used to count the letters in all of the valid words
# The word frequency list has already been created, so the write command has been commented out
available_words = [i[:-1] for i in open("words2.txt", "r").readlines()]
letter_dictionary = {}
for letter in "abcdefghijklmnopqrstuvwxyz":
    letter_dictionary.update({letter:0})
for word in available_words:
    for letter in word:
        letter_dictionary.update({letter:(letter_dictionary[letter] + 1)})
print(letter_dictionary)
letter_list = [letter + " " + str(letter_dictionary[letter]) for letter in letter_dictionary]
for line in letter_list:
    open("letterFreq.txt", "a").write(line + "\n")

def get_word_value(word, counted_word=""):
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

# best_word_1 = "starn"
# best_word_2 = "louie"

# max_score = 0
# for word_1 in available_words:
#     for word_2 in available_words:
#         if not has_common_letters(word_1, word_2):
#             if (get_word_value(word_1) + get_word_value(word_2)) > max_score:
#                 max_score = get_word_value(word_1) + get_word_value(word_2)
#                 best_word_1 = word_1
#                 best_word_2 = word_2
#                 print(word_1, word_2, max_score)
# print("The best first pair is", best_word_1, best_word_2)

# best_word_3 = "dampy"
# max_score = 0
# for word_3 in available_words:
#         if get_word_value(word_3, best_word_1 + best_word_2) > max_score:
#             max_score = get_word_value(word_3, best_word_1 + best_word_2)
#             best_word_3 = word_3
#             print(word_3, max_score)
# print("The best third word is", best_word_3)

# best_word_4 = "chowk"
# max_score = 0
# for word_4 in available_words:
#         if get_word_value(word_4, best_word_1 + best_word_2 + best_word_3) > max_score:
#             max_score = get_word_value(word_4, best_word_1 + best_word_2 + best_word_3)
#             best_word_4 = word_4
#             print(word_4, max_score)
# print("The best fourth word is", best_word_4)

# best_word_5 = "befog"
# max_score = 0
# for word_5 in available_words:
#         if get_word_value(word_5, best_word_1 + best_word_2 + best_word_3 + best_word_4) > max_score:
#             max_score = get_word_value(word_5, best_word_1 + best_word_2 + best_word_3 + best_word_4)
#             best_word_5 = word_5
#             print(word_5, max_score)
# print("The best fifth word is", best_word_5)