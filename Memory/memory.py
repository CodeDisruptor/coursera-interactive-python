# implementation of card game - Memory
import simplegui
import random

# helper function to initialize globals
def new_game():
	global state, turn_counter, deck, exposed, turned_cards
	state, turn_counter = 0, 0
	deck = range(8)
	deck.extend(range(8))
	random.shuffle(deck)
	exposed = [False for i in range(16)]
	turned_cards = []

# define event handlers
def mouseclick(pos):
	global state, turn_counter, exposed, turned_cards
	card_number = pos[0] // 50  # get Card number from 0-15
	if state == 0:  # No cards exposed
		state, exposed[card_number] = 1, True
		turn_counter += 1
		turned_cards.append(card_number)  # Add card to list of turned cards.
	elif state == 1:  # One card exposed
		exposed[card_number] = True
		# Check if this card is not on turned list and add if not.
		# Change state if card was added to turned list
		if not (card_number in turned_cards):
			state = 2
			turned_cards.append(card_number)
	else:  # Two cards exposed then reset to one
		# Check if this card is not on turned list and add if not else do nothing.
		# Set exposed to true if card is not yet exposed and add to turned List
		if not (card_number in turned_cards):
			# Check if exposed cards match and cover up if they don't
			# Always check the last two elements in the list since they are recently added
			if deck[turned_cards[-1]] != deck[turned_cards[-2]]:
				exposed[turned_cards[-1]], exposed[turned_cards[-2]] = False, False
				turned_cards.pop()
				turned_cards.pop()
			state, exposed[card_number] = 1, True
			turn_counter += 1
			turned_cards.append(card_number)

# cards are logically 50x100 pixels in size
def draw(canvas):
	# Update clicks
	label.set_text('Turn = %d' % turn_counter)
	# Draw cards from deck
	for i in range(16):
		if exposed[i]:
			# Position text to center on card slot
			canvas.draw_text(str(deck[i]), [10 + (50 * i), 65], 50, "White")
		else:
			card_pos = [[0 + (50 * i), 0], [50 + (50 * i), 0], [50 + (50 * i), 100], [0 + (50 * i), 100]]
			canvas.draw_polygon(card_pos, 1, 'Red', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
