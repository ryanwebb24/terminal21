'''
Project: Twenty One Game:
Course: CS-1410 X02
Name: Ryan Webb
Due Date: 1/20/23

Description:
This is a game of 21 first the main function starts the game then runs the game class. In the game class it first deals the hand and then runs the game if you hit then it will give you another card and ask you if you
if you want to hit again or stand if you choose hit again then it will give you another card if you stand the dealer wiull complete his turn. if your card total is over 21 you bust if the dealers busts you win it the
dealer has a higher score without busting he wins. if you have a higher score without busting you win. if you tie then the game starts over. At the end of every game you are asked if you want to play again if y then
you start over is n it closes the program.
'''

import os
import random

class Card:
   """Card class with methods __init__, and __str__"""
   def __init__(self, suit, value, numeric_value, suit_value):
      """takes the suit, value, numeric_value, suit_value of a card as input"""
      self.suit = suit
      self.value = value
      self.numeric_value = numeric_value
      self.suit_value = suit_value
      self.face_up = True
   def __str__(self):
      """This converts the card to a ascii image if the card is face down it makes it question marks"""
      if not self.face_up:
         new_card = ' ----------------\n|  ?             |\n|                |\n|                |\n|                |\n|                |\n|                |\n|                |\n|                |\n|                |\n|                |\n|                |\n|                |\n|             ?  |\n---------------- '
      else:
         card = ' ----------------\n| a             |\n|                |\n|                |\n|                |\n|                |\n|                |\n|        b       |\n|                |\n|                |\n|                |\n|                |\n|                |\n|            c  |\n---------------- '
         if len(self.value) == 2:
            new_card = card.replace('a',self.value).replace('b',self.suit_value).replace('c',self.value)
         else:
            new_card = card.replace('a',f" {self.value}").replace('b',self.suit_value).replace('c',f" {self.value}")
      return(new_card)

class Deck:
   suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
   suits_values = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs": "\u2667", "Diamonds": "\u2662"}
   cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
   numeric_values = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
   def __init__(self):
      """initializes the deck and fills it"""
      self.card = []
      for suit in self.suits:
         for value in self.cards:
            self.card.append(Card(suit, value, self.numeric_values[value], self.suits_values[suit]))
   def shuffle(self):
      """shuffles the cards"""
      return random.shuffle(self.card)

   def deal(self):
      """deals a card removing one from the deck"""
      return self.card.pop()

class Hand:
   """Hand class with methods of __init__, __str__, add, and ace_changes"""
   def __init__(self):
      """initializes cards, score, busted, ace_counter, player, and hidden_card"""
      self.cards = []
      self.score = 0
      self.busted = False
      self.ace_counter = 0
      self.player = True
      self.hidden_card = False

   def __str__(self):
      '''This prints the cards horizontally'''
      # players hand
      if self.player:
         card_strings = [str(card).split("\n") for card in self.cards]
         top_line = '      '.join([lines[0] for lines in card_strings])
         bottom_line = '      '.join([lines[-1] for lines in card_strings])
         card_strings = [lines[1:-1] for lines in card_strings]
         horizontal_cards = ["     ".join(lines) for lines in zip(*card_strings)]
         return "Players Hand:\n" + top_line + '\n' + "\n".join(horizontal_cards) + '\n ' + bottom_line + '\n' + f"Players Score = {self.score}"
      # dealers hidden hand
      elif self.hidden_card:
         card_strings = [str(card).split("\n") for card in self.cards]
         top_line = '      '.join([lines[0] for lines in card_strings])
         bottom_line = '      '.join([lines[-1] for lines in card_strings])
         card_strings = [lines[1:-1] for lines in card_strings]
         horizontal_cards = ["     ".join(lines) for lines in zip(*card_strings)]
         return "Dealers Hand:\n" + top_line + '\n' + "\n".join(horizontal_cards) + '\n ' + bottom_line + '\n' + f"Dealers Score = {self.score - self.cards[1].numeric_value}"
      # dealers unhidden hand
      else:
         card_strings = [str(card).split("\n") for card in self.cards]
         top_line = '      '.join([lines[0] for lines in card_strings])
         bottom_line = '      '.join([lines[-1] for lines in card_strings])
         card_strings = [lines[1:-1] for lines in card_strings]
         horizontal_cards = ["     ".join(lines) for lines in zip(*card_strings)]
         return "Dealers Hand:\n" + top_line + '\n' + "\n".join(horizontal_cards) + '\n ' + bottom_line + '\n' + f"Dealers Score = {self.score}"
   def add(self, card):
      """add takes a card object as input
         it adds the card to the hand and then adds the score if the score is greater than 21 then the hand busts by changing busted to true unless there is an ace"""
      if card.value == "A":
         self.ace_counter += 1
      self.cards.append(card)
      self.score += card.numeric_value
      if self.score > 21:
         if self.ace_counter >= 1:
            self.ace_change()
            self.ace_counter -= 1
         else:
            self.busted = True

   def ace_change(self):
      """runs only when the player has an ace and changes it to a 1"""
      self.score -= 10

