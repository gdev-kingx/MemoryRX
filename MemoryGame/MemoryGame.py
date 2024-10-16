""" MemoryRX (The Game) """
# Modules
import reflex as rx
import random
import asyncio

class State(rx.State):
    # to set the opacity, we need to create states for all tiles/emojis
    # get opacity states
    emoji_list: list[list] = [[i, "0%"] for i in range(36)]
    
    moves: int = 0
    misses: int = 0
    count: int = 0
    track: list = []
    score: int = 0
    result: str
    game_over: bool = False

    def reveal_emoji(self, emoji, emoji_type):
        if not self.game_over:
            index = emoji[0]
            self.emoji_list = [
                [i, "100%"] if i == index else [i, opacity]
                for i, opacity in self.emoji_list
            ]
            self.count += 1
            self.track.append((emoji_type, emoji))
            self.moves += 1
            return State.check_emoji

    async def check_emoji(self):
        if self.count == 2:
            if self.track[0][0] == self.track[1][0]:
                self.score += 1
                if self.score == 8:
                    self.result = 'Congrats!! You WON!'
                    self.game_over = True
            else:
                self.misses += 1
                if self.misses == 8:
                    self.result = 'Game Over! You LOSE!'
                    self.game_over = True
                indicies = [e[1][0] for e in self.track]
                self.emoji_list = [
                    [i, "0%"] if i in indicies else [i, opacity]
                    for i, opacity in self.emoji_list
                ]
            self.count = 0
            self.track = []
        
        await asyncio.sleep(2)

    def restart_game(self):
        self.reset()
        return State.initialize_game

    def initialize_game(self):
        self.emoji_list = [[i, "0%"] for i in range(36)]
        self.moves = 0
        self.misses = 0
        self.count = 0
        self.track = []
        self.score = 0
        self.result = ""
        self.game_over = False

class MemoryRX:
    def __init__(self):
        self.stage: int = 2
        self.emojis: list = [
            # "🔥", "🍎", "😡", "💀",
            "🤣", "😅", "😭", "🥺",
            # "🎱", "⚽️", "🎾", "🏉"
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
                            font_size="42px",
                            cursor="pointer",
                            transition="opacity 0.55s ease 0.35s",
                            # now we can set each opacity from the state class
                            opacity=State.emoji_list[count][1],
                            on_click=State.reveal_emoji(State.emoji_list[count], emojis[count])
                        ),
                        width="75px",
                        height="75px",
                        bg="rgba(48, 99, 131, 0.6)",
                        border="2px solid rgba(220, 236, 246)",
                        border_radius="6px",
                        justify_content="center",
                        center_content=True,
                        cursor="pointer",
                    )
                )

                count += 1
            items.append(row)

        self.game_grid.children = items
        return self.game_grid
    
    def score_board(self):
        return rx.hstack(
            rx.text(f"Score: {State.score}"),
            spacing="20px",
            color="rgba(220, 236, 246)",
            font_size="30px",
            font_weight="bold",
            font_family="Agdasima",
        )
    
    def move_board(self):
        return rx.hstack(
            rx.text(f"Moves: {State.moves}"),
            spacing="20px",
            color="rgba(220, 236, 246)",
            font_size="30px",
            font_weight="bold",
            font_family="Agdasima",
        )
    
    def miss_board(self):
        return rx.hstack(
            rx.text(f"Misses: {State.misses}"),
            spacing="20px",
            color="rgba(220, 236, 246)",
            font_size="30px",
            font_weight="bold",
            font_family="Agdasima",
        )

def index() -> rx.Component:
    # Our Main UI Component
    return rx.center(
        rx.vstack(
            # title
            rx.heading(
                "MemoryRX",
                font_size="105px",
                font_family="Hammersmith One",
                font_weight="extrabold",
                color="rgba(220, 236, 246)"
            ),
            rx.spacer(),
            rx.spacer(),
            # our game instance here...
            game.game_grid, 
            rx.spacer(),
            rx.container(
                rx.hstack(
                    rx.box(
                        game.score_board(),
                        bg="rgba(48, 99, 131, 0.6)",
                        border="2px dotted rgba(220, 236, 246)",
                        border_radius="5px",
                        width="fit",
                        margin="12px",
                        padding="12px",
                    ),
                    rx.box(
                        game.move_board(),
                        bg="rgba(48, 99, 131, 0.6)",
                        border="2px dotted rgba(220, 236, 246)",
                        border_radius="5px",
                        width="fit",
                        margin="12px",
                        padding="12px",
                    ),
                    rx.box(
                        game.miss_board(),
                        bg="rgba(48, 99, 131, 0.6)",
                        border="2px dotted rgba(220, 236, 246)",
                        border_radius="5px",
                        width="fit",
                        margin="12px",
                        padding="12px",
                    ),
                ),
            ),
            rx.button(
                "Restart Game",
                on_click=State.restart_game,
                is_disabled=~State.game_over,
                bg="rgba(48, 99, 131, 0.6)",
                border="2px solid rgba(220, 236, 246)",
                color="rgba(220, 236, 246)",
                size="4",
                font_size="30px",
                font_weight="bold",
                font_family="Agdasima",
                radius="medium",
                cursor="pointer",
            ),
            # result text
            rx.text.strong(
                State.result,
                font_size="45px",
                font_family="Agdasima",
                color="rgba(220, 236, 246)"
            ),
            spacing="25px",
            align="center"
        ),
        background = "linear-gradient(180deg, #07283B 0%, 14.407502131287297%, #63ACBF 54.390451832907075%, 79.96589940323956%, #020E1A 100%)",    
        height="100vh",
        max_width="auto",
        position="relative",
        overlay="hidden",
    )

game = MemoryRX()

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Agdasima&family=Hammersmith+One&display=swap",
    ],
)
app.add_page(index)
