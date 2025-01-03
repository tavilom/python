import flet as ft
from PIL import Image
import random
import os

class PuzzleGame:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Jogo de Quebra-Cabeça"
        self.grid_size = 3  # Tamanho do grid (3x3)
        self.tile_size = 100  # Tamanho de cada peça
        self.images = self.load_images()
        self.current_image_index = 0
        self.tiles = []  # Lista de peças do quebra-cabeça
        self.empty_tile = None
        self.create_menu()

    def load_images(self):
        images = []
        for filename in os.listdir('imagens'):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                images.append(os.path.join('imagens', filename))
        return images

    def create_menu(self):
        self.page.controls.clear()
        self.page.add(
            ft.Column(
                [
                    ft.Text("Menu Principal", size=30, weight="bold"),
                    ft.ElevatedButton("Iniciar Jogo", on_click=self.start_game),
                    ft.ElevatedButton("Sair", on_click=lambda _: self.page.window_close())
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        self.page.update()

    def start_game(self, _):
        if not self.images:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nenhuma imagem encontrada na pasta 'imagens'."))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        self.current_image_index = 0
        self.create_game_frame()

    def create_game_frame(self):
        self.page.controls.clear()
        self.page.add(ft.Column([ft.Text("Quebra-Cabeça", size=24, weight="bold")]))
        self.load_next_image()

    def load_next_image(self):
        if self.current_image_index < len(self.images):
            image_path = self.images[self.current_image_index]
            self.prepare_puzzle(image_path)
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Você completou todas as imagens!"))
            self.page.snack_bar.open = True
            self.page.update()

    def prepare_puzzle(self, image_path):
        # Carrega e redimensiona a imagem
        image = Image.open(image_path)
        image = image.resize((self.grid_size * self.tile_size, self.grid_size * self.tile_size))

        # Divide a imagem em peças
        self.tiles = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                left = col * self.tile_size
                upper = row * self.tile_size
                right = left + self.tile_size
                lower = upper + self.tile_size
                tile = image.crop((left, upper, right, lower))
                self.tiles.append((row, col, tile))

        # Embaralha as peças
        random.shuffle(self.tiles)
        self.render_puzzle()

    def render_puzzle(self):
        grid = ft.GridView(
            expand=True,
            runs=self.grid_size,
            max_extent=self.tile_size,
            child_aspect_ratio=1.0,
        )
        self.page.controls.clear()

        for idx, (row, col, tile) in enumerate(self.tiles):
            if idx == len(self.tiles) - 1:  # Espaço vazio
                self.empty_tile = (row, col)
                grid.controls.append(ft.Container(bgcolor=ft.colors.GREY))
                continue

            # Converte a peça em imagem exibível
            tile.save(f"tile_{row}_{col}.png")
            tile_control = ft.Image(
                src=f"tile_{row}_{col}.png",
                width=self.tile_size,
                height=self.tile_size,
                on_click=lambda _, r=row, c=col: self.move_tile(r, c),
            )
            grid.controls.append(tile_control)

        self.page.add(grid)
        self.page.update()

    def move_tile(self, row, col):
        if self.is_adjacent(row, col, *self.empty_tile):
            for i, (r, c, tile) in enumerate(self.tiles):
                if r == row and c == col:
                    self.tiles[i] = (*self.empty_tile, tile)
                    self.empty_tile = (row, col)
                    break
            self.render_puzzle()
            if self.check_win():
                self.page.snack_bar = ft.SnackBar(ft.Text("Parabéns! Você completou o quebra-cabeça!"))
                self.page.snack_bar.open = True
                self.page.update()

    def is_adjacent(self, r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def check_win(self):
        for idx, (row, col, _) in enumerate(self.tiles):
            if idx == len(self.tiles) - 1:
                continue
            expected_row = idx // self.grid_size
            expected_col = idx % self.grid_size
            if row != expected_row or col != expected_col:
                return False
        return True


def main(page: ft.Page):
    PuzzleGame(page)


ft.app(target=main)
