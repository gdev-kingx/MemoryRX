""" MemoryPyne (The Game) """
# Modules
import reflex as rx
import random
import asyncio

class State(rx.State):
    # to set the opacity, we need to create states for all tiles/emojis
    # get opacity states
    emoji_list: list[list] = [[i, "0%"] for i in range(36)]
    
    count: int = 0
    track: list = []
    score: int = 0
    result: str

    def reveal_emoji(self, emoji, emoji_type):
        index = emoji[0]
        self.emoji_list = [
            [i, "100%"] if i == index else [i, opacity]
            for i, opacity in self.emoji_list
        ]

        self.count += 1
        self.track.append((emoji_type, emoji))
        
    async def check_emoji(self):
        if self.count == 2:
            if self.track[0][0] == self.track[1][0]:
                self.score += 1
                if self.score == 8:
                    self.result = 'Congrats!! You WON!'
                pass
            else:
                indicies = [e[1][0] for e in self.track]
                self.emoji_list = [
                    [i, "0%"] if i in indicies else [i, opacity]
                    for i, opacity in self.emoji_list
                ]
            self.count = 0
            self.track = []
        
        await asyncio.sleep(2) 

class MemoryRX:
    def __init__(self):
        self.stage: int = 2
        self.emojis: list = [
            "🔥", "🍎", "😡", "💀", 
            "🤘", "💩", "😃", "😀",
            "🎱", "⚽️", "🎾", "🏉"
        ]
        self.game_grid = rx.vstack(spacing="15px")
        self.create_board()
        
    def create_board(self):
        # we want to make sure we have pairs of emojies in the grid
        emojis = self.emojis[: self.stage * 2] * self.stage * 2
        # randomize the list, i.e. shuffle
        random.shuffle(emojis)
        # set a counter to track some parameters
        count = 0
        items = []
        # now we can create the grid
        for _ in range(self.stage * 2):
            row = rx.hstack(spacing="15px")
            for __ in range(self.stage * 2):
                row.children.append(
                    rx.center(
                        rx.text(
                            # get the emoji from the list
                            emojis[count],
                            font_size="32px",
                            cursor="pointer",
                            transition="opacity 0.55s ease 0.35s",
                            # now we can set each opacity from the state class
                            opacity=State.emoji_list[count][1],
                            on_click=lambda: [
                                State.reveal_emoji(
                                    State.emoji_list[count], 
                                    emojis[count],
                                ),
                                State.check_emoji()
                            ]
                        ),
                        width="58px",
                        height="58px",
                        bg="#331e19",
                        border_radius="4px",
                        justify_content="center",
                        center_content=True,
                        cursor="pointer",
                    )
                )

                count += 1
            items.append(row)

        self.game_grid.children = items
        return self.game_grid

def index() -> rx.Component:
    # Our Main UI Component
    return rx.center(
        rx.vstack(
            # title
            rx.heading(
                "MemoryRX",
                font_size="65px",
                font_weight="extrabold",
                color="#AEA6A4"
            ),
            rx.spacer(),
            # our game instance here...
            game.game_grid, 
            rx.spacer(),
            # result text
            rx.text.strong(
                State.result,
                font_size="25px",
                color="#AEA6A4"
            ),
            spacing="25px",
            align="center"
        ),
        bg="#140501",
        height="100vh",
        max_width="auto",
        # display="grid",
        position="relative",
        overlay="hidden",
    )

game = MemoryRX()

app = rx.App()
app.add_page(index)