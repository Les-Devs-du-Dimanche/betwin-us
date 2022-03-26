from multiprocessing import freeze_support

import ctypes


if __name__ == '__main__':
    freeze_support()

    # check python version
    import sys

    MIN_VER = (3, 10)

    if sys.version_info[:2] < MIN_VER:
        sys.exit(
            'This game requires Python {}.{}'.format(*MIN_VER)
        )

    # hide pygame init message
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # start game
    from src.game import Game

    game = Game()
    game.run()
