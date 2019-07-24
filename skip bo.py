#24/7/19 Skip Bo program - putting code into proper class format

"""Skip Bo Rules:
-numbered cards - twelve sets of 1 to 12 (144 cards) + 18 Skip Bo (wild) cards
-each player is dealt 10 cards (stock pile), and the goal is to get rid of
these stock cards. only one card from the pile is upturned at one time.
-to start each turn, the player picks up cards from the draw pile to equal 5
cards in their hand (eg. if they already had 3 cards, they would pick up 2).
- a turn ends by discarding a card from the player's hand to sit next to the
stock pile. There can be up to four discard piles.
- if a player discards all five cards in their hand without discarding one to
the discard pile, they pick up 5 more cards from the draw pile.
- there can be at most, 4 'building' piles in the center. once a building pile
reaches 12, it is removed and there can be another pile started.
"""

from random import randint, choice, shuffle
from time import sleep #for computer decisions
from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.stockPile = drawCards(10, [])
        self.hand = []
        self.discardPiles = [[], [], [], []]

    #put card from hand out to discard pile
    def discardFromHand(self, discardPilesIndex, cardToDiscard):
        self.discardPiles[discardPilesIndex].append(cardToDiscard)
        self.hand.remove(cardToDiscard)
        print("- Added", cardToDiscard, "card to discard pile -")
        print('Discard piles are now:', self.discardPiles)
        
    #deals 5 more cards to player if they have played all 5 in the same turn
    def checkHand(self):
        if len(self.hand) == 0:
            print("Hand is empty. Drawing 5 more cards...")
            sleep(0.5)
            self.hand = drawCards(5, [])

    #given a building pile to put it on, puts out a card from the stock pile
    def putOutCardFromStock(self, letter):
        print("- Added", self.stockPile[-1], "from Stock Pile to Building Pile", letter + ' -\n')
        buildingPiles[letter].append(self.stockPile[-1])
        self.stockPile.pop()
        sleep(1)
        checkBuildingPile(letter) #show what the building piles look like now

    #given a building pile, puts out a card from a given discard pile
    def putOutCardFromDiscardPile(self, letter, discardPileIndex):
        print("- Added", self.discardPiles[discardPileIndex][-1], "from Discard Pile to Building Pile", letter, '-')
        buildingPiles[letter].append(self.discardPiles[discardPileIndex][-1]) #add last card from given discard pile to dict
        self.discardPiles[discardPileIndex].pop() #remove card from discard pile
        checkBuildingPile(letter) #check whether pile has reached 12
        sleep(1)

    #given a building pile (letter), puts out a card from the hand
    def putOutCardFromHand(self, letter, card):
        print("- Added", card, "from Hand to Building Pile", letter, '-')
        buildingPiles[letter].append(card)
        self.hand.remove(card)
        self.checkHand() #deals 5 more cards to player if they just put out their last one
        sleep(0.5)
        checkBuildingPile(letter) #check whether pile has reached 12
        sleep(0.5)

    @abstractmethod
    def takeTurn(self):
        pass

    @abstractmethod
    def endTurn(self):
        pass    

