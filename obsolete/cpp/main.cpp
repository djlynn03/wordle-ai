/* -----------------------------------------------------------------------------
 *
 * File Name:  main.cpp
 * Author: Derek Zhang and Duncan Lynn
 * Description:  This program will attempt to find the optimal words to solve Wordle
 * Last Updated: 3/6/2022
 *
 ---------------------------------------------------------------------------- */

#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <random>
#include <algorithm>
#include <numeric>
#include <ctime>

std::unordered_map<int, int> gameData;
std::vector<std::string> wordList;
std::vector<std::string> filter(std::string correctLetters, std::string inWord, std::string notInWord, std::vector<std::string> wordList);
void printList(std::vector<std::string> wordList);
bool inWordFilter(std::string inWord, std::string word);
bool correctLettersFilter(std::string correctLetters, std::string word);
bool notInWordFilter(std::string notInWord, std::string word);
double getWordWeighting(std::string word, std::vector<std::string> wordList, std::vector<std::string> focusedList);
std::vector<std::string> checkFilter(std::vector<std::string> wordList, std::string guessWord, std::string checkWord);
double getWordValue(std::string word, std::vector<std::string> wordList);
std::vector<std::string> repetitionFilter(char c, std::vector<std::string> wordList);

std::vector<std::string> populateWordList()    //populates a list with the provided .txt file
{
    // std::cout << "Populating\n";
    std::ifstream inFile;
    std::string word = "";
    std::vector<std::string> returnVector;
    inFile.open("words1.txt");
    while(std::getline(inFile, word))
    {
        // std::cout << word << "\n";
        returnVector.push_back(word);
    }
    inFile.close();
    return returnVector;
}

std::string generateRandomWord(std::vector<std::string> wordList)
{
    // std::cout << floor(((double) rand() / RAND_MAX) * wordList->size()) << "\n";
    srand((unsigned int)time(NULL));
    return wordList.at(floor(((double) rand() / RAND_MAX) * wordList.size()));
}

int main()
{
    // std::cout << "Main\n";
    std::vector<std::string> wordList = populateWordList();
    std::string randomWord = generateRandomWord(wordList);
    std::cout << "Current word: " << randomWord << "\n";

    // wordList = filter("_ea__", "b", "zxcvnm", wordList);
    // wordList = checkFilter(wordList, std::string{"beans"}, std::string{"brain"});
    // std::cout << wordList.size() << "\n";
    std::cout << getWordValue(randomWord, wordList);
    printList(wordList);
    return 0;
}

std::vector<std::string> filter(std::string correctLetters, std::string inWord, std::string notInWord, std::vector<std::string> wordList)    //returns a filtered word list based on the inclusion of a character
{
    // std::cout << correctLetters << " " << inWord << " " << notInWord << "\n";
    // std::cout << "Filtering\n";
    if(correctLetters.size() + inWord.size() + notInWord.size() == 0)
    {
        return wordList;
    }
    std::vector<std::string> returnVector;
    for(int i = 0; i < wordList.size(); i++)
    {
        std::string word = wordList.at(i);
        if(inWordFilter(inWord, word) && correctLettersFilter(correctLetters, word) && notInWordFilter(notInWord, word))
        {
            returnVector.push_back(word);
        }
    }
    return returnVector;
}

bool inWordFilter(std::string inWord, std::string word) //returns whether or not the word contains the characters in the string inWord
{
    // std::cout << "In Word Filter\n";
    for(int i = 0; i < inWord.size(); i++)
    {
        if(word.find(inWord.at(i)) == std::string::npos)
        {
            return false;
        }
    }
    return true;
}
// "a_c_e"
bool correctLettersFilter(std::string correctLetters, std::string word)
{
    // std::cout << "Correct Letters Filter\nsize= " << correctLetters.size() << "\n";
    if(correctLetters.size() == 0)
    {
        return true;
    }
    if (std::count(correctLetters.begin(), correctLetters.end(), '_') == 5)
    {
        return true;
    }
    for(int i = 0; i < word.size(); i++)
    {
        if(correctLetters.at(i) == '_')
        {
            continue;
        }
        else if(word.at(i) != correctLetters.at(i))
        {
            return false;
        }
    }
    return true;
}

bool notInWordFilter(std::string notInWord, std::string word)
{
    // std::cout << "Not In Word Filter\n";
    for(int i = 0; i < notInWord.size(); i++)
    {
        if(word.find(notInWord.at(i)) != std::string::npos)
        {
            return false;
        }
    }
    return true;
}

std::vector<std::string> repetitionFilter(char c, std::vector<std::string> wordList)
{
    // std::cout << "Repetition Filterr\n";
    std::vector<std::string> returnVector;
    std::string word;
    for(int i = 0; i < wordList.size(); i++)
    {
        word = wordList.at(i);
        for(int j = 0; j < 4; j++)
        {
            if(word[j] == c && word[j] == word[j + 1])
            {
                returnVector.push_back(word);
            }
        }
    }
    return returnVector;
}


