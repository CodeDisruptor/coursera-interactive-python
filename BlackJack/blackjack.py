# Mini-project #6 - Blackjack
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ''
score = 0
deck = None
player_prompt = ''

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
	def __init__(self, suit, rank):
		if (suit in SUITS) and (rank in RANKS):
			self.suit = suit
			self.rank = rank
		else:
			self.suit = None
			self.rank = None
			print 'Invalid card: ', suit, rank

	def __str__(self):
		return self.suit + self.rank

	def get_suit(self):
		return self.suit

	def get_rank(self):
		return self.rank

	def draw(self, canvas, pos):
		card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
					CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
		canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
	def __init__(self):
		self.cards_in_hand = []

	def __str__(self):
		msg = ""
		for card in self.cards_in_hand:
			msg += card.get_suit() + card.get_rank() + " "
		return 'Hand contains %s' % msg

	def add_card(self, card):
		self.cards_in_hand.append(card)

	def get_value(self):
		value = 0
		aces = False
		for card in self.cards_in_hand:
			value += VALUES[card.get_rank()]
			if card.get_rank() == 'A':
				aces = True
		# If an ace was found count 10 to the value if the hand doesn't bust
		# otherwise just return the value
		if aces and value + 10 <= 21:
			return value + 10
		else:
			return value

	def draw(self, canvas, pos):
		for card in self.cards_in_hand:
			pos[0] += CARD_SIZE[0]
			card.draw(canvas, pos)

# define deck class
class Deck:
	def __init__(self):
		self.deck = []
		for s in SUITS:
			for r in RANKS:
				self.deck.append(Card(s, r))

	def shuffle(self):
		random.shuffle(self.deck)

	def deal_card(self):
		return self.deck.pop()

	def __str__(self):
		msg = ""
		for card in self.deck:
			msg += card.get_suit() + card.get_rank() + " "
		return 'Deck contains %s' % msg

# define event handlers for buttons
def deal():
	global player_prompt, score, outcome, in_play, deck, player_hand, dealer_hand
	player_hand, dealer_hand = Hand(), Hand()
	outcome, player_prompt = '', 'Hit or Stand?'

	deck = Deck()
	deck.shuffle()

	for i in range(2):
		player_hand.add_card(deck.deal_card())
		dealer_hand.add_card(deck.deal_card())

	# Check if player clicked deal during a game
	# and subtract by 1
	if in_play:
		score -= 1
	else:
		in_play = True

def hit():
	global score, player_prompt, outcome, in_play
	# if the hand is in play, hit the player
	if in_play:
		player_hand.add_card(deck.deal_card())

	if player_hand.get_value() > 21:
		if in_play:
			score -= 1
		in_play = False
		outcome = 'You\'ve busted!'
		player_prompt = 'Deal?'

def stand():
	global player_prompt, in_play, score, outcome
	player_prompt = 'Deal?'

	if in_play:
		in_play = False
		if player_hand.get_value() > 21:
			outcome = 'You\'ve busted!'
		else:
			while dealer_hand.get_value() < 17:
				dealer_hand.add_card(deck.deal_card())

			if dealer_hand.get_value() > 21:
				score += 1
				outcome = "The Dealer busts. You win!"
			elif dealer_hand.get_value() == player_hand.get_value():
				score -= 1
				outcome = "Game is tied. Dealer wins!"
			elif dealer_hand.get_value() > player_hand.get_value():
				score -= 1
				outcome = "The Dealer wins."
			else:
				score += 1
				outcome = "You win!"

# draw handler
def draw(canvas):
	# Game Title and score
	canvas.draw_text("Black Jack", (20, 50), 48, "White")
	canvas.draw_text("Score: %d" % score, (450, 50), 24, "White")

	# Dealer Cards
	canvas.draw_text("Dealer", (30, 125), 24, "White")
	dealer_hand.draw(canvas, [0, 150])
	if in_play:
		card_pos = (CARD_CENTER[0] + CARD_SIZE[0], 150 + CARD_CENTER[1])
		canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, card_pos, CARD_SIZE)

	# Player Cards
	canvas.draw_text("Player", (30, 450), 24, "White")
	player_hand.draw(canvas, [0, 475])

	# Game Messages
	canvas.draw_text("%s" % outcome, (60, 350), 36, "White")
	canvas.draw_text("%s" % player_prompt, (150, 450), 24, "White")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