class HumanPlayer(Player):
    def takeTurn(self):
        #add x cards to hand so that there are now 5 cards in player hand
        print('\n****' + self.name + "'s turn****")
        cardsToAdd = 5-len(self.hand)
        print(self.name, "adding", cardsToAdd, "cards to hand...")
        self.hand = drawCards(cardsToAdd, self.hand)
        sleep(0.5)
        endOfTurn = False
        
        while endOfTurn == False:
            #show what the player's hand and the play area looks like
            print("\nYour hand is", self.hand)
            print("Your stock pile contains", len(self.stockPile), "cards and the top card is", self.stockPile[-1:])
            print("Your discard piles are", self.discardPiles)
            displayBuildingPiles()
            sleep(1)
            
            decision = input("\nWhat do you want to do? ('s' for putting out a card from your \
stock pile, 'h' for putting out a card from your hand, 'd' to put out card from discard pile,\
 'e' to put card down to discard pile and end turn) ").strip().lower()
            
            if decision == 's': #put out card from stock pile
                self.playFromStockPile()
                #check if win condition met
                if len(self.stockPile) == 0:
                    return True #passes True back to main gameplay loop (to end game)
                
            elif decision == 'h': #put out card from hand to building pile
                self.playFromHand()
                
            elif decision == 'd': #put out card from discard pile to building pile
                self.playFromDiscardPile()
                
            elif decision == 'e': #put card from hand to discard pile, and end turn
                endOfTurn = self.endTurn() #returns True if a card was put down, False if function was exited early
            else:
                print("'" + decision + "'", "was not a valid option\n")
                
        #outside of main (endOfTurn) while loop       
        print("****End of", self.name + "'s turn****") 
        sleep(1)

    def playFromStockPile(self):
        displayBuildingPiles()
        while True:
            whichPile = input("Which pile do you want to add the " + self.stockPile[-1] + " card to? (eg. A) ").upper()
            if whichPile in buildingPiles:
                #checking that the top card from stock pile can be put out to the specified building pile
                if self.stockPile[-1] == 'W' or getTopCardFromBuildingPile(buildingPiles[whichPile]) + 1 == int(self.stockPile[-1]):
                    self.putOutCardFromStock(whichPile)
                    break
                else: #if card cannot go there, print error message and go back to start of loop (ask for new input)
                    print("Cannot put a", self.stockPile[-1], "card on top of a", \
                                  getTopCardFromBuildingPile(buildingPiles[whichPile]))
                    continue
            else: #if whichPile not in buildingPiles
                if whichPile == 'X': #the exit key
                    print("Going back to decision...\n")
                    sleep(0.5)
                    return
                else: 
                    print("Not a valid pile letter")

    def playFromHand(self):
        while True:
            print("\nYour hand is", self.hand)
            cardToPlay = input("Which card do you wish to place down? (press x to escape) ").upper()
            if cardToPlay == 'X':
                print("Going back to decision...\n")
                sleep(0.5)
                return #go back to decision loop, in same turn
            elif cardToPlay not in self.hand:
                print("You don't have that card in your hand")
                continue
            else: #if cardToDiscard was in self.hand
                while True:
                    #checking that the card can be put out to the specified building pile
                    whichPile = input("Which pile are you adding the " + cardToPlay + " card to? (eg. A) ").upper()
                    if whichPile in buildingPiles:
                        if cardToPlay == 'W' or getTopCardFromBuildingPile(buildingPiles[whichPile]) + 1 == int(cardToPlay):
                            self.putOutCardFromHand(whichPile, cardToPlay)
                            return
                        else: #if card cannot go there, print error message and go back to start of loop (ask for new input)
                            print("Cannot put a", cardToPlay, "card on top of a", \
                                  getTopCardFromBuildingPile(buildingPiles[whichPile]))
                            continue
                    else: #if whichPile not in buildingPiles
                        if whichPile == 'X': #the exit key
                            print("Going back to decision...\n")
                            sleep(0.5)
                            return
                        else: 
                            print("Not a valid pile letter")

    def playFromDiscardPile(self):
        print("The following are the top cards from your discard piles:")
        #takes last element of each list in discardPiles unless that list is empty
        availableCards = [i[-1] for i in self.discardPiles if len(i) > 0]
        print(availableCards)
        while True:
            cardToPlay = input("Which card do you want to play? (x to escape) ").upper()
            if cardToPlay == "X":
                print("Going back to decision...\n")
                sleep(0.5)
                return
            elif cardToPlay not in availableCards:
                print("That card is not available from your discard pile.")
                continue #loops again
            else: #if cardToPlay is in availableCards
                displayBuildingPiles()
                while True:
                    whichPile = input("Which pile do you want to add the card to? (eg. A) ").upper()
                    if whichPile in buildingPiles:
                        if cardToPlay == 'W' or getTopCardFromBuildingPile(buildingPiles[whichPile]) + 1 == int(cardToPlay):
                            for i in range(len(self.discardPiles)): #note: this only finds the first instance of that card
                                if len(self.discardPiles[i]) > 0 and self.discardPiles[i][-1] == cardToPlay:
                                    self.putOutCardFromDiscardPile(whichPile, i) #function takes buildingPiles key, and discardPile index number
                                    break
                            return
                        else:
                            print("Cannot put a", cardToPlay, "card on top of a", \
                                  getTopCardFromBuildingPile(buildingPiles[whichPile]))
                            continue #go back to start of loop
                    else: #if whichPile not in buildingPiles
                        if whichPile == 'X': #the exit key
                            print("Going back to decision...\n")
                            sleep(0.5)
                            return
                        else: 
                            print("Not a valid pile letter")

    def endTurn(self):
        while True:
            print("\nYour hand is", self.hand)
            cardToDiscard = input("Which card do you wish to place down? (press x to escape) ").upper()
            if cardToDiscard == 'X':
                print("Going back to decision...\n")
                sleep(0.5)
                return False
            elif cardToDiscard not in self.hand: #error message, and back to start of loop
                print("You don't have that card in your hand")
                continue
            else: #if cardToDiscard was in self.hand
                while True:
                    print("Your current discard piles are:", self.discardPiles)
                    try:
                        whichPile = int(input("Which discard pile (1-4) do you want to put the " + cardToDiscard + " card? "))
                        if whichPile > 4 or whichPile < 1:
                            print("Please enter a pile number from 1 to 4")
                        else: #if whichPile was a number from 1-4
                            self.discardFromHand(whichPile - 1, cardToDiscard) # -1 because index numbers are 0 based
                            return True
                    except:
                        print("Please enter an integer")

