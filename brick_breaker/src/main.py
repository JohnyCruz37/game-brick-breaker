import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#caminho base para o projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from game import Game

if __name__ == "__main__":
    game = Game(BASE_DIR)
    game.run()
    game.quit()