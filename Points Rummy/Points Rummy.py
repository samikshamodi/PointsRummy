# Name: SAMIKSHA MODI
# ROll No:2019331
# Section:B


import random
import pygame
import time
import os
pygame.init()


"""
How to Play
-Tap on a card to select it
-To throw a card select a card and then tap on the designated area
-To swap 2 cards, select 2 cards
-Press Right Arrow key to change the music
"""

blue = (0, 76, 153)
yellow = (255, 255, 51)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
pink = (216, 48, 228)
# size of game window
l = 1200
b = 700

screen = pygame.display.set_mode((l, b))
pygame.display.set_caption('Points Rummy')
running = True


cards = []
suit = ['c', 'd', 'h', 's']
rank = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']
rankvalue = {}
# creates a dictionary of the rank value of all the cards
for i in suit:
    l = 1
    for j in rank:
        rankvalue[i+j] = l
        l += 1
rankvalue['pj'] = 0

pointvalue=dict(rankvalue)
for i in pointvalue:
    if i[1]=='j' or i[1]=='q' or i[1]=='k' or i[1]=='a':
        pointvalue[i]=10

pointvalue['pj']=0

computer = []  # stores the computer cards that are assigned to it
user = []  # stores the user cards that are assigned to it
opendeck = []  # stores the cards in the open deck
cards = []  # acts as the closed deck
wj = ''  # stores wild joker
sc = ''  # stores starting card or first card of opendeck at the beginning of the game

songlist = os.listdir("music")  # stores songs present in the folder music
songno = 0  # stores song no being played


