import random

# # Define deck and a card
# cards = [2, 3, 4, 5, 6, 7, 8, 9, "T", "J", "Q", "K", "A"]
# suits = ["S", "C", "D", "H"]
# deck = []
# round_number = 0  # Initialize round counter

# TEST BLACKJACKS
cards = ["T", "J", "Q", "K", "A"]
suits = ["S", "C", "D", "H"]
deck = []
round_number = 0  # Initialize round counter

# Create deck
for item in cards:
    for item2 in suits:
        deck.append(f'{item}{item2}')

# Add 6 Aces for each suit
for _ in range(6):
    for suit in suits:
        deck.append(f'A{suit}')

# Add 4 Fives for each suit
for _ in range(4):
    for suit in suits:
        deck.append(f'5{suit}')

# Shuffle the cards
random.shuffle(deck)

# Insert separator
separator = len(deck) // 2 + random.randint(-10, 10)
deck.insert(separator, 'SEPARATOR')

# Define card values
def hand_value(hand):
    value = 0
    ace = 0

    for card in hand:
        card_value = card[0]

        if card_value in ['T', 'J', 'Q', 'K']:
            value += 10
        elif card_value == 'A':
            value += 11
            ace += 1
        else:
            try:
                value += int(card_value)
            except ValueError:
                pass  # Handle other non-integer values

    while value > 21 and ace:
        value -= 10
        ace -= 1

    return value

# "hand" parameter and argument allows
# dealing to any specified hand
def deal(hand):
    card = deck.pop(0)
    if card == 'SEPARATOR':
        print("Reached the CUTTING CARD. Shoe change after this round!")
        card = deck.pop(0)
    hand.append(card)
    return card

def initial_deal():
    # Increment round number
    global round_number
    round_number += 1
    print(f"ROUND NUMBER - {round_number} !")

    player_hand = []
    dealer_hand = []

    # Deal initial cards for player and dealer (one hidden card)
    deal(player_hand)
    deal(dealer_hand)
    deal(player_hand)
    deal(dealer_hand)

    dealer_open_card = dealer_hand[0]  # Get the dealer's open card
    dealer_hidden_card = dealer_hand[1]

    dealer_open_value = hand_value(dealer_open_card)  # value of dealers open card
    dealer_hand = [dealer_open_card, dealer_hidden_card]

    player_total = hand_value(player_hand)
    dealer_total = hand_value(dealer_hand)

    print(f"Player's hand: {player_hand} of total value {player_total}")
    print(f"Dealer's hand: '?', {dealer_open_card} of value {dealer_open_value}")

    return player_hand, dealer_hand, dealer_open_card, dealer_hidden_card

def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21

def offer_insurance(dealer_open_card):
    if dealer_open_card[0] == 'A':
        print("Dealer has an ACE, offering INSURANCE BET!")
        has_insurance = input("Would you like to place INSURANCE BET? y/n ")
        return has_insurance
    return False  # if dealer's open card is not an Ace


def determine_outcome(player_hand, dealer_hand, has_insurance):
    if has_insurance == "y":
        if is_blackjack(dealer_hand):
            print("Dealer has a Blackjack. You win the insurance bet!")
        else:
            print("Dealer does not have a Blackjack. You lose the insurance bet.")

# Add the split function
def can_split(hand):
    return len(hand) == 2 and hand[0][0] == hand[1][0]

def split_hand(player_hand):
    if can_split(player_hand):
        # Create two new hands for the player
        new_hands = [player_hand[:1] + [deal(player_hand)], player_hand[:1] + [deal(player_hand)]]

        for i, new_hand in enumerate(new_hands):
            print(f"Split Hand {i + 1}: {new_hand}")
            while hand_value(new_hand) < 21:
                action = input(f"Choose an action for Split Hand {i + 1}: (H)IT, (S)TAND, (D)OUBLE: ").lower()
                if action == "h":
                    new_hand.append(deal(new_hand))
                    print(f"Split Hand {i + 1}: {new_hand}")
                elif action == "s":
                    break
                elif action == "d":
                    if len(new_hand) == 2 and hand_value(new_hand) != 21:
                        new_hand.append(deal(new_hand))
                        break

        return new_hands

# Welcome message
print("Hola Amigo! Welcome to the Blackjack Madness! May the fortune and the force of luck be with you!")

