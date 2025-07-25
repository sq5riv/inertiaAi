import os

from game.inertia import Inertia, Moves
from random import choice, random
from json import dump, load, dumps
import logging

logging.basicConfig(level=logging.INFO, filename='log.txt')
logging.info('Start')

class QLearning:
    def __init__(self, x: int, y: int) -> None:
        self.maps = []
        self.x = x
        self.y = y
        self.get_random_maps(1000)
        self.q_table = {}

    def get_random_maps(self, n: int) -> None:
         for i in range(n):
             self.maps.append(Inertia.map_generator(self.x,self.y))

    def add_value_into_q_table(self, sate: str, action: Moves, q_value: float) -> None:
        self.q_table.setdefault(sate, {})[action] = q_value

    def get_value_from_q_table  (self, state: str, action: Moves) -> float:
        return self.q_table.setdefault(state, 0).setdefault(action, 0)

    def get_best_action_or_random(self, state: str) -> Moves:
        to_max = self.q_table.get(state, {choice(list(Moves)): 0.0})
        return max(to_max, key=to_max.get)

    def choose_action(self, state: str, temp: float = 0.6) -> Moves:
        if random() < temp:
            return choice(list(Moves))
        else:
            return self.get_best_action_or_random(state)

    @staticmethod
    def calculate_reward(state: dict, new_state: dict) -> float:
        if new_state['state'] == 'END':
            return -5.0
        if state['state'] == 'WIN':
            return 5.0
        return state['actual_gems'] - new_state['actual_gems'] + 1.0

    def update_q_list(self, state: dict, action: Moves, new_state: dict, alpha: float = 0.1, gamma: float = 0.9) -> None:
        max_future_q = max(self.q_table.get(new_state['map'], {0.0: 0.0}).values())
        current_q = self.q_table.get((state['map'], action), 0.0)
        self.q_table.setdefault(state['map'], {})[action] = current_q + alpha * (self.calculate_reward(state, new_state) + gamma * max_future_q - current_q)

    def learnig_loop(self):

        for _ in range(500):
            logging.info(f"Round {_}")
            print(f"Round {_}")
            for mapa in self.maps:
                game = Inertia(mapa)
                logging.info(f"Work on map \n{game.get_human_board()}")
                i = 0
                while game:
                    logging.info(f"Step {i}")
                    i+=1
                    state = game.check_state()
                    action = self.choose_action(state['map'])
                    new_state = game.move(action)
                    self.update_q_list(state, action, new_state)
                    if new_state['state'] == 'WIN' or new_state['state'] == 'END':
                        game = None
        logging.info(f'{self.q_table}')
        self.save_q_table()


    def save_q_table(self) -> None:
        with open('q_table.json', 'w') as f:

            dump(self.q_table, f, indent=4)


class QPlay:

    def __init__(self, game:str, q_table_path:str):
        #self.q_table = None
        self.game = Inertia(game)
        #self.get_q_table(q_table_path)

    def q_table(self, path: str) -> None:
        with open(path, 'r') as f:
            self.q_table = load(f)

def main() -> None:
    QLearning(3,3).learnig_loop()

if __name__ == '__main__':
    main()
