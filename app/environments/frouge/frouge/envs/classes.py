import random

BOARD_stage7_24 = "a023gMRPkeqos4cDHjTniu"
BOARD_stage7_56 = "0123gMRPkeqos4cDHjT09niu"
BOARD_stage8_24 = "a02h4oIcQDF3prsejLktgu"
BOARD_stage8_56 = "012h4oIcQDF3prsejLktg09u"
BOARD_stage9_24 = "A023p507okjq4e806hgirsTu"
BOARD_stage9_56 = "12093p507okjq4e806hgirsTu"
BOARD_stage11_24 = "a02805qgir0304sopthk706eJu"
BOARD_stage11_56 = "012805qgir90304sopthk706eJu"
BOARD_stage12_24 = "A024qMOKRFsd3plnhgeTju"
BOARD_stage12_56 = "124qMOKRFsd3pln09hgeTju"
BOARD_stage18_24 = "a02h4Lopc506r3gqJksteIU"
BOARD_stage18_56 = "012h409Lopc506r3gqJksteIU"
COL_BALLON_24 = "AnLHgceqtrMBoipjDFkSu"
CLASSICISSIMA_24 = "AebQRNHPcgikDFsLojmtu"
CORSO_PASEO_24 = "abcdefghijklmnopqrstu"
FIRENZE_24 = "abcgiDHqntmKQLrepJsfu"
MONTAGNE_24 = "abcfimetKGLHJsdopRQNU"
WEVELGEM_24 = "abcmgfteqonLPjkIDHrSu"


ALL_BOARDS = [
    BOARD_stage7_56,
    BOARD_stage8_56,
    BOARD_stage9_56,
    BOARD_stage11_56,
    BOARD_stage12_56,
    BOARD_stage18_56,
    # CORSO_PASEO_24
]

MAX_BOARD_SIZE = 120
MAX_START_SPACES = 15


# s = start
# n = normal
# d = descent
# c = climb
# f = finish
# p = paved
# su = supply unit
TILES = {
    "a" : ["s"] * 5 + ["n"],
    "A" : ["s"] * 4 + ["n"]*2,
    "b" : ["n"] * 6,
    "B" : ["d"] * 4 + ["n"]*2,
    "c" : ["n"] * 6,
    "C" : ["n"] * 3 + ["c"]*3,
    "d" : ["n"] * 6,
    "D" : ["c"] * 5 + ["d"],
    "e" : ["n"] * 2,
    "E" : ["c"] * 2,
    "f" : ["n"] * 6,
    "F" : ["d"] * 3 + ["n"]*3,
    "g" : ["n"] * 2,
    "G" : ["c"] * 2,
    "h" : ["n"] * 2,
    "H" : ["d"] * 2,
    "i" : ["n"] * 2,
    "I" : ["n"] * 2,
    "j" : ["n"] * 2,
    "J" : ["n"] * 2,
    "k" : ["n"] * 2,
    "K" : ["c"] * 2,
    "l" : ["n"] * 6,
    "L" : ["c"] * 3 + ["d"]*3,
    "m" : ["n"] * 6,
    "M" : ["n"] * 2 + ["c"]*4,
    "n" : ["n"] * 6,
    "N" : ["c"] * 6,
    "o" : ["n"] * 2,
    "O" : ["c"] * 2,
    "p" : ["n"] * 2,
    "P" : ["d"] * 2,
    "q" : ["n"] * 2,
    "Q" : ["c"] * 2,
    "r" : ["n"] * 2,
    "R" : ["c"] * 2,
    "s" : ["n"] * 2,
    "S" : ["n"] * 2,
    "t" : ["n"] * 2,
    "T" : ["n"] * 2,
    "u" : ["n"] + ["f"] * 5,
    "U" : ["n"] * 2 + ["f"]*4,
    "1" : ["s3"] * 4 + ["n3"] * 2,
    "11" : ["s3"] * 5 + ["n3"],
    "2" : ["n3"] * 5 + ["n"], #FIXME
    "22" : ["n3"] * 6,
    "3" : ["su3"] * 5 + ["n"], #FIXME
    "33" : ["n"] * 2 + ["p1"] * 2 + ["p2"] + ["p1"],
    "4" : ["su3"] * 5 + ["n"], 
    "44" : ["p1"] + ["p2"] + ["p1"] * 2 + ["n"],
    "5" : ["p1"] + ["p2"] + ["p1"] + ["p2"] + ["p1"] * 2,
    "55" : ["p1"] * 2 + ["n"] * 4,
    "6" : ["p1"] * 2 + ["p2"] + ["p1"] * 3,
    "66" : ["p1"] * 3 + ["p2"] + ["p1"] + ["n"],
    "7" : ["n"] * 2 + ["p1"] * 2 + ["p2"] + ["p1"],
    "77" : ["p1"] + ["p2"] + ["p1"] + ["n"] * 3,
    "8" : ["n"] * 3 + ["p1"] + ["p2"] + ["p1"],
    "88" : ["p1"] * 2 + ["p2"] + ["p1"] * 2 + ["n"],
    "9" : ["su3"] * 2 + ["n"],
    "99" : ["n3"] * 2 + ["n"],
}