class Dealer:
   """dealer class with methods of __init__, reveal, hit, and give_hidden_card"""
   def __init__(self):
      """initializes the dealers hand and sets the hand.player to false signifying that it is the dealer"""
      self.hand = Hand()
      self.hand.player = False
   def reveal(self):
      """reveals the dealers face down card by changing the seconds cards face_up value to true"""
      self.hand.cards[1].face_up = True

   def hit(self, card):
      """takes a Card object as input
         adds the card to the dealers hand"""
      self.hand.add(card)

   def give_hidden_card(self, card):
      """takes a Card object as input
         adds a card to the dealers hand making sure that the card is face down"""
      self.hand.add(card)
      card.face_up = False

class Player:
   """player class with methods of __init__, and hit"""
   def __init__(self):
      """initializes the players hand with the Hand class"""
      self.hand = Hand()

   def hit(self, card):
      """takes a Card object as input
         adds the card to the players hand"""
      self.hand.add(card)
class Game:
   """the main game of 21 with methods of __init__, start, run, and replay"""
   def __init__(self):
      """initializes the deck player and dealer"""
      self.deck = Deck()
      self.player = Player()
      self.dealer = Dealer()

   def start(self):
      """begins the game by shuffling and giving 2 cards to both the dealer and player"""
      #shuffles the cards to start the game
      self.deck.shuffle()
      #gives cards to the player and dealer
      for i in range(2):
         self.player.hit(self.deck.deal())
      self.dealer.hit(self.deck.deal())
      self.dealer.give_hidden_card(self.deck.deal())
      #print the hands of the dealer and the player
      self.dealer.hand.hidden_card = True
      print(self.player.hand)
      print(self.dealer.hand)

   def run(self):
      """runs main game strating with the players turn then once the player is done it moves on to the dealer then determines the winner"""
      while True:
      # player turn
         while True:
            choice = input("Do you want to hit or stand? ")
            clear()
            if choice == "hit":
               self.player.hit(self.deck.deal())
               print(self.player.hand)
               print(self.dealer.hand)
            elif choice == "stand":
               self.dealer.hand.hidden_card = False
               break
            else:
               print(self.player.hand)
               print(self.dealer.hand)
            if self.player.hand.busted:
               self.dealer.hand.hidden_card = False
               self.dealer.reveal()
               print(self.player.hand)
               print(self.dealer.hand)
               print("Player busts, dealer wins :(")
               choice = input("Do you want to play again? (y/n)")
               if choice == 'y':
                  self.replay()
               else:
                  quit()
         # dealer turn
         self.dealer.reveal()
         while self.dealer.hand.score < 17:
            self.dealer.hit(self.deck.deal())
         # dealer bust check
         if self.dealer.hand.busted:
            clear()
            self.dealer.hand.hidden_card = False
            print(self.player.hand)
            print(self.dealer.hand)
            print("Dealer busts, player wins!")
            choice = input("Do you want to play again? (y/n)")
            if choice == 'y':
               self.replay()
            else:
               quit()
         # determine winner
         if self.player.hand.score > self.dealer.hand.score:
            clear()
            self.dealer.hand.hidden_card = False
            print(self.player.hand)
            print(self.dealer.hand)
            print("Player wins!")
            choice = input("Do you want to play again? (y/n)")
            if choice == 'y':
               self.replay()
            else:
               quit()
         elif self.player.hand.score < self.dealer.hand.score:
            clear()
            self.dealer.hand.hidden_card = False
            print(self.player.hand)
            print(self.dealer.hand)
            print("Dealer wins :(")
            choice = input("Do you want to play again? (y/n)")
            if choice == 'y':
               self.replay()
            else:
               quit()
         else:
            clear
            self.dealer.hand.hidden_card = False
            print(self.player.hand)
            print(self.dealer.hand)
            print("It's a tie.")
            choice = input("Do you want to play again? (y/n)")
            if choice == 'y':
               self.replay()
            else:
               quit()

   def replay(self):
      """this reaplay the game starting from the beginning"""
      self.__init__()
      self.start()
      self.run()


def clear():
   """Clear the console."""
   os.system('cls' if os.name == 'nt' else 'clear')


def main():
   '''sets the class Game to game and then starts it and runs it'''
   game = Game()
   game.start()
   game.run()

if __name__ == '__main__':
   main()