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
After considering over a 100 sample cases, the best strategy for the computer to win would be if it created a pure sequence of 3 cards, an impure sequence of 4 cards, a set of 3 cards and a sequence of 3 cards.

Following is the order followed by the computer.

**Arranging its Card**
1. The computer counts and stores the number of jokers it has, removing them from its deck.
2. It sorts the remaining computer deck in the order a,2,3,4,...j,q,k.
3. It tries to form a pure sequence (same suit) of 3 cards, eg (a3,a4,a5). - Pure<br>
⋅⋅1.


..1. If that does not exist then it tries to pick 2 consecutive cards to form a pure sequence, and adds the possible cards to complete the sequence in its picklist.
 eg. It picks (a3,a4) and adds (a2,a5) to its picklist.
If that also does not exist then it tries to pick a sequence with a card missing in between, and adds the possible card to complete the sequence in its picklist.
 eg. It picks (a3,a5) and adds (a4) to its picklist.
If that also does not exist then it picks the first card the computer has left, and adds the possible cards to complete the sequence in its picklist.
 eg. It picks (a4) and adds (a3,a5) to its picklist.
It tries to form an impure/pure sequence (same suit) of 4 cards, eg. (pj,a2,a3,a4) - Impure
If it has 4 jokers then the sequence is complete. 
Else if it has 3 jokers then the sequence is completed by taking one card from the computer deck.
Else if it has 2 jokers then it looks for a sequence of 2 cards. If that is not found then it picks one card from the computer deck and adds the possible card in its picklist. 
eg. It picks (a4) and adds (a3,a5) to its picklist.
Else if it has 1 joker then it looks for a sequence of 3 cards. 
If that is not found then it looks for a sequence of 2 consecutive cards and updates its picklist.
eg. It picks (a3,a4) and adds (a2, a5) to its picklist.
If that is also not found then it looks for a sequence with a card missing in between and updates its picklist.
eg. It picks (a3,a5) and adds (a4) to its picklist.
If that is also not found then it picks one card from the computer deck and  updates its picklist.
eg. It picks (a3) and adds (a2,a4) to its picklist.
Else if has 0 jokers then it looks for a sequence of 4 cards
If that is not found then it looks for a sequence of 3 consecutive cards and updates its picklist. 
eg. It picks (a3,a4,a5) and adds (a2, a6) to its picklist.
If that is not found then it looks for a sequence of 2 consecutive cards and updates its picklist.
eg. It picks (a3,a4) and adds (a5, a6) to its picklist.
If that is also not found then it picks one card from the computer deck and adds the possible cards in its picklist.
eg. It picks (a3) and adds (a4,a5,a6) to its picklist.
It sorts the remaining computer deck according to rank value.
It tries to form a set  (same rank) of 3 cards, eg. (a3,c3,h3) - Group 1
If that does not exist then it looks for 2 cards with the same rank value and updates the picklist.
eg. It picks (a3,h3) and adds (c3,d3) to its picklist.
If that is also not found then it picks one card from the computer deck and updates its picklist. 
eg. It picks (a3) and adds (h3,c3,d3) to its picklist.
It sorts the remaining computer deck in the order a,2,3,4,...j,q,k.
It tries to form a sequence (same suit) of 3 cards, eg. (a3,a4,a5). - Group 2
If that does not exist then it tries to pick 2 consecutive cards and updates its picklist.
 eg. It picks (a3,a4) and adds (a2,a5) to its picklist.
If that also does not exist then it tries to pick a sequence with a card missing in between and updates its picklist.
 eg. It picks (a3,a5) and adds (a4) to its picklist.
If that also does not exist then it picks the first card the computer has left and updates its picklist.
 eg. It picks (a4) and adds (a3,a5) to its picklist.
It adds all the jokers in all the 3 picklists except the pure sequence picklist.
It empties the picklist if the set/sequence is complete
Deciding its Move
If the card in the opendeck is present in any of the picklist in the order - pure, impure, group1, group2 (This is because pure sequence has the highest priority as a game can't be won without it, followed by impure sequence which is hard to complete because it is a group of 4 cards, followed by group1 which is a set and hence harder to make than a sequence), it picks it, else it picks a card from the opendeck.It checks if the computer can declare that is all the sequence/set is complete at every step.