#cell codes
MAX_CODE = 7
#empty cell
CV = [ 0 ] * MAX_CODE
#normal cell
CN = list(CV)
CN[0] = 1
#start cell
CS = list(CV)
CS[1] = 1
#descent cell
CD = list(CV)
CD[2] = 1
#climb cell
CC = list(CV)
CC[3] = 1
#final cell
CF = list(CV)
CF[4] = 1
#paved cell
CP = list(CV)
CP[5] = 1
#supplies cell
CSU = list(CV)
CSU[6] = 1

CODES = {
    "n2" : [ list(CN), list(CN), list(CV) ],
    "n3" : [ list(CN), list(CN), list(CN) ],
    "s2" : [ list(CS), list(CS), list(CV) ],
    "s3" : [ list(CS), list(CS), list(CS) ],
    "d2" : [ list(CD), list(CD), list(CV) ],
    "c2" : [ list(CC), list(CC), list(CV) ],
    "f2" : [ list(CF), list(CF), list(CV) ],
    "f3" : [ list(CF), list(CF), list(CF) ],
    "su2" : [ list(CSU), list(CSU), list(CV) ],
    "su3" : [ list(CSU), list(CSU), list(CSU) ],
    "p2" : [ list(CP), list(CP), list(CV) ],
    "p1" : [ list(CP), list(CV), list(CV) ],
}

class Player():
    def __init__(self, n, name=None):
        self.n = n
        if name:
            self.name = name
        else:
            self.name = str(n)
        self.s_deck = Deck(SPRINTER_CARDS)
        self.r_deck = Deck(ROULEUR_CARDS)
        self.s_discard = Deck()
        self.r_discard = Deck()
        self.s_played = Deck()
        self.r_played = Deck()
        self.r_hand = Deck()
        self.s_hand = Deck()
        self.s_position = Position()
        self.r_position = Position()
        self.r_chosen = None
        self.r_chosen = None
        self.hand_order = ['r', 's']
    
    def c_pos(self,cyclist):
        if cyclist == "r":
            return self.r_position
        else:
            return self.s_position

    def c_hand(self,cyclist):
        if cyclist == "r":
            return self.r_hand
        else:
            return self.s_hand

    def c_chosen_card(self,cyclist):
        if cyclist == "r":
            return self.r_chosen
        else:
            return self.s_chosen

    def c_set_chosen_card(self,cyclist,card):
        if cyclist == "r":
            self.r_chosen = card
        else:
            self.s_chosen = card
    
    def c_played(self,cyclist):
        if cyclist == "r":
            return self.r_played
        else:
            return self.s_played

    def c_discard(self,cyclist):
        if cyclist == "r":
            return self.r_discard
        else:
            return self.s_discard

    def map_to_board(self,board=None):
        if board:
            a = board
        else:
            a = Board()
        a.array[self.r_position.col][self.r_position.row][0] = str(self.n) + "r"
        a.array[self.s_position.col][self.s_position.row][0] = str(self.n) + "s"
        return a


class Position():
    def __init__(self,col=-1,row=-1):
        self._col = col
        self._row = row
    
    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self,value):
        self._col = value

    @row.setter
    def row(self,value):
        self._row = value
    
    def map_to_board(self,board=None,value=1):
        if board:
            a = board
        else:
            a = Board()
        a.array[self._col][self._row][0] = value
        return a
       
class Deck():
    def __init__(self, cards = list()):
        self.cards = list(cards)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n):
        drawn = []
        for x in range(n):
            try:
                drawn.append(self.cards.pop())
            except:
                pass
        return drawn
    
    def add(self, cards):
        for card in cards:
            self.cards.append(card)
                
    def size(self):
        return len(self.cards)

    def array(self):
        array = [ 0 ] * len(ALL_CARDS)
        for card in self.cards:
            array[ALL_CARDS.index(card)] += 0.1
        return array

