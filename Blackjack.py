from random import shuffle


def createDeck():
    Deck = []
    faceValues = ["A", "J", "Q", "K"]  # ace, jack, queen, king
    for i in range(4):  # for the 4 different suits
        for card in range(2, 11):  # adding number 2 to 10
            # adding numbers to deck, converted to strings for consistency
            Deck.append(str(card))
        for card in faceValues:
            Deck.append(card)  # ace, jack, queen, king to deck
    shuffle(Deck)
    return Deck


class Player:
    # empty list and chosen quantity of money to start with
    def __init__(self, Hand=[], Money=100):
        self.Hand = Hand
        self.Score = self.setScore()
        self.Money = Money
        self.Bet = 0  # amount of money to bet (starts at 0 as default)

    def __str__(self):  # print(Player)
        currentHand = ""  # currently would look like ["A", "10"]
        for card in self.Hand:
            # changes output to more aesthetically pleasing "A 10"
            currentHand += str(card) + " "
        finalStatus = currentHand + "score: " + \
            str(self.Score)  # "A 10 2 4 score: 17"
        return finalStatus

    def setScore(self):  # will recalculate score of current hand
        self.Score = 0
        # faceValues and corresponding scores
        faceCardsDict = {"A": 11, "J": 10, "Q": 10, "K": 10, "2": 2,
                         "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10}
        aceCounter = 0  # will check for how many Aces in hand
        for card in self.Hand:
            self.Score += faceCardsDict[card]  # adds value to score
            if card == "A":  # if there's an Ace in the hand
                aceCounter += 1  # add 1 to the Ace counter
            # checks to see if the score is over 21 and if there's an Ace in the hand
            if self.Score > 21 and aceCounter != 0:
                self.Score -= 10  # if the score is over 21 and there's an ace, remove 10 from the score to make Ace=1 not 11
                aceCounter -= 1  # remove the ace from the ace counter
        return self.Score  # print score

    def hit(self, card):
        self.Hand.append(card)
        self.Score = self.setScore()

    def play(self, newHand):  # function to reset score
        self.Hand = newHand  # hand will be the new hand
        self.Score = self.setScore()  # score is now reset

    def betMoney(self, amount):
        self.Money -= amount
        self.Bet += amount

    def win(self, result):  # win money from the pot to the player
        if result == True:  # if win is True
            # checks to see if blackjack (score of 21 with only 2 cards)
            if self.Score == 21 and len(self.Hand) == 2:
                self.Money += 2.5 * self.Bet  # receive 2.5 times the bet back
                print("Blackjack!")
            else:
                self.Money += 2 * self.Bet  # receive double the bet back
                print("You win!")
                self.Bet = 0  # resets Bet to 0 until next play
        else:
            self.Bet = 0  # in case of loss, no money back and Bet is reset
            print("You lose!")

    def drawGame(self):  # in case of a draw in the game
        print("It's a draw!")
        self.Money += self.Bet  # transfers bet money back
        self.Bet = 0  # resets bet to 0

    def hasBlackjack(self):
        if self.Score == 21 and len(self.Hand) == 2:
            return True
        else:
            return False


def printHouse(House):
    # will access the cards in House's hand, index by index
    for card in range(len(House.Hand)):
        if card == 0:  # the first card
            # prints X instead of first card to hide value and changes end separator to continue printing on the same line instead of new line
            print("X", end=" ")
        elif card == len(House.Hand) - 1:  # the last card in the House's hand
            print(House.Hand[card])  # prints the last card in the House's hand
        else:
            # to print the other cards in the Hand with the same line formatting
            print(House.Hand[card], end=" ")


""" Player1 = Player(["3", "7", "5"])  # manually chosen cards
print(Player1)
Player1.hit("A")  # manually adds Ace to hand, recalculates score
print(Player1)
Player1.betMoney(20)
print(Player1.Money, Player1.Bet)
Player1.win(True)
print(Player1.Money, Player1.Bet)
 """

cardDeck = createDeck()
# first hand is the first two cards removed with pop function
# pop function takes the last number out and reduces the list, similar to drawing a card
firstHand = [cardDeck.pop(), cardDeck.pop()]
secondHand = [cardDeck.pop(), cardDeck.pop()]
# creates 2 hands of cards using pop function
Player1 = Player(firstHand)
House = Player(secondHand)
cardDeck = createDeck()
while(True):
    if len(cardDeck) < 20:
        cardDeck = createDeck()
    firstHand = [cardDeck.pop(), cardDeck.pop()]
    secondHand = [cardDeck.pop(), cardDeck.pop()]
    Player1.play(firstHand)
    House.play(secondHand)
    print(cardDeck)
    printHouse(House)
    print("Player: ", Player1)
    # asks player for their bet amount
    Bet = int(input("Please enter your bet: "))
    Player1.betMoney(Bet)  # adds bet

    if Player1.hasBlackjack():  # checks to see if Player 1 has a blackjack and if so, returns true, else returns false
        if House.hasBlackjack():  # checks to see if House has a blackjack
            Player1.drawGame()  # if both have blackjack, calls a draw
        else:
            Player1.win(True)  # player wins the game
    else:
        # prompts player if they want another card but only if score is under 21
        while(Player1.Score < 21):
            action = input("Do you want another card? (Y/N): ").upper()
            if action == "Y":
                Player1.hit(cardDeck.pop())
                print("Player: ", Player1)
                printHouse(House)
            else:
                break
                # if the House's hand scores less than 16 then the House draws another card
        while (House.Score < 16):
            print(House)
            House.hit(cardDeck.pop())
        if Player1.Score > 21:
            if House.Score > 21:  # if both players have busted = draw
                Player1.drawGame()
            else:
                # if player busts but House doesn't, player loses
                Player1.win(False)
        elif Player1.Score > House.Score:  # if player scores more than house
            Player1.win(True)

        elif Player1.Score == House.Score:  # if player and house score the same
            Player1.drawGame()

        else:
            if House.Score > 21:  # if house busts but player doesn't
                Player1.win(True)
            else:
                Player1.win(False)
    print(Player1.Money)
    print("House: ", House)  # prints the full House's hand and score