# Outer game loop for multiple rounds
while True:
    print() # space between each round number
    player_hand, dealer_hand, dealer_open_card, dealer_hidden_card = initial_deal()

    player_total = hand_value(player_hand)
    dealer_open_value = hand_value(dealer_open_card)  # Initialize dealer total with the open card
    dealer_total = hand_value(dealer_hand)

    # Offer insurance before player's actions
    has_insurance = offer_insurance(dealer_open_card)

    # # Debug: Print the dealer's open card
    # print("Dealer's open card:", dealer_open_card)
    #
    # # DEBUG: Offer insurance before player's actions
    # has_insurance = offer_insurance(dealer_open_card)
    # print("Has insurance:", has_insurance)

    # Inner game loop for a single round
    while True:

        if player_total == 21 and len(player_hand) == 2:
            print("Player have a BLACKJACK")
            print(f"Dealer's hand: {dealer_hidden_card}, {dealer_open_card} of value {dealer_total}")
            # No player input is needed here, so skip to dealer's actions directly

            # Implement outcome comparison and display results
            if dealer_total == 21 and len(dealer_hand) == 2:
                print("It's a PUSH!. Dealer has BLACKJACk as well.")
            else:
                print("CONFETTI & CONGRATULATIONS! YOU WON WITH A BLACKJACK!")
            break  # Exit the game loop as the player's actions are skipped
                    # if i don't exit it prints forever 2 prints above

        else:
            # Player's turn with input
            action = input("Choose an action: (H)IT, (S)TAND, (D)OUBLE, SPLI(T): ").lower()

            if action == "h":
                deal(player_hand)
                player_total = hand_value(player_hand)
                print(f"Player's hand: {player_hand} of total value {player_total}")

                if player_total > 21:
                    print("Player busts. Dealer wins")
                    print(f"Dealer's hand: {dealer_hidden_card}, {dealer_open_card} of total value {dealer_total}")

                    break # Exit the game loop for this round

                if len(player_hand) > 2 and player_total == 21:

                    # Implement dealer's actions here based on the revealed cards
                    while dealer_total < 17:
                        deal(dealer_hand)
                        dealer_total = hand_value(dealer_hand)
                        print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")

                        # Determine the outcome between player and dealer
                        if dealer_total > 21:
                            print("Dealer busts. Player wins")
                            print("PERFECT SCORE!")
                            print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                        elif player_total > dealer_total:
                            print("Player wins.")
                            print("PERFECT SCORE!")
                            print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                        elif player_total < dealer_total:
                            print("Dealer wins.")
                            print("PERFECT SCORE!")
                            print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                        else:
                            print("Player pushes.")
                            print("PERFECT SCORE FOR BOTH!")
                            print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")

                        break  # Exit the game loop for this round
            # Implement "STAND" logic
            elif action == "s":
                # Dealer's actions based on revealed cards
                while dealer_total < 17:
                    deal(dealer_hand)
                    dealer_total = hand_value(dealer_hand)
                    print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")

                # Determine the outcome between player and dealer
                if dealer_total > 21:
                    print("Dealer busts. Player wins")
                    print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                elif player_total > dealer_total:
                    print("Player wins.")
                    print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                elif player_total < dealer_total:
                    print("Dealer wins.")
                    print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                else:
                    print("Player pushes.")
                    print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                break  # Exit the game loop for this round

            elif action == "d":
                if len(player_hand) == 2 and player_total != 21:

                    # Deal one more card to the player and update the total
                    deal(player_hand)
                    player_total = hand_value(player_hand)
                    print(f"Player's hand: {player_hand} of total value {player_total}")


                    if player_total > 21:
                        print("Player busts. Dealer wins")
                        print(f"Dealer's hand: {dealer_hidden_card}, {dealer_open_card} of total value {dealer_total}")

                    # Implement dealer's actions here based on the revealed cards
                    while dealer_total < 17:
                        deal(dealer_hand)
                        dealer_total = hand_value(dealer_hand)
                        print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")

                    # Determine the outcome between player and dealer
                    if dealer_total > 21:
                        print("Dealer busts. Player wins with SUCCESSFULL DOUBLE DOWN!")
                        print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                    elif player_total > dealer_total:
                        print("Player wins with SUCCESSFULL DOUBLE DOWN!.")
                        print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                    elif player_total < dealer_total:
                        print("Dealer wins. Better next DOUBLE DOWN! ")
                        print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")
                    else:
                        print("Player pushes. Push with a DOUBLE DOWN.")
                        print(f"Dealer's hand: {', '.join(dealer_hand)} of total value {dealer_total}")

                    break  # Exit the game loop for this round

                else:
                    print("You can only DOUBLE on the initial hand with 2 cards.")
                # Check if the player's hand is eligible for splitting and player splits
            elif can_split(player_hand) and action == "t":
                if can_split(player_hand):
                    split_hands = split_hand(player_hand)
                    for i, split_hand in enumerate(split_hands):
                        print(f"Split Hand {i + 1}: {split_hand}")
                        while hand_value(split_hand) < 21:
                            action = input(
                                f"Choose an action for Split Hand {i + 1}: (H)IT, (S)TAND, (D)OUBLE:, SPLI(T) ").lower()
                            if action == "h":
                                split_hand.append(deal(split_hand))
                                print(f"Split Hand {i + 1}: {split_hand}")
                            elif action == "s":
                                break
                            elif action == "d":
                                if len(split_hand) == 2 and hand_value(split_hand) != 21:
                                    split_hand.append(deal(split_hand))
                            elif action == "t" and can_split(player_hand):
                                if can_split(player_hand):
                                    split_hands = split_hand(player_hand)
                                    for i, split_hand in enumerate(split_hands):
                                        print(f"Split Hand {i + 1}: {split_hand}")
                                        while hand_value(split_hand) < 21:
                                            action = input(f"Choose an action for Split Hand {i + 1}: (H)IT, (S)TAND, (D)OUBLE:, SPLI(T) ").lower()
                                            if action == "h":
                                                split_hand.append(deal(split_hand))
                                                print(f"Split Hand {i + 1}: {split_hand}")
                                            elif action == "s":
                                                break
                                            elif action == "d":
                                                if len(split_hand) == 2 and hand_value(split_hand) != 21:
                                                    split_hand.append(deal(split_hand))

                                    break
            else:
                print("Invalid action. Please choose a valid action.")

    # Determine the insurance outcome after all actions
    outcome = determine_outcome(player_hand, dealer_hand, has_insurance)
    if dealer_open_card[0] == 'A' and has_insurance:
        if outcome is not None:  # Only print the outcome if it's not None
            print(outcome)

    another_round = input("Would you like to have another round? (yes/no): ").lower()
    if another_round != "y":
        break  # Exit the outer loop if the player doesn't want another round
print()
print("Thank you for playing Blackjack Madness! Hope to see you again soon and take care!")