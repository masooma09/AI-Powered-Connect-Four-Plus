import pygame
import sys
import math
import random
import time
from enum import Enum
from variables import ROW_COUNT, COLUMN_COUNT, SQUARESIZE, size, RADIUS, colors, height, width, PLAYER, AI, PLAYER_PIECE, AI_PIECE, thinking_time, game_end_button_width, game_end_button_height, level_button_height, level_button_width
from functions import create_board, is_valid_location, get_next_open_row, drop_piece, game_over_check, draw_board, board, screen, draw_dotted_circle
from score_ai import pick_best_move
from minmax_ai import minimax
from ui_components import Button
from ui_components import ai_move_sound, self_move_sound, ai_wins_sound, player_wins_sound

class Difficulty(Enum):
    EASY = 1
    INTERMEDIATE = 2
    HARD = 3
    IMPOSSIBLE = 4
    GODMODE = 5

class ConnectFour:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.game_over = False
        self.turn = None
        self.board = create_board()
        self.myfont = pygame.font.SysFont("monospace", 80)
        padding = 20
        restart_button_y = height // 2
        quit_button_y = restart_button_y + game_end_button_height + padding
        self.center_x = width // 2 - game_end_button_width // 2

        self.quit_button = Button(colors["RED"], self.center_x, quit_button_y, game_end_button_width, game_end_button_height, 'Quit')
        self.restart_button = Button(colors["GREEN"], self.center_x, restart_button_y, game_end_button_width, game_end_button_height, 'Restart')

        pygame.display.set_caption("Connect Four")
        self.opponent = self.choose_opponent()
        self.fog_mode = self.opponent == "FogAI"

        if self.opponent in ["AI", "FogAI"]:
            self.difficulty = self.choose_difficulty()
            self.turn = PLAYER
        elif self.opponent == "AI vs AI":
            self.difficulty = Difficulty.HARD
            self.turn = AI
        else:
            self.turn = PLAYER

        self.first = True
        screen.fill(colors["DARKGREY"])
        if self.fog_mode:
            draw_board(self.board, PLAYER_PIECE)
        else:
            draw_board(self.board)
        pygame.display.update()

    def handle_mouse_motion(self, event):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))
        posx = event.pos[0]
        if self.turn == PLAYER:
            draw_dotted_circle(screen, posx, int(SQUARESIZE / 2), RADIUS, colors["YELLOW"], gap_length=6)
        pygame.display.update()

    def handle_mouse_button_down(self, event):
        if self.opponent == "Player":
            p = AI_PIECE if self.first else PLAYER_PIECE
        else:
            p = PLAYER_PIECE

        posx = event.pos[0]

        if (self.turn == PLAYER and self.opponent in ["AI", "FogAI"]) or self.opponent == "Player":
            col = int(math.floor(posx / SQUARESIZE))
            if is_valid_location(self.board, col):
                self_move_sound.play()
                self._extracted_from_ai_move_7(col, p, "You win!! ^_^")

                if self.fog_mode:
                    draw_board(self.board, PLAYER_PIECE)
                else:
                    draw_board(self.board)
                pygame.display.update()

                self.turn ^= 1
                self.first = not self.first

                if self.opponent == "Player":
                    self.render_thinking("Player #" + str(self.turn) + " Turn")
                else:
                    self.render_thinking("Thinking...")

        if self.game_over:
            if self.quit_button.is_over((posx, event.pos[1])):
                sys.exit()
            elif self.restart_button.is_over((posx, event.pos[1])):
                self.__init__()

    def ai_move(self):
        if self.opponent in ["AI", "FogAI"]:
            player = AI_PIECE
        elif self.opponent == "AI vs AI":
            player = self.turn + 1

        if self.difficulty == Difficulty.EASY:
            col = random.randint(0, COLUMN_COUNT - 1)
            time.sleep(thinking_time + 1)

        elif self.difficulty == Difficulty.INTERMEDIATE:
            col = pick_best_move(self.board, player, directions=tuple(1 if i in random.sample(range(4), 2) else 0 for i in range(4)))
            time.sleep(thinking_time + 1.2)

        elif self.difficulty == Difficulty.HARD:
            col, _ = minimax(self.board, 4, -math.inf, math.inf, True)
            time.sleep(thinking_time + 1.5)

        elif self.difficulty == Difficulty.IMPOSSIBLE:
            col, _ = minimax(self.board, 6, -math.inf, math.inf, True)

        elif self.difficulty == Difficulty.GODMODE:
            col, _ = minimax(self.board, 7, -math.inf, math.inf, True)

        if is_valid_location(self.board, col):
            ai_move_sound.play()
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, player)

            if self.fog_mode:
                draw_board(self.board, PLAYER_PIECE)
            else:
                draw_board(self.board)

            pygame.display.update()

            if game_over_check(self.board, player):
                self.display_winner("AI wins!! :[")
                self.game_over = True
                return self.handle_game_over()

            self.turn ^= 1

    def _extracted_from_ai_move_7(self, col, piece, win_message):
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, piece)

        if game_over_check(self.board, piece):
            self.display_winner(win_message)
            self.game_over = True
            return self.handle_game_over()

    def display_winner(self, message):
        self.clear_label()
        if message == "AI wins!! :[":
            ai_wins_sound.play()
        elif message == "You win!! ^_^":
            player_wins_sound.play()
        label = self.myfont.render(message, 1, colors["YELLOW"])
        screen.blit(label, (40, 10))
        pygame.display.update()

    def handle_game_over(self):
        draw_board(self.board)
        pygame.display.update()
        self.quit_button.draw(screen, outline_color=colors["DARKGREY"])
        self.restart_button.draw(screen, outline_color=colors["DARKGREY"])
        pygame.display.update()

        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    if self.quit_button.is_over((posx, posy)):
                        sys.exit()
                    elif self.restart_button.is_over((posx, posy)):
                        self.__init__()
                        return self.game_start()

    def choose_difficulty(self):
        btn_height = 90
        text_color = colors['DARKGREY']
        btn_y = [i * (btn_height + 20) + height / 1.8 for i in range(-3, 3)]

        buttons = {
            Difficulty.EASY: 'EASY',
            Difficulty.INTERMEDIATE: 'INTERMEDIATE',
            Difficulty.HARD: 'HARD',
            Difficulty.IMPOSSIBLE: 'IMPOSSIBLE',
            Difficulty.GODMODE: 'GODMODE'
        }

        btn_objs = {}
        for idx, (level, text) in enumerate(buttons.items()):
            btn_objs[level] = Button(colors["GREEN" if idx < 2 else "YELLOW" if idx < 4 else "RED"],
                                     self.center_x, btn_y[idx], 250, btn_height, text, text_color=text_color)

        screen.fill(colors["GREY"])
        for btn in btn_objs.values():
            btn.draw(screen)

        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    for level, btn in btn_objs.items():
                        if btn.is_over((posx, posy)):
                            return level

    def choose_opponent(self):
        btn_height = 90
        text_color = colors['DARKGREY']
        btn_y = [i * (btn_height + 20) + height / 1.8 for i in range(-2, 2)]
        self.player = Button(colors['GREEN'], self.center_x, btn_y[0], 300, btn_height, 'Player', text_color=text_color)
        self.ai = Button(colors['YELLOW'], self.center_x, btn_y[1], 300, btn_height, 'AI', text_color=text_color)
        self.aivsai = Button(colors['RED'], self.center_x, btn_y[2], 300, btn_height, 'AI vs AI', text_color=text_color)
        self.fog_ai = Button(colors['YELLOW'], self.center_x, btn_y[3], 300, btn_height, 'Fog of War (PvAI)', text_color=text_color)

        screen.fill(colors['GREY'])
        self.player.draw(screen)
        self.ai.draw(screen)
        self.aivsai.draw(screen)
        self.fog_ai.draw(screen)

        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    if self.player.is_over((posx, posy)):
                        return "Player"
                    elif self.ai.is_over((posx, posy)):
                        return "AI"
                    elif self.aivsai.is_over((posx, posy)):
                        return "AI vs AI"
                    elif self.fog_ai.is_over((posx, posy)):
                        return "FogAI"

    def game_start(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)

            if self.opponent in ["AI", "FogAI"] and self.turn == AI and not self.game_over:
                self.ai_move()
            elif self.opponent == "AI vs AI":
                self.render_thinking("AI 1 is thinking..." if self.turn == 1 else "AI 2 is thinking...")
                self.ai_move()

    def clear_label(self):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))

    def render_thinking(self, text):
        self.clear_label()
        label = pygame.font.SysFont("monospace", 60).render(text, 1, colors["YELLOW"])
        screen.blit(label, (40, 10))
        pygame.display.update()

if __name__ == "__main__":
    game = ConnectFour()
    game.game_start()