#computer players
        #should check if can put out card from stock pile, then only check again if the player
        #gets more cards
class ComputerPlayer(Player):
    def takeTurn(self):
        print("\n****" + self.name + "'s turn****")
        print(len(self.stockPile), "cards in the stock pile - top card is", self.stockPile[-1:])
        
        #add x cards to hand so that there are now 5 cards in player hand
        cardsToAdd = 5-len(self.hand)
        print(self.name, "adding", cardsToAdd, "cards to hand...")
        self.hand = drawCards(cardsToAdd, self.hand)
        endOfTurn = False
        
        while endOfTurn != True:
            sleep(1) #pause for 1 second between each action
            
            #first priority = put out card from stock pile
            if self.tryStockPile(): #returns True if a card was put out                
                #check win condition
                if len(self.stockPile) == 0:
                    print(self.name, "has no cards left in the stock pile!\n")
                    return True
                #displaying what has occurred to the player (as long as the game is still going)
                displayBuildingPiles()
                print(self.name, "now has", len(self.stockPile), "cards in the stock pile - top card is", self.stockPile[-1:])

            #second priority = can my available cards help me reach the stock pile card in one turn
            elif self.canStockCardBeReached():
                continue
            
            #next priority = can cards from the hand or the discard pile be put out
            elif self.tryHand(): #if a card is able to be put out from hand, returns True
                continue
            
            elif self.tryDiscardPile():
                continue
            
            else: #if no cards are able to be put out from stockPile, discardPile, or hand
                self.endTurn()
                endOfTurn = True
            
        print("****End of", self.name + "'s turn****")
        
    def tryStockPile(self): #put out top card from the stock pile if there is a corresponding building pile
        if self.stockPile[-1] == 'W':
            #put out W on a random building pile
            #https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-in-python-dictionary
            randomLetter = choice(list(buildingPiles.keys())) #pick random pile using random.choice
            self.putOutCardFromStock(randomLetter)         
            return True
        else: #if top card is a number
            for letter, cardList in buildingPiles.items():
                if int(self.stockPile[-1]) == getTopCardFromBuildingPile(cardList) + 1: #if stock card can go directly onto a building pile
                    self.putOutCardFromStock(letter)         
                    return True
            return False

    def tryHand(self):
        for card in self.hand: #checking each card in the hand, against each building pile
            for letter, cardList in buildingPiles.items():
                if card != 'W' and int(card) == getTopCardFromBuildingPile(cardList) + 1: #if the card can be put out (and isn't a W)
                    self.putOutCardFromHand(letter, card)
                    return True
        return False

    def tryDiscardPile(self):
        for index in range(len(self.discardPiles)):
            if len(self.discardPiles[index]) > 0: #for error handling, when trying to get the last card from the pile in next line
                availableCard = self.discardPiles[index][-1]
                for letter, cardList in buildingPiles.items():
                    #if the card can be put out (and isn't a W)
                    if availableCard != 'W' and int(availableCard) == getTopCardFromBuildingPile(cardList) + 1: 
                        self.putOutCardFromDiscardPile(letter, index)
                        return True
        return False

    def canStockCardBeReached(self, lowestDiff=13):
        availableCards = []
        path = []
        
        for letter, pile in buildingPiles.items():
            #difference is the number of cards between stock card and building pile
            difference = int(self.stockPile[-1]) - int(getTopCardFromBuildingPile(pile))

            #if difference is negative, indicates that to put out the stock card,
            #the pile needs to go past 12 (ie. be cleared)
            if difference <= 0:
                difference += 11

            #finding the lowest difference (pile with card closest to the stock card)
            if difference < lowestDiff:
                lowestDiff = difference
                lowestKey = letter

        #adding top cards of discard piles and all of hand to availableCards list
        for cardList in self.discardPiles:
            if len(cardList) > 0:
                availableCards.append(cardList[-1])
        availableCards += self.hand

        path = self.createPath(int(getTopCardFromBuildingPile(buildingPiles[lowestKey])), availableCards, path)

        #if the path is empty, it was not possible to create a full path with the available cards
        if len(path) == 0:
            return False

        #putting out each card as specified in path list
        for card in path:
            sleep(0.5)

            #if the card was from the hand, put it out from self.hand
            if card in self.hand:
                self.putOutCardFromHand(lowestKey, card)

            else:#if the card wasn't from the hand, look through the discardPiles and put out the card
                for index in range(len(self.discardPiles)):#iterating through each pile to find the card
                    #once the card is found (len > 0 for error handling)
                    if len(self.discardPiles[index]) > 0 and str(self.discardPiles[index][-1]) == card:
                            self.putOutCardFromDiscardPile(lowestKey, index)
                            break #ends the 'for index' loop, goes back to 'for card in path'
                         
        return True #at the very end, once all cards have been put out

    def createPath(self, buildingPileCard, availableCards, path):
        #if the path involves going past 12 and starting with a new pile, will run the function twice
        #one loop for buildingPileCard to 12, another from 0 to stockPile[-1]
        stockPileCard = int(self.stockPile[-1])
        if buildingPileCard > stockPileCard:
            stockPileCard = 13

        for i in range(buildingPileCard+1, stockPileCard): #buildingPileCard + 1 because we want to find cards starting from that number
            if str(i) in availableCards: #if the player has that card to use
                path.append(str(i))
                availableCards.remove(str(i))
            elif 'W' in availableCards: #if the player has a W to stand in for that card
                path.append('W')
                availableCards.remove('W')
            else: #if the player doesn't have that card
                return []

        if stockPileCard == 13: # starting with a new pile, a new loop will run starting from 1
            return self.createPath(0, availableCards, path)

        return path #if there is a possible path
    
    def endTurn(self):       
        #first, check if there are any discard piles that only contain one number, and if there is 
        #a matching card in the hand, put that one down
        for i in range(len(self.discardPiles)):
            if doesListContainOneCard(self.discardPiles[i]):
                for card in self.hand:
                    if card != 'W' and card == self.discardPiles[i][-1]:
                        self.discardFromHand(i, card)
                        return

        #second, if there is an empty discard pile:
        for i in range(len(self.discardPiles)):
            if len(self.discardPiles[i]) == 0:
                #if there is a duplicate card in your hand, put down one of those to the empty discard pile
                uniqueCards = []
                for card in self.hand:
                    if card not in uniqueCards or card == 'W':
                        #if card is unique or card is a 'W', add to list and keep looking for duplicates
                        uniqueCards.append(card)
                    else: #there must be a duplicate of that card in self.hand
                        self.discardFromHand(i, card)
                        return
                    
                #otherwise, put down the first card (preferrably not a W) in the empty discard pile               
                cardToDiscard = self.hand[0]
                for card in self.hand:
                    if card != 'W':
                        cardToDiscard = card
                        break
                self.discardFromHand(i, cardToDiscard)
                return
             
        #lastly, where all discard piles are full:       
        #find the first card from the hand (that isn't a W, unless no choice)
        cardToDiscard = self.hand[0]
        for card in self.hand:
            if card != 'W':
                cardToDiscard = card
                break
            
        #try to put the card on a pile that has only one other card in it
        for i in range(len(self.discardPiles)):
            if len(self.discardPiles[i]) == 1:
                self.discardFromHand(i, cardToDiscard)
                return

        #try to put the card on a designated "random cards" pile
        
        #otherwise, just put the card down to a random pile
        randomIndex = randint(0, 3) #random index for one of the four discard piles
        self.discardFromHand(randomIndex, cardToDiscard)
        return
            
