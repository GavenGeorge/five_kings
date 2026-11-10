import sys
import arcade
from models.deck import Deck, Hand

WIDTH, HEIGHT = 800, 600

class App(arcade.Window):
    def __init__(self):
        super().__init__(1000, 600, "Five Crowns")
        arcade.set_background_color(arcade.color.DARK_GREEN)

        self.deck = Deck()
        self.deck.build()
        self.deck.shuffle()


        def deal_to(hand, y, face_up=True):
            card = self.deck.deal()
            if face_up:
                card.flip()
            card.position = (150 + len(hand) * 110, y)  # cards are 99 px wide at scale 3
            hand.append(card)

        self.user_hand = Hand()
        self.dealer_hand = Hand()

        deal_to(self.user_hand, y=150, face_up=True)
        deal_to(self.dealer_hand, y=450, face_up=False)
        deal_to(self.user_hand, y=150, face_up=True)
        deal_to(self.dealer_hand, y=450, face_up=False)



    def on_draw(self):
        self.clear()
        self.dealer_hand.draw(pixelated=True)   # keeps the 8-bit pixels sharp when scaled
        self.user_hand.draw(pixelated=True)

    def on_update(self, delta_time):
        self.dealer_hand.update()
        self.user_hand.update()

    def on_mouse_press(self, x, y, button, modifiers):
        for card in arcade.get_sprites_at_point((x, y), self.deck.cards):
            card.flip()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
            sys.exit()

    def on_key_release(self, key, modifiers):
        pass


if __name__ == "__main__":
    app = App()
    arcade.run()