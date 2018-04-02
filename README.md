# GA-Hearthstone
The purpose of this project is to use Genetic Algorithm to find out deck building strategies that could achieve the best mana curve in Hearthstone.

Requires python 2.7

Run "./ga-hs.py [number of decks] [number of generations] [parity option]" to start simulation.

parity options:
- 0: No parity. Cards will use randomized cost between 1 to 10
- 1: Odd parity. Cards will use randomized cost among 1,3,5,7,9
- 2: Even parity. Cards will use randomized cost among 2,4,6,8,10


The result will be printed in console. Average scores of each generation's "Champion" will also be output to result.csv

