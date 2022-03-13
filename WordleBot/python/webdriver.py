import main as gameEngine
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

def keyboardIn(string):
    keyBoardLocation = "document.querySelector('game-app').shadowRoot.children[1].children[1].children[1].shadowRoot.children[1]"
    for letter in string:
        if letter in "qwertyuiop":
            driver.execute_script(keyBoardLocation + ".children[0]" + ".children[" + str("qwertyuiop".index(letter)) + "].click()")
        elif letter in "asdfghjkl":
            driver.execute_script(keyBoardLocation + ".children[1]" + ".children[" + str("asdfghjkl".index(letter) + 1) + "].click()")
        else:
            driver.execute_script(keyBoardLocation + ".children[2]" + ".children[" + str("zxcvbnm".index(letter) + 1) + "].click()")
    driver.execute_script(keyBoardLocation + ".children[2]" + ".children[0].click()")

def getWordState(rowIndex):
    wordState = ""
    for int in range(5):
        letterState = driver.execute_script('return document.querySelector("game-app").shadowRoot.children[1].children[1].children[0].children[0].children[' + str(rowIndex) + '].shadowRoot.children[1].children[' + str(int) + '].getAttribute("evaluation")')
        if letterState == 'absent':
            wordState += "0"
        elif letterState == 'present':
            wordState += "1"
        else:
            wordState += "2"
    return wordState

driver.get("https://www.nytimes.com/games/wordle/index.html")
driver.execute_script("document.querySelector('body > game-app').shadowRoot.querySelector('#game > game-modal').shadowRoot.querySelector('div > div > div').click()")

wordList = gameEngine.available_words
keyboardIn("salet")
wordList = gameEngine.gameFilter("salet", getWordState(0), wordList)
for i in range(5):
    time.sleep(2)
    if gameEngine.isBlimp(wordList):
        inputWord = gameEngine.blimpSearch(wordList)
    else:
        inputWord = gameEngine.getMaxValue1(wordList)
    keyboardIn(inputWord)
    wordList = gameEngine.gameFilter(inputWord, getWordState(i + 1), wordList)
time.sleep(10)