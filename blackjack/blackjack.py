import random
random.seed(999)

class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.number = num
    
    def display(self):
        return f"{self.number}{self.suit}"

class Deck:
    def __init__(self):
        self.card_ls = []

        #create deck
        suits = "♠️ ♣️ ♥️ ♦️".split(" ")
        nums = "2 3 4 5 6 7 8 9 10 J Q K A".split(" ")

        for i in suits:
            for j in nums:
                self.card_ls.append(Card(suit=i, num=j))

        random.shuffle(self.card_ls)

    def draw_card(self):
        return self.card_ls.pop(0)
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.role = "P"

    def draw_card(self, card:Card):
        self.hand.append(card)

    def sum_score(self) -> int:
        number2score = {
            "A":11, 
            "2":2, 
            "3":3, 
            "4":4, 
            "5":5, 
            "6":6, 
            "7":7, 
            "8":8, 
            "9":9, 
            "10":10, 
            "J":10, 
            "Q":10, 
            "K":10
        }

        score = 0
        n_ace = 0 

        for c in self.hand:
            if(c.number == "A"):
                n_ace += 1
            else:
                score += number2score[c.number]

        # calculate value of ace
        for _ in range(n_ace):
            if(n_ace == 1 ):
                if(score<=10):
                    score += 11
                else:
                    score += 1
            else:
                if(score<=10):
                    score += 11
                else:
                    score += 1
        
        return score
    
    def is_blackjack(self):
        score = self.sum_score(is_hidden=False)
        if(score == 21):
            return True
        return False
    
    def is_busted(self):
        score = self.sum_score()
        if(score > 21):
            return True
        return False
    
    def display(self):
        txt = f"{self.name}'s cards : "
        for c in self.hand:
            txt += c.display()+" "
        
        txt += "\nscore : "+str(self.sum_score())

        return txt
    
    
class Dealer:
    def __init__(self):
        self.hand = []
        self.role = "Dealer"

    def draw_card(self, card:Card):
        self.hand.append(card)

    def sum_score(self, is_hidden) -> int:
        number2score = {
            "A":11, 
            "2":2, 
            "3":3, 
            "4":4, 
            "5":5, 
            "6":6, 
            "7":7, 
            "8":8, 
            "9":9, 
            "10":10, 
            "J":10, 
            "Q":10, 
            "K":10
        }

        score = 0
        n_ace = 0 
        ace_value_ls = []

        for c in self.hand:
            if(c.number == "A"):
                n_ace += 1
            else:
                score += number2score[c.number]

        # calculate value of ace
        add = 0
        for _ in range(n_ace):
            if(n_ace == 1 ):
                if(score<=10):
                    add += 11
                else:
                    add += 1
            else:
                if(score<=10):
                    add += 11
                else:
                    add += 1
            #print("add:", add)
            score += add
            ace_value_ls.append(add)
            add = 0

        if(is_hidden):
            first_c = self.hand[0]
            if(first_c.number == "A"):
                score -= ace_value_ls[0]
            else:
                score -= number2score[first_c.number]
        
        return score
    
    def is_blackjack(self):
        score = self.sum_score(is_hidden=False)
        if(score == 21):
            return True
        return False
    
    def is_busted(self):
        score = self.sum_score(is_hidden=False)
        if(score > 21):
            return True
        return False
    
    def display(self, is_hidden=True):
        txt = "Dealer's cards : "
        for idx in range(len(self.hand)):
            if(idx == 0 and is_hidden):
                txt += "XX "
            else:
                txt += self.hand[idx].display()+" "
        
        txt += "\nscore : "+str(self.sum_score(is_hidden=is_hidden))

        return txt

    def make_decision(self, player_score_ls) -> bool:

        if(self.is_blackjack()):
            return False
        if(self.is_busted()):
            return False
        
        # need to draw
        score = self.sum_score(is_hidden=False)
        if(score<17):
            return True
        
        for s in player_score_ls:
            if(score<s):
                return True
            
        return False
    
def main(n_player:int):
    # init deck
    deck = Deck()

    # init player
    player_ls = []
    for idx in range(n_player):
        name_input = input(f"Input player {idx+1} name : ")
        player = Player(name=name_input)
        player_ls.append(player)

    # init dealer
    dealer = Dealer()

    # start give cards in order
    for _ in range(2):
        for p in player_ls:
            p.draw_card(deck.draw_card())
        dealer.draw_card(deck.draw_card())

    # player's turn
    for idxx in range(n_player):
        print()
        print(f"{player_ls[idxx].name}'s turn :")
        print()

        while(True):
            for pp in player_ls:
                print(pp.display())
                if(pp.sum_score() > 21):
                    print("ว้าย ตายแล้ว")
                if(pp.sum_score() == 21):
                    print("เก่งมาก เอาไป 1 นิ้วโป้ง")
                print()
                
            print(dealer.display())
            print()
            print("==========================")
            print()

            if(player_ls[idxx].sum_score() >= 21):
                print("break")
                break
            choice = input(f"{player_ls[idxx].name} selcet H (hit) or S (stand) : ")
            if(choice in ["S", "s"]):
                break
            elif(choice in ["H", "h"]):
                player_ls[idxx].draw_card(card = deck.draw_card())

            else:
                print("พิมพ์ให้ถูกไอควาย 🫵🏻")
    
    # dealer turn
    player_score = [pivot.sum_score() for pivot in player_ls]
    while(dealer.make_decision(player_score_ls=player_score)):
        dealer.draw_card(deck.draw_card())

    for pp in player_ls:
        print(pp.display())
        if(pp.sum_score() > 21):
            print("ว้าย ตายแล้ว")
        if(pp.sum_score() == 21):
            print("เก่งมาก เอาไป 1 นิ้วโป้ง")
        print()
                
    print(dealer.display(is_hidden=False))
    print()
    print("==========================")
    print()
    
    # find winner
    for p in player_ls:
        if(p.sum_score == 21 and dealer.sum_score(is_hidden=False)==21):
            print(f"{p.name} Draw!")
        elif(p.sum_score == 21 and not dealer.sum_score(is_hidden=False)==21):
            print(f"{p.name} Win!")
        elif(p.sum_score() < 21 and dealer.sum_score(is_hidden=False) < p.sum_score()):
            print(f"{p.name} Win!")
        elif(p.sum_score() <= 21 and dealer.is_busted()):
            print(f"{p.name} Win!")
        elif(p.sum_score() == dealer.sum_score(is_hidden=False)):
            print(f"{p.name} Draw!")
        elif(p.is_busted() and dealer.is_busted()):
            print(f"{p.name} Draw!")
        else:
            print(f"{p.name} Loss!")



if(__name__ == "__main__"):
    n_player = int(input("Input number of players :"))
    main(n_player=n_player)