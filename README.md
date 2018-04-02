# GA-Hearthstone
The purpose of this project is to use Genetic Algorithm to find out deck building strategies that could achieve the best mana curve in Hearthstone.

Requires python 2.7

Run "./ga-hs.py [MaxTurn N] [ManaEfficiencyDecay r] [parity option]" to start simulation.


parity options:
- 0: No parity. Cards will use randomized cost between 1 to 10
- 1: Odd parity. Cards will use randomized cost among 1,3,5,7,9
- 2: Even parity. Cards will use randomized cost among 2,4,6,8,10

By default, N=10, r=0.9, parity option = 0;


The result will be printed in console. Average scores of each generation's "Champion" will also be output to result.csv

