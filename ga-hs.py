#!/usr/bin/env python3
import random, sys, csv, time, statistics

# GA parameters
COMPETE_ROUNDS = 5 # number of rounds that a deck takes to compute its score upon one iteration
MUTATION_PROBABILITY = 0.3 # chance of mutation happen upon birth
MUTATION_AMOUNT = 0.3 # when mutation happens, the amount of genes to randomize
CHAMPIONS_TO_COPY = 5 # number of champions to directly copy from last generation
num_decks = 40 # total number of decks in the race
num_rounds = 500 # total number of iterations would the race take to complete

# Game Constants
HAND_LIMIT = 10
HAND_START = 3
MANA_LIMIT = 10
DECK_CARD_COUNT = 30

# Game Values
TURN_LIMIT = 10
MANA_VALUE_DECAY_RATE = 0.85



start_time = time.time()
avg_scores = []

class Card:
	cost = 0
	def __init__(self, n=None):
		if n is None:
			self.cost = 0
		else:
			self.cost = n
	def randomize(self):
		global parity

		if parity == 1:
			self.cost = random.randint(1, 5) * 2 -1
		elif parity == 2:
			self.cost = random.randint(1, 5) * 2
		else:
			self.cost = random.randint(1, 10)

	def copy(self):
		return Card(self.cost)

class Deck:
	cards = []
	latest_score = 0
	def init_cards(self):
		self.latest_score = 0
		self.cards = []
		for i in range(0, DECK_CARD_COUNT):
			new_card = Card()
			new_card.randomize()
			self.cards.append(new_card)

	def copy(self):
		deck_copy = Deck()
		for c in self.cards:
			deck_copy.cards.append(c.copy())
		return deck_copy

	def inherit(self, winner_decks):
		self.latest_score = 0
		self.cards = []
		for i in range(0, DECK_CARD_COUNT):
			j = random.randint(0, len(winner_decks) -1)
			new_card = winner_decks[j].cards[i].copy()
			self.cards.append(new_card)

	def debug_print(self):
		card_costs = []
		for c in self.cards:
			card_costs.append(c.cost)
		card_costs.sort()
		print(card_costs)

	def mutate(self):
		n = int(MUTATION_AMOUNT * len(self.cards))
		for i in range(0, n):
			j = random.randint(0, len(self.cards)-1)
			self.cards[i].randomize()


	def compete_once(self):
		comp_cards = list(self.cards)
		random.shuffle(comp_cards, random.random)
		comp_hand = []
		score = 0
		comp_mana_value = 1.0
		for i in range(0, HAND_START):
			comp_hand.append(comp_cards.pop())

		for comp_turn in range(1, TURN_LIMIT + 1):
			comp_mana = min(comp_turn, MANA_LIMIT)
			# draw cards
			if (len(comp_hand) < HAND_LIMIT):
				comp_hand.append(comp_cards.pop())
			else:
				comp_cards.pop()

			# use cards in had
			used_cards = find_hand(comp_hand, comp_mana)
			# xxx
			score += comp_mana_value * comb_mana(used_cards)
			comp_hand = [c for c in comp_hand if c not in used_cards]
			comp_mana_value *= MANA_VALUE_DECAY_RATE
		return score

	def compete_full(self):
		self.latest_score = 0
		for i in range(0, COMPETE_ROUNDS):
			self.latest_score += self.compete_once()
		return self.latest_score