void printList(std::vector<std::string> wordList)  //prints a list to terminal
{
    // std::cout << "is printing " << wordList->size() << " words\n";
    for(int i = 0; i < wordList.size(); i++)
    {
        std::cout << wordList.at(i) << "\n";
    }
    std::cout << wordList.size() << "\n";
}
std::vector<std::string> checkFilter(std::vector<std::string> wordList, std::string guessWord, std::string checkWord)
{
    // std::cout << "Check Filter\n";
    std::vector<std::string> returnVector = wordList;
    std::string tempString = "_____";

    for(int i = 0; i < guessWord.size(); i++)
    {
        tempString = "_____";
        // std::cout << wordList.size() << "\n";
        if(guessWord.at(i) == checkWord.at(i))
        {
            // std::cout << "1\n";
            tempString[i] = guessWord.at(i);
            returnVector = filter(tempString, "", "", returnVector);
        }
        if(std::count(checkWord.begin(), checkWord.end(), guessWord.at(i)) > 1)
        {
            // std::cout << "2\n";
            returnVector = repetitionFilter(guessWord.at(i), returnVector);
        }
        if(checkWord.find(guessWord.at(i)) != std::string::npos)
        {
            // std::cout << "3\n";
            returnVector = filter("", guessWord.at(i) + "", "", returnVector);
        }
        if(checkWord.find(guessWord.at(i)) == std::string::npos)
        {
            // std::cout << "4\n";
            returnVector = filter("", "", guessWord.at(i) + "", returnVector);
        }

    }
    // std::cout << "returnVector size: " << returnVector.size() << "\n";
    // std::cout << "wordList size: " << wordList.size() << "\n";
    return returnVector;
}

double getWordWeighting(std::string word, std::vector<std::string> wordList, std::vector<std::string> focusedList)
{
    std::vector<std::string> originalList = wordList;
    int matches = 0;
    for(int i = 0; i < wordList.size(); i++)
    {   
        if(wordList.at(i) == word)
        {
            continue;
        }
        wordList = checkFilter(wordList, word, wordList.at(i));
        // std::cout << "wordList size: " << wordList.size() << "\n";
        // std::cout << "focuslist size: " << focusedList.size() << "\n";

        if(wordList == focusedList)
        {
            matches++;
        }
        wordList = originalList;
    }
    // std::cout << "matches: " << matches << " --------+_+_+_+_+_+_+_+_+_+_+\n";
    return matches / originalList.size();
}

double getWordValue(std::string word, std::vector<std::string> wordList)
{
    std::vector<std::string> originalList = wordList;
    std::vector<std::string> newList = wordList;
    std::vector<int> resultingLengths;

    std::string tempString = "_____";
    // [0-2,0-2,0-2,0-2,0-2]
    for(int a = 0; a < 3; a++)
    {
        for(int b = 0; b < 3; b++)
        {
            for(int c = 0; c < 3; c++)
            {
                for(int d = 0; d < 3; d++)
                {
                    for(int e = 0; e < 3; e++)
                    {
                        std::cout << "Testing state " << a * 81 + b * 27 + c * 9 + d * 3 + e * 1 << "\n";
                        tempString = "_____";
                        if(a == 0)
                        {
                            wordList = filter("", "", word[0] + "", wordList);
                        }
                        else if(a == 1)
                        {
                            wordList = filter("", word[0] + "", "", wordList);
                        }
                        else if(a == 2)
                        {
                            tempString[0] = word[0];
                            wordList = filter(tempString, "", "", wordList);
                        }
                        if(b == 0)
                        {
                            wordList = filter("", "", word[1] + "", wordList);
                        }
                        else if(b == 1)
                        {
                            wordList = filter("", word[1] + "", "", wordList);
                        }
                        else if(b == 2)
                        {
                            tempString[1] = word[1];
                            wordList = filter(tempString, "", "", wordList);
                        }
                        if(c == 0)
                        {
                            wordList = filter("", "", word[2] + "", wordList);
                        }
                        else if(c == 1)
                        {
                            wordList = filter("", word[2] + "", "", wordList);
                        }
                        else if(c == 2)
                        {
                            tempString[2] = word[2];
                            wordList = filter(tempString, "", "", wordList);
                        }
                        if(d == 0)
                        {
                            wordList = filter("", "", word[3] + "", wordList);
                        }
                        else if(d == 1)
                        {
                            wordList = filter("", word[3] + "", "", wordList);
                        }
                        else if(d == 2)
                        {
                            tempString[3] = word[3];
                            wordList = filter(tempString, "", "", wordList);
                        }
                        if(e == 0)
                        {
                            wordList = filter("", "", word[4] + "", wordList);
                        }
                        else if(e == 1)
                        {
                            wordList = filter("", word[4] + "", "", wordList);
                        }
                        else if(e == 2)
                        {
                            tempString[4] = word[4];
                            wordList = filter(tempString, "", "", wordList);
                        }
                        resultingLengths.push_back(wordList.size() * getWordWeighting(word, originalList, wordList));
                        std::cout << resultingLengths.size() << "\n";
                        wordList = originalList;
                    }
                }
            }
        }
    }
    return std::accumulate(resultingLengths.begin(), resultingLengths.end(), 0.0) / resultingLengths.size();
}