class User:
    def __init__(self, user, wj, sc):
        self.cards = user
        self.wj = wj
        self.sc = sc
        self.pure = []  # stores pure sequence as declared by user
        self.impure = []  # stores impure/pure sequence by user
        self.group1 = []  # stores a sequence or set by user
        self.group2 = []  # stores a sequence or set by user
        self.swapcard = []  # stores card to be swapped
        self.rectobject = []  # stores rectangle object of hihglighted area
        self.index = []  # stores index of selected cards to swap
        self.flag = 0
        self.points=0

    def print_cards(self):
        """Prints only the user cards on screen"""
        x = 0
        for i in self.cards:
            image = pygame.image.load("images/cards/"+i+".png")
            screen.blit(image, (x, (b-105)))
            pygame.display.update()
            x = x+74

    def highlight_card(self, x):
        """Highlights the card yellow when the game is being played between the computer and the user during user's turn.
        It is then used to swap the cards, or throw a card in the opendeck or throw a card in the finish slot to declare"""
        self.flag += 1
        r = pygame.Rect((x*74, b-110), (74, 5))
        screen.fill(yellow, r)
        self.swapcard.append(self.cards[x])
        self.rectobject.append(r)
        self.index.append(x)
        print(self.cards[x])
        pygame.display.update()
        if self.flag == 2:
            time.sleep(1)
            self.swap()

    def swap(self):
        """ It is called by the highlight_card function to swap 2 user cards"""
        self.flag = 0
        print("User swapped " +
              str(self.cards[self.index[0]])+" with "+str(self.cards[self.index[1]]))
        self.cards[self.index[0]], self.cards[self.index[1]
                                              ] = self.cards[self.index[1]], self.cards[self.index[0]]
        self.print_cards()
        screen.fill(blue, self.rectobject[0])
        screen.fill(blue, self.rectobject[1])
        self.swapcard = []
        self.rectobject = []
        self.index = []
        pygame.display.update()

    def sort(self):
        """It sorts the user cards in the order [2,3,4...j,q,k,a]. It first makes 4 new lists for the 4 different suits,
        sort them in the required order and then merge them"""

        print("User cards before sorting: ", self.cards)
        flag = 0
        for i in self.cards:
            if i == 'pj':
                flag = 1

        def sort_again(temp):
            temp2 = []
            arr = ['2', '3', '4', '5', '6', '7',
                   '8', '9', '1', 'j', 'q', 'k', 'a']
            for i in arr:
                for j in temp:
                    for k in temp:
                        if(i == k[1]):
                            temp2.append(k)
                            temp.remove(k)
                            break
            return temp2

        t = []

        def remove_nest(temp):
            for i in temp:
                if type(i) == list:
                    remove_nest(i)
                else:
                    t.append(i)

        c = [x for x in self.cards if x[0] == 'c']
        d = [x for x in self.cards if x[0] == 'd']
        s = [x for x in self.cards if x[0] == 's']
        h = [x for x in self.cards if x[0] == 'h']

        self.cards = []
        if flag == 1:
            self.cards = ['pj']

        self.cards.append(sort_again(c))
        self.cards.append(sort_again(d))
        self.cards.append(sort_again(s))
        self.cards.append(sort_again(h))

        remove_nest(self.cards)
        self.cards = t
        print("User cards after sorting: ", self.cards)
        print()
        self.print_cards()

    def pick_card_open_deck(self):
        """The user can pick a card from the opendeck.Then that card is removed from, the opendeck and an empty
        blue area is shown instead which tells the user that no card has been thrown by them"""

        global opendeck
        print("Picked card by user: ", opendeck[-1])
        self.cards.append(opendeck[-1])
        opendeck.pop()
        r = pygame.Rect((746, 301), (73, 105))
        screen.fill(blue, r)
        pygame.display.update()
        self.print_cards()

    def pick_card_closed_deck(self):
        """ User can pick the card from the closed deck. The system generates a random card from the closed deck (list:cards),
        then removes it from the closed deck. If the closed deck is empty, it reshuffles the open deck and the game continues."""
        global opendeck
        global cards

        if len(cards) == 0:
            random.shuffle(opendeck)
            cards = opendeck
            opendeck = []
            r = pygame.Rect((746, 301), (73, 105))
            screen.fill(blue, r)
            pygame.display.update()

        temp = random.choice(cards)
        print("Picked card by user: ", temp)
        self.cards.append(temp)
        cards.remove(temp)
        self.print_cards()

    def throw_card(self):
        """The user first selects the card using the highlight_card function, and then taps on either the open deck or the finish slot
        to finish their turn. The user cards are updated and printed again"""
        global userturn
        global opendeck

        print("Thrown card by user: ", self.swapcard[0])
        opendeck.append(self.swapcard[0])
        self.cards.remove(self.swapcard[0])
        # blue at the place where 14th card was
        screen.fill(blue, self.rectobject[0])
        pygame.display.update()
        self.swapcard.pop()
        self.rectobject.pop()
        self.index.pop()
        self.flag = 0
        userturn = 0        #tells that now it is computer's turn
        print_rest()
        r = pygame.Rect((13*74, b-105), (75, 106))
        screen.fill(blue, r)
        pygame.display.update()
        self.print_cards()
        print()
        print("User cards after throw: ", self.cards)
        print("Open Deck: ", opendeck)
        print("Closed Deck: ", cards)
        print()

        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render('Turn:COMPUTER', True, white, blue)
        textRect = text.get_rect()
        textRect.center = (1000, 300)
        screen.blit(text, textRect)
        pygame.display.update()

        c.move()

    def declare(self):
        """ Creates a declare screen by printing the user cards and instructions"""
        global declared
        declared = 1

        screen.fill(blue)
        pygame.display.update()
        self.print_cards()
        pygame.display.update()

        text = font.render(
            'Select a Pure Sequence and then tap OK', True, white, blue)
        textRect = text.get_rect()
        textRect.center = (500, 150)
        screen.blit(text, textRect)
        pygame.display.update()

        image = pygame.image.load("images/ok.png")
        screen.blit(image, (1000, 550))
        pygame.display.update()

    def accept_groups(self, x):
        """ When ok==0 it accepts a pure sequence from the user. When ok==1 it accepts another pure/impure sequence from the user. When ok==2 it accepts a set/sequence from the user. When ok==3 it assigns the remaning cards to another set/sequence """
        global ok

        if ok == 0:
            r = pygame.Rect((x*74, b-110), (74, 5))
            screen.fill(yellow, r)
            pygame.display.update()

            self.pure.append(self.cards[x])

            if self.pure.count(self.cards[x]) == 2:
                self.pure.remove(self.cards[x])
                self.pure.remove(self.cards[x])
                screen.fill(blue, r)
                pygame.display.update()

        if ok == 1:
            r = pygame.Rect((x*74, b-110), (74, 5))
            screen.fill(yellow, r)
            pygame.display.update()

            self.impure.append(self.cards[x])

            if self.impure.count(self.cards[x]) == 2:
                self.impure.remove(self.cards[x])
                self.impure.remove(self.cards[x])
                screen.fill(blue, r)
                pygame.display.update()

        if ok == 2:
            r = pygame.Rect((x*74, b-110), (74, 5))
            screen.fill(yellow, r)
            pygame.display.update()

            self.group1.append(self.cards[x])

            if self.group1.count(self.cards[x]) == 2:
                self.group1.remove(self.cards[x])
                self.group1.remove(self.cards[x])
                screen.fill(blue, r)
                pygame.display.update()

        if ok == 3:
            self.group2 = list(self.cards)
            self.check_groups()

    def sort_declare(self, l):
        """ sorts cards in the order a,2,3,4...k,q,k"""
        global rankvalue
        flag = 0
        for i in l:

            if i == 'pj':
                flag = 1
                l.remove('pj')

        l = sorted(l, key=lambda x: (x[0], rankvalue[x]))

        if flag == 1:
            l.append('pj')

        return l

    def check_pure(self):
        """ Checks if the sequence is pure."""
        global rankvalue
        self.pure = self.sort_declare(self.pure)
        if len(self.pure) == 4:
            if self.pure[0][0] == self.pure[1][0] == self.pure[2][0] == self.pure[3][0] and self.pure[0][1] == 'a' and self.pure[1][1] == 'j' and self.pure[2][1] == 'q' and self.pure[3][1] == 'k':
                print("Valid Pure Sequence")
            elif self.pure[0][0] == self.pure[1][0] == self.pure[2][0] == self.pure[3][0] and self.pure[0][1] == 'a' and self.pure[1][1] == '2' and self.pure[2][1] == 'q' and self.pure[3][1] == 'k':
                print("Valid Pure Sequence")
            elif self.pure[0][0] == self.pure[1][0] == self.pure[2][0] == self.pure[3][0] and self.pure[0][1] == 'a' and self.pure[1][1] == '2' and self.pure[2][1] == '3' and self.pure[3][1] == 'k':
                print("Valid Pure Sequence")
            elif self.pure[0][0] == self.pure[1][0] == self.pure[2][0] == self.pure[3][0] and rankvalue[self.pure[0]]+3 == rankvalue[self.pure[1]]+2 == rankvalue[self.pure[2]]+1 == rankvalue[self.pure[3]]:
                print("Valid Pure Sequence")
            else:
                print("Invalid Pure Sequence")
                for i in self.pure:
                    self.points+=pointvalue[i]
                #invalid()
        elif len(self.pure) == 3:
            if self.pure[0][0] == self.pure[1][0] == self.pure[2][0] and self.pure[0][1] == 'a' and self.pure[1][1] == 'q' and self.pure[2][1] == 'k':
                print("Valid Pure Sequence")
            elif self.pure[0][0] == self.pure[1][0] == self.pure[2][0] and self.pure[0][1] == 'a' and self.pure[1][1] == '2' and self.pure[2][1] == 'k':
                print("Valid Pure Sequence")
            elif self.pure[0][0] == self.pure[1][0] == self.pure[2][0] and rankvalue[self.pure[0]]+2 == rankvalue[self.pure[1]]+1 == rankvalue[self.pure[2]]:
                print("Valid Pure sequence")
            else:
                print("Invalid Pure Sequence")
                for i in self.pure:
                    self.points+=pointvalue[i]
                #invalid()
        print(self.points)

    def check_impure(self):
        """ Checks if the sequence is pure/impure"""
        global rankvalue

        possiblejokers = ['pj', ('s'+wj[1]), ('c'+wj[1]),
                          ('h'+wj[1]), ('d'+wj[1])]
        self.impure = self.sort_declare(self.impure)
        for i in self.impure:
            if i in possiblejokers:
                self.impure.remove(i)

        if len(self.impure) == 4:  # joker=0
            if self.impure[0][0] == self.impure[1][0] == self.impure[2][0] == self.impure[3][0] and self.impure[0][1] == 'a' and self.impure[1][1] == 'j' and self.impure[2][1] == 'q' and self.impure[3][1] == 'k':
                print("Valid Impure Sequence")
            elif self.impure[0][0] == self.impure[1][0] == self.impure[2][0] == self.impure[3][0] and self.impure[0][1] == 'a' and self.impure[1][1] == '2' and self.impure[2][1] == 'q' and self.impure[3][1] == 'k':
                print("Valid Impure Sequence")
            elif self.impure[0][0] == self.impure[1][0] == self.impure[2][0] == self.impure[3][0] and self.impure[0][1] == 'a' and self.impure[1][1] == '2' and self.impure[2][1] == '3' and self.impure[3][1] == 'k':
                print("Valid Impure Sequence")
            elif self.impure[0][0] == self.impure[1][0] == self.impure[2][0] == self.impure[3][0] and rankvalue[self.impure[0]]+3 == rankvalue[self.impure[1]]+2 == rankvalue[self.impure[2]]+1 == rankvalue[self.impure[3]]:
                print("Valid Impure Sequence")
            else:
                print("Invalid Impure Sequence")
                for i in self.impure:
                    self.points+=pointvalue[i]
                #invalid()
        elif len(self.impure) == 3:  # joker=0 or 1
            if self.impure[0][0] == self.impure[1][0] == self.impure[2][0] and self.impure[0][1] == 'a' and self.impure[1][1] == 'q' and self.impure[2][1] == 'k':
                print("Valid Impure Sequence")
            elif self.impure[0][0] == self.impure[1][0] == self.impure[2][0] and self.impure[0][1] == 'a' and self.impure[1][1] == '2' and self.impure[2][1] == 'k':
                print("Valid Impure Sequence")
            elif self.impure[0][0] == self.impure[1][0] == self.impure[2][0] and rankvalue[self.impure[0]]+2 == rankvalue[self.impure[1]]+1 == rankvalue[self.impure[2]]:
                print("Valid Impure Sequence")
            else:
                print("Invalid Impure Sequence")
                for i in self.impure:
                    self.points+=pointvalue[i]
                #invalid()
        elif len(self.impure) == 2:  # joker=1 or 2
            if self.impure[0][0] == self.impure[1][0] and self.impure[0][1] == 'a' and self.impure[1][1] == 'k':
                print("Valid Impure Sequence")
            elif self.impure[0][0] == self.impure[1][0] and rankvalue[self.impure[0]]+1 == rankvalue[self.impure[1]]:
                print("Valid Impure Sequence")
            elif self.impure[0][0] == self.impure[1][0] and rankvalue[self.impure[0]]+2 == rankvalue[self.impure[1]]: #Middle card was wild joker eg c6 c7(wj) c8
                print("Valid Impure Sequence")
            else:
                print("Invalid Impure Sequence")
                for i in self.impure:
                    self.points+=pointvalue[i]
                #invalid()
        elif len(self.impure) == 1:  # joker=2 or 3
            print("Valid Impure Sequence")
        elif len(self.impure) == 0:  # joker=3 or 4
            print("Valid Impure Sequence")

        print(self.points)

    def check_group1(self):
        """ Checks for a set or sequence"""
        global rankvalue
        possiblejokers = ['pj', ('s'+wj[1]), ('c'+wj[1]),
                          ('h'+wj[1]), ('d'+wj[1])]

        set = 0
        for i in self.group1:
            if i in possiblejokers:
                self.group1.remove(i)

        # checking whether possible set or sequence
        if len(self.group1) > 1 and self.group1[0][1] == self.group1[1][1]:
            set = 1

        # if set=1 check for set else if set=0 check for sequence
        if set == 1:  # checking for set
            self.group1 = sorted(
                self.group1, key=lambda x: (rankvalue[x]))

            if len(self.group1) == 4:
                if self.group1[0][1] == self.group1[1][1] == self.group1[2][1] == self.group1[3][1]:
                    print("Valid Set Group1")
                else:
                    print("Invalid Set Group1")
                    for i in self.group1:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group1) == 3:
                if self.group1[0][1] == self.group1[1][1] == self.group1[2][1]:
                    print("Valid Set Group1")
                else:
                    print("Invalid Set Group1")
                    for i in self.group1:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group1) == 2:
                if self.group1[0][1] == self.group1[1][1]:
                    print("Valid Set Group1")
                else:
                    print("Invalid Set Group1")
                    for i in self.group1:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group1) == 1:
                print("Valid Set Group1")
            elif len(self.group1) == 0:
                print("Valid Set Group1")

        if set == 0:  # checking for sequence
            self.group1 = self.sort_declare(self.group1)
            if len(self.group1) == 4:  # joker=0
                if self.group1[0][0] == self.group1[1][0] == self.group1[2][0] == self.group1[3][0] and self.group1[0][1] == 'a' and self.group1[1][1] == 'j' and self.group1[2][1] == 'q' and self.group1[3][1] == 'k':
                    print("Valid Sequence Group1")
                elif self.group1[0][0] == self.group1[1][0] == self.group1[2][0] == self.group1[3][0] and self.group1[0][1] == 'a' and self.group1[1][1] == '2' and self.group1[2][1] == 'q' and self.group1[3][1] == 'k':
                    print("Valid Sequence Group1")
                elif self.group1[0][0] == self.group1[1][0] == self.group1[2][0] == self.group1[3][0] and self.group1[0][1] == 'a' and self.group1[1][1] == '2' and self.group1[2][1] == '3' and self.group1[3][1] == 'k':
                    print("Valid Sequence Group1")
                elif self.group1[0][0] == self.group1[1][0] == self.group1[2][0] == self.group1[3][0] and rankvalue[self.group1[0]]+3 == rankvalue[self.group1[1]]+2 == rankvalue[self.group1[2]]+1 == rankvalue[self.group1[3]]:
                    print("Valid Sequence Group1")
                else:
                    print("Invalid Sequence Group1")
                    for i in self.group1:
                        self.points+=pointvalue[i]
                    #invalid()
            if len(self.group1) == 3:  # joker=0 or 1
                if self.group1[0][0] == self.group1[1][0] == self.group1[2][0] and self.group1[0][1] == 'a' and self.group1[1][1] == 'q' and self.group1[2][1] == 'k':
                    print("Valid Sequence Group1")
                elif self.group1[0][0] == self.group1[1][0] == self.group1[2][0] and self.group1[0][1] == 'a' and self.group1[1][1] == '2' and self.group1[2][1] == 'k':
                    print("Valid Sequence Group1")
                elif self.group1[0][0] == self.group1[1][0] == self.group1[2][0] and rankvalue[self.group1[0]]+2 == rankvalue[self.group1[1]]+1 == rankvalue[self.group1[2]]:
                    print("Valid Sequence Group1")
                else:
                    print("Invalid Sequence Group1")
                    for i in self.group1:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group1) == 2:  # joker=1 or 2
                if self.group1[0][0] == self.group1[1][0] and self.group1[0][1] == 'a' and self.group1[1][1] == 'k':
                    print("Valid Sequence Group1")
                elif self.group1[0][0] == self.group1[1][0] and rankvalue[self.group1[0]]+1 == rankvalue[self.group1[1]]:
                    print("Valid Sequence Group1")
                else:
                    print("Invalid Sequence Group1")
                    for i in self.group1:
                        self.points+=pointvalue[i]
                   # invalid()
            elif len(self.group1) == 1:  # joker=2 or 3
                print("Valid Sequence Group1")
            elif len(self.group1) == 0:  # joker=3 or 4
                print("Valid Sequence Group1")

        print(self.points)

    def check_group2(self):
        """Checks for a set or sequence"""
        global rankvalue
        possiblejokers = ['pj', ('s'+wj[1]), ('c'+wj[1]),
                          ('h'+wj[1]), ('d'+wj[1])]
        # checking group1. can be a set or a sequence

        set = 0
        for i in self.group2:
            if i in possiblejokers:
                self.group2.remove(i)

        # check for set else check for sequence
        if len(self.group2) > 1 and self.group2[0][1] == self.group2[1][1]:
            set = 1

        # if set=1 check for set else if set=0 check for sequence
        if set == 1:  # checking for set
            self.group2 = sorted(
                self.group2, key=lambda x: (rankvalue[x]))

            if len(self.group2) == 4:
                if self.group2[0][1] == self.group2[1][1] == self.group2[2][1] == self.group2[3][1]:
                    print("Valid Set Group2")
                else:
                    print("Invalid Set Group2")
                    for i in self.group2:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group2) == 3:
                if self.group2[0][1] == self.group2[1][1] == self.group2[2][1]:
                    print("Valid Set Group2")
                else:
                    print("Invalid Set Group2")
                    for i in self.group2:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group2) == 2:
                if self.group2[0][1] == self.group2[1][1]:
                    print("Valid Set Group2")
                else:
                    print("Invalid Set Group2")
                    for i in self.group2:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group2) == 1:
                print("Valid Set Group2")
            elif len(self.group2) == 0:
                print("Valid Set Group2")

        if set == 0:  # checking for sequence
            self.group2 = self.sort_declare(self.group2)
            if len(self.group2) == 4:  # joker=0
                if self.group2[0][0] == self.group2[1][0] == self.group2[2][0] == self.group2[3][0] and self.group2[0][1] == 'a' and self.group2[1][1] == 'j' and self.group2[2][1] == 'q' and self.group2[3][1] == 'k':
                    print("Valid Sequence Group2")
                elif self.group2[0][0] == self.group2[1][0] == self.group2[2][0] == self.group2[3][0] and self.group2[0][1] == 'a' and self.group2[1][1] == '2' and self.group2[2][1] == 'q' and self.group2[3][1] == 'k':
                    print("Valid Sequence Group2")
                elif self.group2[0][0] == self.group2[1][0] == self.group2[2][0] == self.group2[3][0] and self.group2[0][1] == 'a' and self.group2[1][1] == '2' and self.group2[2][1] == '3' and self.group2[3][1] == 'k':
                    print("Valid Sequence Group2")
                elif self.group2[0][0] == self.group2[1][0] == self.group2[2][0] == self.group2[3][0] and rankvalue[self.group2[0]]+3 == rankvalue[self.group2[1]]+2 == rankvalue[self.group2[2]]+1 == rankvalue[self.group2[3]]:
                    print("Valid Sequence Group2")
                else:
                    print("Invalid Sequence Group2")
                    for i in self.group2:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group2) == 3:  # joker=0 or 1
                if self.group2[0][0] == self.group2[1][0] == self.group2[2][0] and self.group2[0][1] == 'a' and self.group2[1][1] == 'q' and self.group2[2][1] == 'k':
                    print("Valid Sequence Group2")
                elif self.group2[0][0] == self.group2[1][0] == self.group2[2][0] and self.group2[0][1] == 'a' and self.group2[1][1] == '2' and self.group2[2][1] == 'k':
                    print("Valid Sequence Group2")
                elif self.group2[0][0] == self.group2[1][0] == self.group2[2][0] and rankvalue[self.group2[0]]+2 == rankvalue[self.group2[1]]+1 == rankvalue[self.group2[2]]:
                    print("Valid Sequence Group2")
                else:
                    print("Invalid Sequence Group2")
                    for i in self.group2:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group2) == 2:  # joker=1 or 2
                if self.group2[0][0] == self.group2[1][0] and self.group2[0][1] == 'a' and self.group2[1][1] == 'k':
                    print("Valid Sequence Group2")
                elif self.group2[0][0] == self.group2[1][0] and rankvalue[self.group2[0]]+1 == rankvalue[self.group2[1]]:
                    print("Valid Sequence Group2")
                else:
                    print("Invalid Sequence Group2")
                    for i in self.group2:
                        self.points+=pointvalue[i]
                    #invalid()
            elif len(self.group2) == 1:  # joker=2 or 3
                print("Valid Sequence Group2")
            elif len(self.group2) == 0:  # joker=3 or 4
                print("Valid Sequence Group2")

        print(self.points)

    def check_groups(self):
        """Checks if the length of declaration of all set/sequences is valid. Then it calls the functions to check the validity of pure, impure/pure,set/sequence,set/sequence. If all of them are valid it shows the result that the user won """
        global rankvalue

        print("user_pure", self.pure)
        print("user_impure", self.impure)
        print("user_group1", self.group1)
        print("user_group2", self.group2)

        screen.fill(blue)
        pygame.display.update()

        length = [len(self.pure), len(self.impure),
                  len(self.group1), len(self.group2)]
        print("length", length)
        length.sort()
        if length[0] == length[1] == length[2] == 3 and length[3] == 4:
            print("Valid length declaration")
        else:
            print("Invalid length declaration")
            tttemp=self.pure+self.impure+self.group1+self.group2
            for i in tttemp:
                self.points+=pointvalue[i]

            if self.points>80:
                self.points=80
                
            invalid()

        self.check_pure()
        self.check_impure()
        self.check_group1()
        self.check_group2()

        screen.fill(blue)
        pygame.display.update()

        if self.points==0:
            pygame.mixer.stop()
            file = "win music.mp3"
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(0)
            font = pygame.font.Font('freesansbold.ttf', 24)
            text = font.render('User:'+str(u.points)+'points', True, white, blue)
            textRect = text.get_rect()
            textRect.center = (550, 350)
            screen.blit(text, textRect)
            font = pygame.font.Font('freesansbold.ttf', 34)
            for i in range(2):
                text = font.render('You Win!', True, red, blue)
                textRect = text.get_rect()
                textRect.center = (550, 250)
                screen.blit(text, textRect)
                pygame.display.update()
                time.sleep(0.5)
                text = font.render('You Win!', True, green, blue)
                textRect = text.get_rect()
                textRect.center = (550, 250)
                screen.blit(text, textRect)
                pygame.display.update()
                time.sleep(0.5)
                text = font.render('You Win!', True, pink, blue)
                textRect = text.get_rect()
                textRect.center = (550, 250)
                screen.blit(text, textRect)
                pygame.display.update()
                time.sleep(1.5)
            quit()

        else:
            if self.points>80:
                self.points=80
            invalid()


