import os
import random

import arcade
from PIL import Image

SHEET_PATH = f"{os.path.dirname(__file__)}/../assets/8BitDeckAssets.png"

# ---- set these from your measurements ----
CARD_W, CARD_H = 33, 45   # one card
GAP_X, GAP_Y = 2, 2       # 2 px between cards
OFFSET_X, OFFSET_Y = 1, 1 # 1 px padding around the sheet edge
# ------------------------------------------

SUITS = ["hearts", "clubs", "diamonds", "spades"]                     # row order
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def load_card_textures(path: str) -> dict:
    sheet = Image.open(path).convert("RGBA")

    def cell(col: int, row: int) -> arcade.Texture:
        x = OFFSET_X + col * (CARD_W + GAP_X)
        y = OFFSET_Y + row * (CARD_H + GAP_Y)
        img = sheet.crop((x, y, x + CARD_W, y + CARD_H))
        return arcade.Texture(img, hash=f"card_{col}_{row}")

    textures = {}
    for row, suit in enumerate(SUITS):
        for i, rank in enumerate(RANKS):
            textures[(rank, suit)] = cell(i + 1, row)   # column 0 is backs/jokers

    textures["back_red"] = cell(0, 0)
    textures["back_blue"] = cell(0, 1)
    textures["joker_red"] = cell(0, 2)
    textures["joker_black"] = cell(0, 3)
    return textures

class Hand(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.ace_count = 0

    def add_card(self, card: Card):
        self.append(card)
        if card.value == 11: # check if card is an ace
            self.ace_count += 1

    def total(self):
        if len(self) == 0:
            return 0
        elif len(self) == 1:
            return self[0]
        elif len(self) == 2:
            return self[0] + self[1]
        else:
            total = 0
            for card in self:
                total += card

            while total > 21 & self.ace_count > 0:
                total -= 10
                self.ace_count -= 1

            return total




class Card(arcade.Sprite):
    def __init__(self, rank, suit, textures, scale=3):
        self.rank, self.suit = rank, suit
        if rank in ("J", "Q", "K"):
            self.value = 10
        elif rank == "A":
            self.value = 11
        else:
            self.value = rank
        self.face_tex = textures[(rank, suit)]
        self.back_tex = textures["back_red"]
        self.face_up = False
        super().__init__(self.back_tex, scale=scale)

    def flip(self):
        self.face_up = not self.face_up
        self.texture = self.face_tex if self.face_up else self.back_tex

class Deck:
    def __init__(self):
        self.cards: list[Card] = []
        self.textures = load_card_textures(SHEET_PATH)

    def build(self):
        for rank in RANKS:
            for suit in SUITS:
                card = Card(rank, suit, self.textures)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self) -> Card:
        return self.cards.pop()


