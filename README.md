# points-rummy
This is a game called Points Rummy. An indian variation of the popular game Rummy which I made in my first semester at IIITD for my course Intro to Programming.

## Usage
- It is written in Python3.6.9 and implemented using pygame. 
- Open terminal and navigate to the directory Points Rummy.
- Run PointsRummy.py using the following command 
```
python3 PointsRummy.py
```
## Logic
The 13 cards for both the user and the computer are randomly distributed.

### Logic for Computer
After considering over a 100 sample cases, the best strategy for the computer to win would be if it created a pure sequence of 3 cards, an impure sequence of 4 cards, a set of 3 cards and a sequence of 3 cards. <br>

- The computer first counts and stores the number of jokers it has removing it from its deck.
- It then sorts the remaining cards in the order a,2,3,4,...j,q,k.
- First it tries to form a pure sequence (same suit) of 3 cards, eg (a3,a4,a5). <br>
  - If it does not exist then it tries to pick 2 consecutive cards to form a pure sequence,  and adds the possible cards to complete the sequence in its picklist.<br>
eg. It picks (a3,a4) and adds (a2,a5) to its picklist.
  - If that also does not exist then it tries to pick a sequence with a card missing in between, and adds the possible card to complete the sequence in its picklist.<br>
eg. It picks (a3,a5) and adds (a4) to its picklist.
  - If that also does not exist then it picks the first card the computer has left, and adds the possible card to complete the sequence in its picklist.<br>
eg. It picks (a4) and adds (a3,a5) to its picklist. 
- The computer then tries to form an impure sequence (same suit) 