class Computer:
    def __init__(self, computer, wj, sc):
        self.cards = computer
        self.wj = wj
        self.sc = sc
        self.picklist_puresequence = []
        self.puresequence = []
        self.picklist_impuresequence = []
        self.impuresequence = []
        self.group1 = []
        self.picklist_group1 = []
        self.group2 = []
        self.picklist_group2 = []

    def arrange(self):
        """After considering over a 100 sample cases, the best strategy for the computer to win would be if it created a pure sequence of 3 cards, an impure sequence of 4 cards, a set of 3 cards and a sequence of 3 cards. 
        In this function it first counts and stores the no of jokers the computer has. """
        global rankvalue

        jokercnt = 0
        joker = []
        for i in self.cards:
            if i == 'pj':
                jokercnt += 1
                joker.append(i)
                self.cards.remove(i)
            if i == ('c'+self.wj[1]) or i == ('s'+self.wj[1]) or i == ('d'+self.wj[1]) or i == ('h'+self.wj[1]):
                jokercnt += 1
                joker.append(i)
                self.cards.remove(i)
        print("computer jokers: ", joker)
        print()

        def card_sort():
            """ Sorts the card in the order a,2,3,4..j,q,k"""
            global rankvalue
            flag = 0

            for i in self.cards:
                if i == 'pj':
                    flag = 1
                    self.cards.remove('pj')

            self.cards = sorted(
                self.cards, key=lambda x: (x[0], rankvalue[x]))

            if flag == 1:
                self.cards.append('pj')

        def get_key(val, alpha):
            """ returns the card corresponding to the rankvalue and the given suit"""
            for key, value in rankvalue.items():
                if val == value and key[0] == alpha:
                    return key

        def pureseq():
            # group of 3
            # check for sequences (same suit) - PURE
            global rankvalue

            # not checking if it exists for 4 cards because it's probability to be found is really really low

            # checking if it exists for 3 cards
            for i, j, k in zip(self.cards, self.cards[1:], self.cards[2:]):
                if i[0] == j[0] == k[0] and rankvalue[i]+2 == rankvalue[j]+1 == rankvalue[k]:
                    self.puresequence = [i, j, k]
                    self.cards.remove(i)
                    self.cards.remove(j)
                    self.cards.remove(k)
                    break

            # if not then picking 2 consecutive cards to form a pure sequence
            if len(self.puresequence) == 0:
                for i, j in zip(self.cards, self.cards[1:]):
                    if i[0] == j[0] and rankvalue[i]+1 == rankvalue[j]:
                        self.puresequence = [i, j]
                        if i[1] == 'a':
                            self.picklist_puresequence.append(i[0]+'k')
                            self.picklist_puresequence.append(
                                get_key(rankvalue[j]+1, i[0]))
                        elif j[1] == 'k':
                            self.picklist_puresequence.append(i[0]+'a')
                            self.picklist_puresequence.append(
                                get_key(rankvalue[i]-1, i[0]))
                        else:
                            self.picklist_puresequence.append(
                                get_key(rankvalue[i]-1, i[0]))
                            self.picklist_puresequence.append(
                                get_key(rankvalue[j]+1, i[0]))

                        self.cards.remove(i)
                        self.cards.remove(j)
                        break

            # if can't then finding sequence with a card missing in between
            if len(self.puresequence) == 0:
                for i, j in zip(self.cards, self.cards[1:]):
                    if i[0] == j[0] and rankvalue[i]+2 == rankvalue[j]:
                        self.puresequence = [i, j]
                        self.picklist_puresequence.append(
                            get_key(rankvalue[i]+1, i[0]))
                        self.cards.remove(i)
                        self.cards.remove(j)
                        break
                for k in joker:  # checking if puresequence can be formed using joker
                    if self.picklist_puresequence[0] == k:
                        joker.remove(k)
                        self.puresequence.append(k)

            # if can't then make the first card of computer for pure sequence
            if len(self.puresequence) == 0:
                i = self.cards[0]
                self.puresequence = [i]
                self.cards.remove(i)
                if i[1] == 'a':
                    self.picklist_puresequence.append(i[0]+'k')
                    self.picklist_puresequence.append(
                        get_key(rankvalue[i]+1, i[0]))
                elif i[1] == 'k':
                    self.picklist_puresequence.append(i[0]+'a')
                    self.picklist_puresequence.append(
                        get_key(rankvalue[i]-1, i[0]))
                else:
                    self.picklist_puresequence.append(
                        get_key(rankvalue[i]-1, i[0]))
                    self.picklist_puresequence.append(
                        get_key(rankvalue[i]+1, i[0]))

            print("puresequence:", self.puresequence)
            print("picklist_puresequence: ", self.picklist_puresequence)
            print()

        card_sort()
        pureseq()

        def impureseq():
            # group of 4
            # check for sequences (same suit) - IMPURE/PURE
            global rankvalue

            if jokercnt == 4:  # impure sequence is complete
                self.impuresequence = list(joker)
                self.picklist_impuresequence = []

            if jokercnt == 3:  # impure sequence is completed by taking one card form the computer cards
                self.impuresequence = list(joker)
                self.picklist_impuresequence = []
                self.impuresequence.append(self.cards[0])
                self.cards.remove(self.cards[0])

            if jokercnt == 2:
                self.impuresequence = list(joker)
                # look for sequence of 2 cards
                for i, j in zip(self.cards, self.cards[1:]):
                    if i[0] == j[0] and rankvalue[i]+1 == rankvalue[j]:
                        self.impuresequence.append(i)
                        self.impuresequence.append(j)
                        self.cards.remove(i)
                        self.cards.remove(j)
                        break

                # if not present then select one computer card
                if len(self.impuresequence) == 2:
                    i = self.cards[0]
                    self.impuresequence.append(i)
                    self.cards.remove(i)
                    if i[1] == 'a':
                        self.picklist_impuresequence.append(i[0]+'k')
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[j]+1, i[0]))
                    elif j[1] == 'k':
                        self.picklist_impuresequence.append(i[0]+'a')
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[i]-1, i[0]))
                    else:
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[i]-1, i[0]))
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[j]+1, i[0]))

            if jokercnt == 1:
                self.impuresequence = list(joker)
                # look for sequence of 3
                for i, j, k in zip(self.cards, self.cards[1:], self.cards[2:]):
                    if i[0] == j[0] == k[0] and rankvalue[i]+2 == rankvalue[j]+1 == rankvalue[k]:
                        self.impuresequence.append(i)
                        self.impuresequence.append(j)
                        self.impuresequence.append(k)
                        self.cards.remove(i)
                        self.cards.remove(j)
                        self.cards.remove(k)
                        break

                # if not present then look for sequence of consecutive 2
                if len(self.impuresequence) == 1:
                    for i, j in zip(self.cards, self.cards[1:]):
                        if i[0] == j[0] and rankvalue[i]+1 == rankvalue[j]:
                            self.impuresequence.append(i)
                            self.impuresequence.append(j)
                            self.cards.remove(i)
                            self.cards.remove(j)
                            if i[1] == 'a':
                                self.picklist_impuresequence.append(i[0]+'k')
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[j]+1, i[0]))
                            elif j[1] == 'k':
                                self.picklist_impuresequence.append(i[0]+'a')
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[i]-1, i[0]))
                            else:
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[i]-1, i[0]))
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[j]+1, i[0]))

                            break

                # if not prsent then look for sequence with a card missing in between
                if len(self.impuresequence) == 1:
                    for i, j in zip(self.cards, self.cards[1:]):
                        if i[0] == j[0] and rankvalue[i]+2 == rankvalue[j]:
                            self.impuresequence.append(i)
                            self.impuresequence.append(j)
                            self.cards.remove(i)
                            self.cards.remove(j)
                            self.picklist_impuresequence.append(
                                get_key(rankvalue[i]+1, i[0]))

                            break

                # if not present then select one card from computer cards
                if len(self.impuresequence) == 1:
                    i = self.cards[0]
                    self.impuresequence.append(i)
                    self.cards.remove(i)
                    if i[1] == 'a':
                        self.picklist_impuresequence.append(i[0]+'k')
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[i]+1, i[0]))
                    elif i[1] == 'k':
                        self.picklist_impuresequence.append(i[0]+'a')
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[i]-1, i[0]))
                    else:
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[i]-1, i[0]))
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[i]+1, i[0]))

            if jokercnt == 0:
                # look for sequence of 4
                for i, j, k, l in zip(self.cards, self.cards[1:], self.cards[2:], self.cards[3:]):
                    if i[0] == j[0] == k[0] == l[0] and rankvalue[i]+3 == rankvalue[j]+2 == rankvalue[k]+1 == rankvalue[l]:
                        self.impuresequence = [i, j, k, l]
                        self.cards.remove(i)
                        self.cards.remove(j)
                        self.cards.remove(k)
                        self.cards.remove(l)
                        break

                # if not present then check for sequence of 3 cards
                if len(self.impuresequence) == 0:
                    for i, j, k in zip(self.cards, self.cards[1:], self.cards[2:]):
                        if i[0] == j[0] == k[0] and rankvalue[i]+2 == rankvalue[j]+1 == rankvalue[k]:
                            self.impuresequence = [i, j, k]
                            self.cards.remove(i)
                            self.cards.remove(j)
                            self.cards.remove(k)
                            if i[1] == 'a':
                                self.picklist_impuresequence.append(i[0]+'k')
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[k]+1, i[0]))
                            elif k[1] == 'k':
                                self.picklist_impuresequence.append(i[0]+'a')
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[i]-1, i[0]))
                            else:
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[i]-1, i[0]))
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[k]+1, i[0]))
                            break

                # if not present then check for consecutive sequence of 2 cards
                if len(self.impuresequence) == 0:
                    for i, j in zip(self.cards, self.cards[1:]):
                        if i[0] == j[0] and rankvalue[i]+1 == rankvalue[j]:
                            self.impuresequence.append(i)
                            self.impuresequence.append(j)
                            self.cards.remove(i)
                            self.cards.remove(j)
                            if j[1] == 'k':
                                self.picklist_impuresequence.append(i[0]+'a')
                                self.picklist_impuresequence.append(i[0]+'2')
                            elif j[1] == 'q':
                                self.picklist_impuresequence.append(i[0]+'k')
                                self.picklist_impuresequence.append(i[0]+'a')
                            else:
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[j]+1, i[0]))
                                self.picklist_impuresequence.append(
                                    get_key(rankvalue[j]+2, i[0]))
                            break

                # if not present then pick one from computer cards
                if len(self.impuresequence) == 0:
                    i = self.cards[0]
                    self.impuresequence.append(i)
                    self.cards.remove(i)
                    if i[1] == 'k':
                        self.picklist_impuresequence.append(i[0]+'a')
                        self.picklist_impuresequence.append(i[0]+'2')
                        self.picklist_impuresequence.append(i[0]+'3')
                    elif i[1] == 'q':
                        self.picklist_impuresequence.append(i[0]+'k')
                        self.picklist_impuresequence.append(i[0]+'a')
                        self.picklist_impuresequence.append(i[0]+'2')
                    elif i[1] == 'j':
                        self.picklist_impuresequence.append(i[0]+'q')
                        self.picklist_impuresequence.append(i[0]+'k')
                        self.picklist_impuresequence.append(i[0]+'a')
                    else:
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[i]+1, i[0]))
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[i]+2, i[0]))
                        self.picklist_impuresequence.append(
                            get_key(rankvalue[i]+3, i[0]))

            print("impuresequence: ", self.impuresequence)
            print("picklist_impuresequence: ",
                  self.picklist_impuresequence)
            print()

        impureseq()

        def grp1():
            # group of 3
            # check for set
            global rankvalue

            self.cards = sorted(self.cards, key=lambda x: (rankvalue[x]))

            # checking if it exists for 3 cards
            for i, j, k in zip(self.cards, self.cards[1:], self.cards[2:]):
                if i[1] == j[1] == k[1]:
                    self.group1 = [i, j, k]
                    self.cards.remove(i)
                    self.cards.remove(j)
                    self.cards.remove(k)
                    break

            # if not then picking 2 cards of same rankvalue
            s = ['c', 'd', 'h', 's']
            if len(self.group1) == 0:
                for i, j in zip(self.cards, self.cards[1:]):
                    if i[1] == j[1]:
                        self.group1 = [i, j]
                        s.remove(i[0])  # removing suit selected
                        s.remove(j[0])
                        self.picklist_group1.append(s[0]+i[1])
                        self.picklist_group1.append(s[1]+i[1])
                        self.cards.remove(i)
                        self.cards.remove(j)
                        break

            # if not then picking one card
            s = ['c', 'd', 'h', 's']
            if len(self.group1) == 0:
                i = self.cards[0]
                self.group1 = [i]
                self.cards.remove(i)
                s.remove(i[0])
                self.picklist_group1.append(s[0]+i[1])
                self.picklist_group1.append(s[1]+i[1])
                self.picklist_group1.append(s[2]+i[1])

            print("group1:", self.group1)
            print("picklist_group1: ", self.picklist_group1)
            print()

        grp1()

        def grp2():
            # group of 3
            # check for sequence
            card_sort()
            global rankvalue

            # checking if it exists for 3 cards
            for i, j, k in zip(self.cards, self.cards[1:], self.cards[2:]):
                if i[0] == j[0] == k[0] and rankvalue[i]+2 == rankvalue[j]+1 == rankvalue[k]:
                    self.group2 = [i, j, k]
                    self.cards.remove(i)
                    self.cards.remove(j)
                    self.cards.remove(k)
                    break

            # if not then picking 2 consecutive cards
            if len(self.group2) == 0:
                for i, j in zip(self.cards, self.cards[1:]):
                    if i[0] == j[0] and rankvalue[i]+1 == rankvalue[j]:
                        self.group2 = [i, j]
                        self.cards.remove(i)
                        self.cards.remove(j)
                        if i[1] == 'a':
                            self.picklist_group2.append(i[0]+'k')
                            self.picklist_group2.append(
                                get_key(rankvalue[j]+1, i[0]))
                        elif j[1] == 'k':
                            self.picklist_group2.append(i[0]+'a')
                            self.picklist_group2.append(
                                get_key(rankvalue[i]-1, i[0]))
                        else:
                            self.picklist_group2.append(
                                get_key(rankvalue[i]-1, i[0]))
                            self.picklist_group2.append(
                                get_key(rankvalue[j]+1, i[0]))
                        break

            # if can't then finding sequence with a card missing in between
            if len(self.group2) == 0:
                for i, j in zip(self.cards, self.cards[1:]):
                    if i[0] == j[0] and rankvalue[i]+2 == rankvalue[j]:
                        self.group2 = [i, j]
                        self.cards.remove(i)
                        self.cards.remove(j)
                        self.picklist_group2.append(
                            get_key(rankvalue[i]+1, i[0]))
                        break

            # if can't then make the pick the first card from computer cards
            if len(self.group2) == 0:
                i = self.cards[0]
                self.group2 = [i]
                self.cards.remove(i)
                if i[1] == 'a':
                    self.picklist_group2.append(i[0]+'k')
                    self.picklist_group2.append(get_key(rankvalue[i]+1, i[0]))
                elif i[1] == 'k':
                    self.picklist_group2.append(i[0]+'a')
                    self.picklist_group2.append(get_key(rankvalue[i]-1, i[0]))
                else:
                    self.picklist_group2.append(get_key(rankvalue[i]-1, i[0]))
                    self.picklist_group2.append(get_key(rankvalue[i]+1, i[0]))

            print("Group2:", self.group2)
            print("picklist_group2: ", self.picklist_group2)
            print()

        grp2()

        ttemp = ['pj', 'c'+self.wj[1], 'd'+self.wj[1], 'h'+self.wj[1],
                 's'+self.wj[1]]  # list of all jokers in the game

        # appending them to all the picklists except puresequence
        for i in ttemp:
            self.picklist_impuresequence.append(i)
            self.picklist_group1.append(i)
            self.picklist_group2.append(i)

        # emptying picklist if the group is complete
        if len(self.impuresequence) == 4:
            self.picklist_impuresequence = []
        if len(self.group1) == 3:
            self.picklist_group1 = []
        if len(self.group2) == 3:
            self.picklist_group2 = []

        print("Computer cards after arrangement", self.cards)
        print()

    def move(self):
        """ Decides if the card is to be picked form the opendeck or closed deck. If the card in the opendeck is present in any of the picklist in the order - pure,impure,group1,group2 (This is because pure sequence has the highest priority as a game can't be won without it, followed by impure sequence which is hard to complete because it is a group of 4 cards, followe by group1 which is a set and hence harder to make than a sequence), it picks it,e lse it picks a card from the opendeck.It checks if the computer can declare that is all the sequence/set is complete at every step."""
        global userturn
        global opendeck
        global cards

        def check_for_declare():
            if len(self.puresequence) == 3 and len(self.impuresequence) == 4 and len(self.group1) == 3 and len(self.group2) == 3:
                return True

        if opendeck[-1] in self.picklist_puresequence:
            print()
            print("Picked card by computer: ", opendeck[-1])
            self.puresequence.append(opendeck[-1])
            self.picklist_puresequence.remove(opendeck[-1])
            opendeck.pop()
            r = pygame.Rect((746, 301), (73, 105))
            screen.fill(blue, r)
            pygame.display.update()
            if len(self.puresequence) == 3:
                self.picklist_puresequence = []

            if check_for_declare() == True:
                u.declare()
            else:
                throw = self.cards[0]
                print("Thrown card by computer: ", throw)
                opendeck.append(throw)
                self.cards.remove(throw)
                print_rest()

        elif opendeck[-1] in self.picklist_impuresequence:
            print("Picked card by computer: ", opendeck[-1])
            self.impuresequence.append(opendeck[-1])
            self.picklist_impuresequence.remove(opendeck[-1])
            opendeck.pop()
            r = pygame.Rect((746, 301), (73, 105))
            screen.fill(blue, r)
            pygame.display.update()
            if len(self.impuresequence) == 4:
                self.picklist_impuresequence = []

            if check_for_declare() == True:
                u.declare()
            else:
                throw = self.cards[0]
                print("Thrown card by computer: ", throw)
                opendeck.append(throw)
                self.cards.remove(throw)
                print_rest()

        elif opendeck[-1] in self.picklist_group1:
            print("Picked card by computer: ", opendeck[-1])
            self.group1.append(opendeck[-1])
            self.picklist_group1.remove(opendeck[-1])
            opendeck.pop()
            r = pygame.Rect((746, 301), (73, 105))
            screen.fill(blue, r)
            pygame.display.update()
            if len(self.group1) == 3:
                self.picklist_group1 = []

            if check_for_declare() == True:
                u.declare()
            else:
                throw = self.cards[0]
                print("Thrown card by computer: ", throw)
                opendeck.append(throw)
                self.cards.remove(throw)
                print_rest()

        elif opendeck[-1] in self.picklist_group2:
            print("Picked card by computer: ", opendeck[-1])
            self.group2.append(opendeck[-1])
            self.picklist_group2.remove(opendeck[-1])
            opendeck.pop()
            r = pygame.Rect((746, 301), (73, 105))
            screen.fill(blue, r)
            pygame.display.update()
            if len(self.group2) == 3:
                self.picklist_group2 = []

            if check_for_declare() == True:
                u.declare()
            else:
                throw = self.cards[0]
                print("Thrown card by computer: ", throw)
                opendeck.append(throw)
                self.cards.remove(throw)
                print_rest()

        else:  # Picking from closed deck
            if len(cards) == 0:
                random.shuffle(opendeck)
                cards = opendeck
                opendeck = []
                r = pygame.Rect((746, 301), (73, 105))
                screen.fill(blue, r)
                pygame.display.update()

            # temp is the card picked from closed deck
            temp = random.choice(cards)
            print("Picked card by computer: ", temp)
            self.cards.append(temp)
            cards.remove(temp)

            if temp in self.picklist_puresequence:
                self.cards.remove(temp)
                self.puresequence.append(temp)
                self.picklist_puresequence.remove(temp)
                if len(self.puresequence) == 3:
                    self.picklist_puresequence = []
                if check_for_declare() == True:
                    u.declare()

            elif temp in self.picklist_impuresequence:
                self.cards.remove(temp)
                self.impuresequence.append(temp)
                self.picklist_impuresequence.remove(temp)
                if len(self.impuresequence) == 4:
                    self.picklist_impuresequence = []
                if check_for_declare() == True:
                    u.declare()

            elif temp in self.picklist_group2:
                self.cards.remove(temp)
                self.group2.append(temp)
                self.picklist_group2.remove(temp)
                if len(self.group2) == 3:
                    self.picklist_group2 = []
                if check_for_declare() == True:
                    u.declare()

            elif temp in self.picklist_group1:
                self.cards.remove(temp)
                self.group1.append(temp)
                self.picklist_group1.remove(temp)
                if len(self.group1) == 3:
                    self.picklist_group1 = []
                if check_for_declare() == True:
                    u.declare()

            if check_for_declare() == True:
                u.declare()
            else:
                throw = self.cards[0]
                print("Thrown card by computer: ", throw)
                opendeck.append(throw)
                self.cards.remove(throw)
                time.sleep(2)
                print_rest()

        print()
        print("puresequence:", self.puresequence)
        print("picklist_puresequence: ", self.picklist_puresequence)
        print()
        print("impuresequence:", self.impuresequence)
        print("picklist_impuresequence: ",
              self.picklist_impuresequence)
        print()
        print("group1:", self.group1)
        print("picklist_group1: ", self.picklist_group1)
        print()
        print("group2:", self.group2)
        print("picklist_group2: ", self.picklist_group2)
        print()
        print("Computer card after throw:", self.cards)
        print("Open Deck: ", opendeck)
        print("Closed Deck", cards)
        print()

        # making screen blue again so Turn:USER can be displayed
        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render('Turn:COMPUTER', True, blue, blue)
        textRect = text.get_rect()
        textRect.center = (1000, 300)
        screen.blit(text, textRect)
        pygame.display.update()

        userturn = 1  # indicates it is the user's turn
        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render('Turn:USER', True, white, blue)
        textRect = text.get_rect()
        textRect.center = (1000, 300)
        screen.blit(text, textRect)
        pygame.display.update()

    def declare(self):
        #It declares the computer as the winner
        screen.fill(blue)
        pygame.display.update()

        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render('Winner:Computer', True, white, blue)
        textRect = text.get_rect()
        textRect.center = (560, 450)
        screen.blit(text, textRect)
        pygame.display.update()

        font = pygame.font.Font('freesansbold.ttf', 34)
        for i in range(2):
            text = font.render('You Lose!', True, red, blue)
            textRect = text.get_rect()
            textRect.center = (550, 250)
            screen.blit(text, textRect)
            pygame.display.update()
            time.sleep(0.5)
            text = font.render('You Lose!', True, green, blue)
            textRect = text.get_rect()
            textRect.center = (550, 250)
            screen.blit(text, textRect)
            pygame.display.update()
            time.sleep(0.5)
            text = font.render('You Lose!', True, pink, blue)
            textRect = text.get_rect()
            textRect.center = (550, 250)
            screen.blit(text, textRect)
            pygame.display.update()
            time.sleep(0.5)
        quit()
        

