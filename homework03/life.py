import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)
        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.clist = self.cell_list()
        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True

        self.clist = game.cell_list()
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_cell_list(self.clist)
            self.update_cell_list(self.clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True) -> list:
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = [[0 for i in range(self.cell_width)]
                      for j in range(self.cell_height)]
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if randomize:
                    self.clist[i][j] = random.randint(0, 1)
        return self.clist

    def draw_cell_list(self, clist: list) -> None:
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        clist = self.clist
        size = self.cell_size
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if clist[i][j] == 0:
                    color = pygame.Color('white')
                else:
                    color = pygame.Color('green')
                rect = Rect(j*size+1, i*size+1, size-1, size-1)
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: tuple) -> list:
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        row, col = cell
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i in range(0, self.cell_height) and j in range(0, self.cell_width) and (i != row or j != col):
                    neighbours.append(self.clist[i][j])
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = deepcopy(self.clist)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neigh = sum(self.get_neighbours((i, j)))
                if self.clist[i][j]:
                    if neigh < 2 or neigh > 3:
                        new_clist[i][j] = 0
                else:
                    if neigh == 3:
                        new_clist[i][j] = 1
        self.clist = new_clist
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