class Race:
	decks = []
	deck_count = 0
	round_count = 0
	max_rounds = 0

	def init(self, count):
		self.deck_count = count
		self.round_count = 0
		for i in range(0, self.deck_count):
			new_deck = Deck()
			new_deck.init_cards()
			self.decks.append(new_deck)


	def update_decks(self):
		global avg_scores
		scores = []
		self.decks.sort(key=lambda d: d.latest_score, reverse=True)
		winner_decks = []
		for i in range(0, CHAMPIONS_TO_COPY):
			#self.decks[i].debug_print()
			#self.decks[i].cards.sort(key=lambda c: c.cost) # SORTED INHERIT OR UNSORTED
			winner_decks.append(self.decks[i])
			scores.append(float(self.decks[i].latest_score) / float(COMPETE_ROUNDS))
		avg = sum(scores) / float(len(scores))
		avg_scores.append(avg)

		generated_decks = []
		for i in range(0, self.deck_count - CHAMPIONS_TO_COPY):
			new_deck = Deck()
			new_deck.inherit(winner_decks)
			if (random.random() <= MUTATION_PROBABILITY):
				new_deck.mutate()
			generated_decks.append(new_deck)
			#self.decks[i].debug_print()
		self.decks = winner_decks + generated_decks
		self.round_count = self.round_count + 1

	def compete_one_round(self):
		for d in self.decks:
			d.compete_full()


	def update(self):
		#print("round start")
		self.compete_one_round()
		self.update_decks()

	def print_best(self):
		for i in range(0, CHAMPIONS_TO_COPY):
			self.decks[i].debug_print()

	def run(self, count, rounds):
		self.max_rounds = rounds
		self.init(count)
		while self.round_count < self.max_rounds:
			self.update()
		self.print_best()


def find_hand(hand, mana):
	sorted_hand = list(hand)
	sorted_hand.sort(key=lambda c: c.cost, reverse=True)
	#print sorted_hand
	return find_hand_recur(sorted_hand, mana, [])


def find_hand_recur(hand, mana, comb):

	# if mana is empty, return current comb
	if mana <= 0 or len(hand) <= 0:
		return comb
	# find available cards in hand
	hand_available = []
	for c in hand:
		if c.cost <= mana:
			hand_available.append(c)
	# compare with all possible comb with one more card included
	if len(hand_available) > 0:
		best_comb = []
		best_comb_mana = 0
		for c in hand_available:
			# get next recursive call
			next_hand = list(hand)
			next_hand.remove(c)
			next_comb = list(comb)
			next_comb.append(c)
			cur_comb = find_hand_recur(next_hand, mana - c.cost, next_comb)
			cur_comb_mana = comb_mana(cur_comb)

			# compare with best
			if cur_comb_mana > best_comb_mana or (cur_comb_mana == best_comb_mana and len(best_comb) > len(cur_comb)) :
				best_comb = cur_comb
				best_comb_mana = cur_comb_mana
		return best_comb
	# if no available card to add, return current comb
	else:
		return comb



def comb_mana(comb):
	result = 0
	for c in comb:
		result += c.cost
	return result


def get_costs(hand):
	card_costs = []
	for c in hand:
		card_costs.append(c.cost)
	card_costs.sort()
	return card_costs

#Main
r = Race()

parity = 0
if len(sys.argv) >= 3:
	TURN_LIMIT = int(sys.argv[1])
	MANA_VALUE_DECAY_RATE = float(sys.argv[2])

filename = "results(N="+str(TURN_LIMIT)+",r="+str(MANA_VALUE_DECAY_RATE)
if len(sys.argv) >= 4:
	parity = int(sys.argv[3])
	filename = filename + ",p=" + str(parity)
filename = filename + ").csv"

print("Simulation Begins.")
r.run(num_decks, num_rounds)

finish_time = time.time()
print("Simulation took", finish_time - start_time,"seconds to complete.")
print( "mean = ", statistics.mean(avg_scores))
print( "stdev = ", statistics.stdev(avg_scores))
print( "final s = ", avg_scores[len(avg_scores)-1])
print( "writing results....")


with open(filename, 'w') as csvfile:

	fieldnames = ['round', 'avg. scores']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(0, len(avg_scores)):
		writer.writerow({'round': i, 'avg. scores': avg_scores[i]})
print ("Results has been writen into '"+filename+"'. End.")