def create_deck():
    """Creating the deck to play the game """
    for j in suit:
        for i in range(1, 14):
            if i == 1:
                cards.append(j+'a')
            elif i == 11:
                cards.append(j+'j')
            elif i == 12:
                cards.append(j+'q')
            elif i == 13:
                cards.append(j+'k')
            else:
                cards.append(j+str(i))

    cards.append('pj')


def assign_cards():
    """ Assigning cards to computer and user, selecting a wj that is not 10 (difficult to check later) 
        or a pj (because then all aces become a wj, so might as well remove the possiblity of a pj
        printed joker then),selecting a starting card for the open deck"""
    global wj
    global sc
    global opendeck
    # assigning cards to computer
    for i in range(13):
        temp = random.choice(cards)
        computer.append(temp)
        cards.remove(temp)

    # assigning cards to user
    for i in range(13):
        temp = random.choice(cards)
        user.append(temp)
        cards.remove(temp)

    # assigning a wild joker
    wj = random.choice(cards)
    while wj[1] == '1' or wj == 'pj':
        wj = random.choice(cards)

    cards.remove(wj)

    # assigning a starting card
    sc = random.choice(cards)
    cards.remove(sc)
    opendeck.append(sc)


def print_cards():
    """ Prints the user and computer cards on screen"""
    x = 0
    for i in user:
        image = pygame.image.load("images/cards/"+i+".png")
        screen.blit(image, (x, (b-105)))
        pygame.display.update()
        x = x+74

    x = 1200-74
    for i in range(13):
        image = pygame.image.load("images/cards/back.png")
        screen.blit(image, (x, 0))
        pygame.display.update()
        x = x-74


