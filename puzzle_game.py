import pygame
import random
from PIL import Image
import os

# Configurações gerais
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 100  # Tamanho de cada peça
GRID_SIZE = 3  # Tamanho do grid (3x3)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class PuzzleGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quebra-Cabeça Pygame")
        self.clock = pygame.time.Clock()
        self.running = True

        self.images = self.load_images()
        self.current_image_index = 0
        self.tiles = []
        self.empty_tile = None
        self.grid_positions = []

    def load_images(self):
        images = []
        for filename in os.listdir("imagens"):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                images.append(os.path.join("imagens", filename))
        return images

    def setup(self):
        if not self.images:
            print("Nenhuma imagem encontrada na pasta 'imagens'.")
            self.running = False
            return

        self.prepare_puzzle(self.images[self.current_image_index])

    def prepare_puzzle(self, image_path):
        # Carrega e redimensiona a imagem
        image = Image.open(image_path)
        image = image.resize((GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE))

        # Divide a imagem em peças
        self.tiles = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                left = col * TILE_SIZE
                upper = row * TILE_SIZE
                right = left + TILE_SIZE
                lower = upper + TILE_SIZE
                tile = image.crop((left, upper, right, lower))
                tile_surface = pygame.image.fromstring(
                    tile.tobytes(), tile.size, tile.mode
                )
                self.tiles.append((row, col, tile_surface))

        # Embaralha as peças
        random.shuffle(self.tiles)

        # Determina a posição do espaço vazio
        self.empty_tile = (GRID_SIZE - 1, GRID_SIZE - 1)

        # Configura as posições da grade
        self.grid_positions = [
            (col * TILE_SIZE, row * TILE_SIZE)
            for row in range(GRID_SIZE)
            for col in range(GRID_SIZE)
        ]

    def draw(self):
        self.screen.fill(WHITE)

        # Renderiza as peças
        for idx, (row, col, tile_surface) in enumerate(self.tiles):
            if (row, col) == self.empty_tile:
                continue
            x, y = self.grid_positions[idx]
            self.screen.blit(tile_surface, (x, y))

        if self.check_win():
            font = pygame.font.SysFont(None, 40)
            text = font.render(
                "Parabéns! Você completou o quebra-cabeça!", True, BLACK
            )
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // TILE_SIZE, y // TILE_SIZE
            if self.is_adjacent(row, col, *self.empty_tile):
                self.swap_tiles(row, col)

    def is_adjacent(self, r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def swap_tiles(self, row, col):
        for idx, (r, c, tile_surface) in enumerate(self.tiles):
            if (r, c) == (row, col):
                self.tiles[idx] = (*self.empty_tile, tile_surface)
                self.empty_tile = (row, col)
                break

    def check_win(self):
        for idx, (row, col, _) in enumerate(self.tiles):
            expected_row = idx // GRID_SIZE
            expected_col = idx % GRID_SIZE
            if row != expected_row or col != expected_col:
                return False
        return True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)

            self.draw()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    game = PuzzleGame()
    game.setup()
    if game.running:
        game.run()
