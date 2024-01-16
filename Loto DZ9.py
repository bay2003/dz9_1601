from random import randint, sample

def generate_unique_numbers(count, minbound, maxbound):
    if count > maxbound - minbound + 1:
        raise ValueError('Incorrect input parameters')
    return sample(range(minbound, maxbound + 1), count)
class Keg:
    num = None

    def __init__(self):
        self.num = randint(1, 90)

    def __str__(self):
        return str(self.num)

class Card:
    __rows = 3
    __cols = 9
    __nums_in_row = 5
    __data = None
    __emptynum = 0
    __crossednum = -1

    def __init__(self):
        uniques_count = self.__nums_in_row * self.__rows
        uniques = generate_unique_numbers(uniques_count, 1, 90)

        self.__data = []
        for i in range(self.__rows):
            row = sorted(uniques[self.__nums_in_row * i: self.__nums_in_row * (i + 1)])
            empty_positions = sample(range(self.__cols), self.__cols - self.__nums_in_row)
            for pos in empty_positions:
                row.insert(pos, self.__emptynum)
            self.__data.extend(row)

    def __str__(self):
        delimiter = '--------------------------'
        ret = delimiter + '\n'
        for i in range(self.__rows):
            for j in range(self.__cols):
                num = self.__data[i * self.__cols + j]
                ret += f'{num:2}' if num != self.__emptynum else '  '
                ret += ' '
            ret += '\n'
        ret += delimiter
        return ret

    def __contains__(self, item):
        return item in self.__data

    def cross_num(self, num):
        try:
            index = self.__data.index(num)
            self.__data[index] = self.__crossednum
        except ValueError:
            raise ValueError(f'Number not in card: {num}')

    def closed(self) -> bool:
        return set(self.__data) == {self.__emptynum, self.__crossednum}
class Game:
    __player_cards = []
    __compcards = []
    __numkegs = 90
    __kegs = []

    def __init__(self, num_players):
        for _ in range(num_players):
            self.__player_cards.append(Card())
        self.__compcards.append(Card())
        self.__compcards.append(Card())
        self.__kegs = generate_unique_numbers(self.__numkegs, 1, 90)

    def play_round(self) -> int:
        keg = self.__kegs.pop()
        print(f'Новый бочонок: {keg} (осталось {len(self.__kegs)})')

        # Ходы игроков
        for i, card in enumerate(self.__player_cards):
            print(f'----- Карточка игрока {i + 1} ------\n{card}')
            if keg in card:
                card.cross_num(keg)
                print(f'Число {keg} зачеркнуто.')
                if card.closed():
                    return i + 1
            else:
                useranswer = input(f'Игрок {i + 1}, у вас нет числа {keg}. Введите n для продолжения: ').lower().strip()
                if useranswer != 'n':
                    return i + 1  # Игрок ошибся, он проиграл

        # Ходы компьютерных игроков
        for i, card in enumerate(self.__compcards):
            print(f'----- Карточка компьютера {i + 1} ------\n{card}')
            if keg in card:
                card.cross_num(keg)
                print(f'Компьютер {i + 1} зачеркнул число {keg}.')
                if card.closed():
                    return -(i + 1)  # Компьютер выиграл

        return 0
if __name__ == '__main__':
    num_players = int(input('Введите количество игроков: '))
    game = Game(num_players)
    while True:
        winner = game.play_round()
        if winner > 0:
            print(f'Игрок {winner} выиграл')
            break
        elif winner < 0:
            print(f'Компьютер {-winner} выиграл')
            break