class Card():
    def __init__(self, name, value):
        self._name = name
        self._value = value
        
    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    def __eq__(self,other):
        if isinstance(other,Card):
            return (other.value == self._value) and (other.name == self._name)
        return False

class Board():
    def __init__(self,track=""):
        self._array = list()
        self._players = list()
        alt_tile = False
        for tile in track:
            if tile == "0":
                alt_tile = True
                continue
            if alt_tile:
                tile += tile
                alt_tile = False
            tiles = TILES[tile]
            for cell in tiles:
                self._array.append(self.code(cell))
        #padding
        for i in range(MAX_BOARD_SIZE - len(self._array)):
            self._array.append([ list(CF), list(CF), list(CF) ])
    
    def add_player(self,player):
        self._players.append(player)

    @property
    def players(self):
        return self._players
    
    def code(self,cell):
        if len(cell) == 1:
            cell += "2"
        return list(CODES[cell])
    
    def first_start_col(self):
        for i, col in enumerate(self.array):
            if col[0] != CS:
                return i-1
    
    @property
    def array(self):
        return self._array
    
    @array.setter
    def array(self,value):
        self._array = value

    def get_cell(self,col,row):
        try:
            cell = self._array[col][row]
        except:
            cell = None
        return cell

    def get_cell_display(self,col,row):
        for p in self._players:
            if p.r_position.col == col and p.r_position.row == row:
                return str(p.n) + "r"
            if p.s_position.col == col and p.s_position.row == row:
                return str(p.n) + "s"
        return ""

    def set_cycl_to_pos(self,player_id,c_type,col):
        row = 0
        while True:
            if self.is_empty(col,row):
                break
            else:
                col, row = self.previous_cell(col,row)

        self.set_cycl_to_square(player_id,c_type, col, row)


    def set_cycl_to_square(self,player_id,c_type, col, row):
        self._players[player_id-1].c_pos(c_type).col = col
        self._players[player_id-1].c_pos(c_type).row = row

    #empty of player
    def is_empty(self,col,row):
        for p in self._players:
            if p.r_position.col == col and p.r_position.row == row:
                return False
            if p.s_position.col == col and p.s_position.row == row:
                return False
        return True
    
    def move(self,player_id,c_type,n,aspiration=False):
        player = self._players[player_id-1]
        start_cell = self.get_cell(player.c_pos(c_type).col,player.c_pos(c_type).row)
        if not aspiration:
            if start_cell == CD:
                n = max(n,5)
            if start_cell == CSU:
                n = max(n,5)
            if start_cell == CC:
                n = min(n,5)
            if self.get_cell(player.c_pos(c_type).col+n,0) == CC:
                if n > 5:
                    n = 5
        self.set_cycl_to_pos(player_id, c_type, player.c_pos(c_type).col + n)

    def previous_cell(self,col,row):
        if row == 2:
            return (col-1,0)
        if self.array[col][row+1] == CV:
            return (col-1,0)
        return (col,row+1)
        
ALL_CARDS = [
        Card("Sprinter 2",2),
        Card("Sprinter 3",3),
        Card("Sprinter 4",4),
        Card("Sprinter 5",5),
        Card("Sprinter 9",9),
        Card("Sprinter penalty",2),
        Card("Rouleur 3",3),
        Card("Rouleur 4",4),
        Card("Rouleur 5",5),
        Card("Rouleur 6",6),
        Card("Rouleur 7",7),
        Card("Rouleur penalty",2),
        ]

SPRINTER_CARDS = \
    [ ALL_CARDS[0] ] * 3 + \
    [ ALL_CARDS[1] ] * 3 + \
    [ ALL_CARDS[2] ] * 3 + \
    [ ALL_CARDS[3] ] * 3 + \
    [ ALL_CARDS[4] ] * 3

PENALTY_SPRINTER_CARD = ALL_CARDS[5]
PENALTY_ROULEUR_CARD = ALL_CARDS[11]

ROULEUR_CARDS = \
    [ ALL_CARDS[6] ] * 3 + \
    [ ALL_CARDS[7] ] * 3 + \
    [ ALL_CARDS[8] ] * 3 + \
    [ ALL_CARDS[9] ] * 3 + \
    [ ALL_CARDS[10] ] * 3
    
 