def print_rest():
    """"Prints other things like the drop, declare, wild joker, closed deck,opendeck,sort option """
    image = pygame.image.load("images/drop.png")
    screen.blit(image, (10, 10))
    image = pygame.image.load("images/tap.png")
    screen.blit(image, (155, 300))
    image = pygame.image.load("images/cards/"+wj+".png")
    image = pygame.transform.rotate(image, 30)
    screen.blit(image, (400, 290))
    image = pygame.image.load("images/cards/back.png")
    screen.blit(image, (450, 290))
    image = pygame.image.load("images/cards/"+opendeck[-1]+".png")
    screen.blit(image, (745, 300))
    image = pygame.image.load("images/sort.png")
    screen.blit(image, (8, 550))
    pygame.display.update()


def invalid():
    """ Prints result when there is an invalid declaration of sequence/set/length"""
    print("User points:",u.points)
    font = pygame.font.Font('freesansbold.ttf', 24)
    text = font.render('Invalid Delaration', True, white, blue)
    textRect = text.get_rect()
    textRect.center = (550, 150)
    screen.blit(text, textRect)
    text = font.render('User:'+str(u.points)+'points', True, white, blue)
    textRect = text.get_rect()
    textRect.center = (550, 350)
    screen.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 34)
    for i in range(2):
        text = font.render('You Lose!', True, red, blue)
        textRect = text.get_rect()
        textRect.center = (550, 250)
        screen.blit(text, textRect)
        pygame.display.update()
        time.sleep(0.5)
        text = font.render('You Lose!', True, green, blue)
        textRect = text.get_rect()
        textRect.center = (550, 250)
        screen.blit(text, textRect)
        pygame.display.update()
        time.sleep(0.5)
        text = font.render('You Lose!', True, pink, blue)
        textRect = text.get_rect()
        textRect.center = (550, 250)
        screen.blit(text, textRect)
        pygame.display.update()
        time.sleep(0.5)
    quit()