#additional helpful functions, not in any class
def drawCards(numToDraw, playerHand=[]): #deals cards from the main pile into the player's hand
    for i in range(numToDraw):
        playerHand.append(pickUpPile[0]) #puts top pile card into the player's hand
        del pickUpPile[0] #removes top card from pile
    return playerHand

def getTopCardFromBuildingPile(cardList): #returns top card of building pile as an integer (rather than the letter 'W') 
    if cardList == []:
        return 0
    elif cardList[-1] == 'W':
        return int(getTopCardFromBuildingPile(cardList[:-1])) + 1
    else:
        return int(cardList[-1])

def displayBuildingPiles(): #shows the top card of each building pile, along with the pile name (A, B, C, or D)
    print("The building piles are as shown:")
    for letter, cardList in buildingPiles.items():
        print("Pile", letter, ":", getTopCardFromBuildingPile(cardList))

def checkBuildingPile(key): #resets building pile if it has reached 12
    if getTopCardFromBuildingPile(buildingPiles[key]) == 12:
        print("- Pile", key, "has reached 12. Clearing pile... -")
        for card in buildingPiles[key]:
            pickUpPile.append(card) #cards are put back into main pile
        shuffle(pickUpPile) #re-shuffles the list after the cards are added
        buildingPiles[key] = [] #the pile is emptied
        sleep(0.5)

