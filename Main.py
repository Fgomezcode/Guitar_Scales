import utility as util


def welcome() -> None:
    header = f'GUITAR SCALE ALMANAC'
    sub_header = f'This program generates keys and chord progressions.\n' \
                 f'It was developed with GUITAR and BASS in mind, but is not limited to those instruments.\n' \
                 f'A \'fretboard\' with specified number of strings and tuning will also be created.\n' \
                 f'Please use natural and sharp (\'#\') notation when entering tuning and root note.\n'

    print(
        f'{header}')
    print(f'{sub_header}')


def menu():
    retune = f'1: CHANGE TUNING.'
    new_note = f'2: CHANGE ROOT NOTE.'
    refresh = f'3: APPLY CHANGES.'
    end = f'4: QUIT.'

    print(f'{retune}\n{new_note}\n{refresh}\n{end}\n')

    is_running = True
    is_tuning  = False
    is_root    = False
    is_refresh = False

    selection = input('What would you like to do?:\t')
    selection = selection.strip()

    selection = int(selection)
    if selection == 1:
        is_tuning = True

    if selection == 2:
        is_root = True
    if selection == 3:
        is_refresh = True
    if selection == 4:
        is_running = False

    return is_tuning, is_root, is_refresh, is_running


def run() -> None:
    welcome()

    intro = f'LET\'S GET YOUR TUNING FIGURED OUT.\n'
    print(f'{intro}')

    is_running = True
    is_tuning = True
    is_root = True
    is_refresh = True

    while is_running:

        while is_tuning:
            tuning = util.get_tuning()
            is_tuning = False

        while is_root:
            root = util.get_root_note()
            is_root = False

        while is_refresh:
            util.display(root, tuning)
            is_refresh = False

        # Loop Control
        # -----------------------------------------------------------------------------------
        print(f'Current Tuning: {" ".join(tuning)}')
        print(f'Current Root Note: {root}')

        is_tuning, is_root, is_refresh, is_running = menu()
        print()


if __name__ == '__main__':
    run()
