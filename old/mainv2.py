import random, pygame, sys
from pygame.locals import *
import re
pygame.init()

white = (255,255,255)
yellow = (255,255,102)
grey = (211, 211, 211)
black = (0,0,0)
green=(0,255,0)
lightGreen=(153,255,204)

font = pygame.font.SysFont("Arial", 40)
bigFont = pygame.font.SysFont("Arial", 60)

youWin = bigFont.render("You Win!",       True, lightGreen)
youLose = bigFont.render("You Lose!",     True, lightGreen)
playAgain = bigFont.render("Play Again?", True, lightGreen)
file = open("words.txt","r")
wordList = [word[:-1] for word in file.readlines()]

class App:
    def __init__(self):
        self.main()
        
    def checkGuess(self, turns, word, userGuess, window):
        print(userGuess.lower(), userGuess.lower() in wordList)
        s = r"/" + str(userGuess.lower()) + r"/"
        print(s)
        if not re.findall(userGuess.lower(), " ".join(wordList)):
            return (False, False)
        in_word = ""
        correct_pos = "_____"
        renderList = ["","","","",""]
        spacing = 0
        guessColourCode = [grey,grey,grey,grey,grey]
        for x in range(0,5):
            if userGuess[x] in word and word.count(userGuess[x]) > in_word.count(userGuess[x]):
                in_word += userGuess[x]
                guessColourCode[x] = yellow

            if word[x] == userGuess[x]:
                correct_pos = correct_pos[:x] + userGuess[x] + correct_pos[x+1:]
                guessColourCode[x] = green
        print(in_word, correct_pos)

        for x in range(0,5):
            renderList[x] = font.render(userGuess[x], True, black)
            pygame.draw.rect(window, guessColourCode[x], pygame.Rect(60 +spacing, 50+ (turns*80), 50, 50))
            window.blit(renderList[x], (70 + spacing, 50 + (turns*80)))
            spacing+=80

        if guessColourCode == [green,green,green,green,green]:
            return True, True
        return False, True


    def main(self):
        word = wordList[random.randint(0, len(wordList)-1)].upper()

        height = 800
        width = 500

        FPS = 30
        clock = pygame.time.Clock()

        window = pygame.display.set_mode((width, height))
        window.fill(black)

        guess = ""

        print(word)


        for x in range(0,5):
            for y in range(0,6):
                pygame.draw.rect(window, grey, pygame.Rect(60+(x*80), 50+(y*80), 50, 50), 2)
                
        pygame.draw.rect(window, grey, pygame.Rect(60, 475, 100, 550))    
        
        pygame.display.set_caption("Wordle!")

        turns = 0
        win = False

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.exit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if len(guess) < 5 and event.unicode.isalpha():
                        guess+=event.unicode.upper()

                    if event.key == K_RETURN and win == True:
                        self.main()

                    if event.key == K_RETURN and turns == 6:
                        self.main()

                    if event.key == K_BACKSPACE:
                        guess = guess[:-1]

                    if event.key == K_RETURN and len(guess) > 4:
                        win, clear_guess = self.checkGuess(turns, word, guess, window)
                        print(clear_guess)
                        if clear_guess:
                            turns+=1
                            guess = ""
                            window.fill(black,(0,500, 500, 200))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse[0] > 60 and mouse[0] < 160 and mouse[1] > 475 and mouse[1] < 725:
                        print("enter")

            # window.fill(black,(0,500, 500, 600))
            renderGuess = font.render(guess, True, grey)
            window.blit(renderGuess, (180, 530))
            if win == True:
                window.blit(font.render("You Win!", True, grey), (10, 530))
            if turns == 6 and win != True:
                window.blit(font.render("You Lose! The word was " + word, True, grey), (10, 530))

            pygame.display.update()
            clock.tick(FPS)

    def make_guess(self, guess_num, correct_letters, in_word):
        if guess_num == 0:
            return "ADIEU"
        elif guess_num == 1:
            return "CORKS"
    
                    
app = App()