def doesListContainOneCard(pile): #returns false if list is empty or if the list contains more than one unique card
    if len(pile) > 0:
        firstCard = pile[-1]
        for card in pile:
            if not firstCard == card:
                return False
        return True #if all cards in the list are the same
    else:
        return False

#--ToDo--

#fix decision computerPlayer - do you always want to put out as many cards as you can?

#if there are no spare discardPiles, it quickly descends into 'put random cards anywhere', where
    #instead it could put out cards onto a single pile that doesn't contain all of the same card
    #ie. ruin only one pile and not the rest

#also, don't need to check if the stock card can be put out each time if it's already established that you can't
#it should run at the start of the turn, and only again in the same turn if the player gets new cards
#if player gets new hand, or if a new stock card is turned over

#if card from discard piles is being added to path, add the next card from that discard pile to available cards list

#should i have different methods for putting out cards (from hand, from discard pile, etc) for both classes?
#that way i could put more code in the methods, and have different spacing for each one

#perhaps I should add decisions based on others' stock cards (ie. not helping them unless it interferes with
    #putting out their own stock cards or getting rid of their full hand)
#going further, could include discardPiles since those are visible to all players.

#apart from to get to the stock card, what conditions would you put a W out?

#need to change other functions that use discardPile in a roundabout (and bad runtime) way

#try hand, discard pile, and discard from hand (computer) all end with checking each discard pile against the chosen card
    #and if it can be put out, implementing the chosen function (eg. putOutCardFrom____)
    #is that worth pursuing?

#when picking a card to discard, you want to keep the cards immediately before your stock card if possible (eg. if stock card
    #is 10, you'll want to keep any 9's you have in your hand

    
#maybe you can implement a hint system for the player
#part of the 'can i put out the stock card' computerPlayer function could then be moved up into
#Player and used there.

#after testing is completed, get rid of unnecessary print statements in computer player class
#eg. printing the hand at end of turn when the user shouldn't be able to see that

#----main routine----

#initial setup: cards and play area
pickUpPile = [str(x % 12 + 1) for x in range(0, 144)] #creates twelve sets of numbers 1-12
pickUpPile += ["W"] * 18 #add 18 Skip Bo cards (represented by 'W')

#randomizing a list: https://stackoverflow.com/questions/976882/shuffling-a-list-of-objects
shuffle(pickUpPile)

buildingPiles = {'A':[], 'B':[], 'C':[], 'D':[]} #these are cards in the middle that anyone can build on

#initial setup: create computer players and human player
playerList = []
NUM_PLAYERS = 0
while NUM_PLAYERS < 1 or NUM_PLAYERS > 3:
    try:
        NUM_PLAYERS = int(input("How many computer players do you want to play? (between 1 and 3) "))
    except:
        print("Please enter an integer\n")

for i in range(NUM_PLAYERS): #creates computer players 
    playerList.append(ComputerPlayer("Computer " + str(i+1)))

#creating human player
userName = input("What would you like to be called? ")
playerList.append(HumanPlayer(userName))
sleep(0.5)

#play game
WinnerFound = False
while WinnerFound != True: #runs as long as the win condition (stockPile of a player is empty) remains False
    for i in range(len(playerList)): #cycles through each player in order
        WinnerFound = playerList[i].takeTurn()
        sleep(1)
        if WinnerFound == True:
            winner = playerList[i]
            break #otherwise, players after winner in list will be allowed to have turns after game has ended
    #loop begins again (if win condition not met) - ie. first player in list gets turn after last in list

#after game
print("********Game Over!********")
print("The winner is", winner.name, '!!!')

# since player1.stockPile.pop() removes last item, stock piles will be read
#from last to first - ie. last item in list will be 'on top' of stock pile