def music(songno):
    """ Plays music"""
    global songlist
    file = "music/"+songlist[songno]
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(0)


file = "intro.mp3"
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(0)
image = pygame.image.load("images/welcome.png")
screen.blit(image, (0, 0))
pygame.display.update()
time.sleep(1.5)
image = pygame.image.load("images/title.png")
screen.blit(image, (300, 0))
pygame.display.update()
time.sleep(2)
image = pygame.image.load("images/name.png")
screen.blit(image, (0, 450))
pygame.display.update()
time.sleep(2)


screen.fill(blue)
music(songno)
create_deck()
assign_cards()
print_cards()
print_rest()
print("Wild Joker:", wj)
print("Computer Cards:", computer)
print("User Cards: ", user)
print()

#user = ['da', 'd2', 'd3', 'd4', 'd5', 'd6','d7', 'd8', 'd9', 'd10', 'dj', 'dq', 'dk']

c = Computer(computer, wj, sc)
c.arrange()

u = User(user, wj, sc)

userturn = 1
declared = 0
ok = 0
font = pygame.font.Font('freesansbold.ttf', 24)
text = font.render('Turn:USER', True, white, blue)
textRect = text.get_rect()
textRect.center = (1000, 300)
screen.blit(text, textRect)
pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                songno += 1
                if songno == len(songlist):
                    songno = 0
                music(songno)

        if event.type == pygame.MOUSEBUTTONDOWN:
            xx, yy = event.pos
            if 10 < yy < 10+38 and 10 < xx < 10+132 and len(u.cards) == 13 and declared == 0:
                c.declare()

            if b-105 < yy < b and xx <= 74*13 and len(u.cards) == 13 and declared == 0:
                u.highlight_card(xx//74)

            if b-105 < yy < b and xx <= 74*(len(u.cards)) and declared == 1 and ok == 0:
                u.accept_groups(xx//74)  # works for pure sequence

            if 550 < yy < 550+39 and 1000 < xx < 1000+132 and declared == 1 and ok == 0:  # click on ok
                ok = 1
                for i in u.pure:
                    u.cards.remove(i)

                screen.fill(blue)
                pygame.display.update()
                text = font.render(
                    'Select Another Sequence and then tap OK', True, white, blue)
                textRect = text.get_rect()
                textRect.center = (500, 150)
                screen.blit(text, textRect)
                image = pygame.image.load("images/ok.png")
                screen.blit(image, (850, 550))
                u.print_cards()
                pygame.display.update()

            if b-105 < yy < b and xx <= 74*(len(u.cards)) and declared == 1 and ok == 1:
                u.accept_groups(xx//74)  # works for impure sequence

            if 550 < yy < 550+39 and 850 < xx < 850+132 and declared == 1 and ok == 1:
                ok = 2
                for i in u.impure:
                    u.cards.remove(i)

                screen.fill(blue)
                pygame.display.update()
                text = font.render(
                    'Select a Set/Sequence and then tap OK', True, white, blue)
                textRect = text.get_rect()
                textRect.center = (500, 150)
                screen.blit(text, textRect)
                image = pygame.image.load("images/ok.png")
                screen.blit(image, (700, 550))
                u.print_cards()
                pygame.display.update()

            if b-105 < yy < b and xx <= 74*(len(u.cards)) and declared == 1 and ok == 2:
                u.accept_groups(xx//74)  # works for group1

            if 550 < yy < 550+39 and 700 < xx < 700+132 and declared == 1 and ok == 2:
                ok = 3
                for i in u.group1:
                    u.cards.remove(i)

                u.accept_groups(xx//74)

            if b-105 < yy < b and xx <= 74*14 and len(u.cards) == 14 and declared == 0:
                u.highlight_card(xx//74)

            if 745 < xx < 820 and 300 < yy < 407 and len(u.cards) == 13 and userturn == 1 and declared == 0:
                u.pick_card_open_deck()
            elif 745 < xx < 820 and 300 < yy < 407 and len(u.cards) == 14 and userturn == 1 and len(u.swapcard) == 1 and declared == 0:
                u.throw_card()

            if 450 < xx < 525 and 290 < yy < 398 and len(u.cards) == 13 and userturn == 1 and declared == 0:
                u.pick_card_closed_deck()

            if 8 <= xx < 140 and 550 < yy < 589 and declared == 0:
                u.sort()

            if 155 <= xx < 229 and 300 < yy < 405 and len(u.cards) == 14 and userturn == 1 and len(u.swapcard) == 1 and declared == 0:
                u.cards.remove(u.swapcard[0])
                u.declare()


pygame.quit()
