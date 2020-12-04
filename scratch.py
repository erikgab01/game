import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Тестовый класс для камеры, можешь переделать его в Enemy
class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 260

class Player(pygame.sprite.Sprite):
    right = True

    # Проверка, находится ли игрок в воздухе
    isMidAir = False

    # Методы
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('persona.png')

        self.rect = self.image.get_rect()

        # вектор скорости игрока
        self.change_x = 0
        self.change_y = 0

    def update(self):
        # тут мы передвигаем игрока
        # подрубаем гравитацию
        self.calc_grav()

        # Передвигаем его на право/лево
        self.rect.x += self.change_x

        # Передвигаемся вверх/вниз
        self.rect.y += self.change_y

    def calc_grav(self):

        # падать на землю под действием гравитации
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .95

        # Если уже на земле, то ставим позицию Y как 0
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.isMidAir = False
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        if self.isMidAir:
            return

        self.isMidAir = True

        self.rect.y += 10

        self.rect.y -= 10

        # тут надо добавить, чтобы перс не прыгал бесконечно
        self.change_y = -16

    # Передвижение игрока
    def go_left(self):
        # Сами функции будут вызваны позже из основного цикла
        self.change_x = -9  # Двигаем игрока по Х
        if (self.right):  # Проверяем куда он смотрит и если что, то переворачиваем его
            self.flip()
            self.right = False

    def go_right(self):
        # то же самое, но вправо
        self.change_x = 9
        if (not self.right):
            self.flip()
            self.right = True

    def stop(self):
        # вызываем этот метод, когда не нажимаем на клавиши
        self.change_x = 0

    def flip(self):
        # типо анимация :)
        self.image = pygame.transform.flip(self.image, True, False)


# Основная функция прогарммы
def main():
    # Инициализация
    pygame.init()

    # Установка высоты и ширины
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # Название игры
    pygame.display.set_caption("Платформер")

    # криэйтим игрока
    player = Player()
    object = Object()

    active_sprite_list = pygame.sprite.Group()

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    active_sprite_list.add(object)

    opened = True

    clock = pygame.time.Clock()

    # Основной цикл программы
    while opened:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если закрыл программу, то останавливаем цикл
                opened = False

            # Если нажали на стрелки клавиатуры, то двигаем объект
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Обновляем игрока
        active_sprite_list.update()

        # чтобы за мапу не уходил
        #if player.rect.right > SCREEN_WIDTH:
        #    player.rect.right = SCREEN_WIDTH

        #if player.rect.left < 0:
         #   player.rect.left = 0

        #active_sprite_list.draw(screen)

        # Реализация камеры
        # Все спрайты смещаются на xoffset относительно игрока
        xoffset = SCREEN_WIDTH / 2 - player.rect.x
        for sprite in active_sprite_list:
            sprite.rect.x += xoffset
        # Устанавливаем количество фреймов
        clock.tick(60)
        # Рендеринг
        screen.fill(BLACK)
        active_sprite_list.draw(screen)

        # Обновляем экран после рисования объектов
        pygame.display.flip()
    # Корректное закртытие программы
    pygame.quit()


if __name__ == '__main__':
    main()