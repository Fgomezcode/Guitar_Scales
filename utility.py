import json


class ConsoleColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',
                   'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


# PROGRAMMATICALLY GENERATED TO ALLOW CUSTOM TUNING
def get_tuning() -> [str]:
    tuning = []
    is_valid = False
    string_count = 6  # default

    while not is_valid:
        print(f'HOW MANY STRINGS ARE ON YOUR INSTRUMENT?')
        try:
            string_count = int(input('Enter number 1 - 12:\t'))
        except:
            continue

        if 0 < string_count <= 12:
            is_valid = True
    print()

    prompt = 'START WITH THE LOWEST STRING:\t'
    temp = f'{prompt}'
    print(temp)

    count = string_count

    while count > 0:
        x = str(input(f'STRING {count}:\t'))
        x = x.strip()
        x = x.upper()

        if x not in chromatic_scale or x == '' or x == ' ':
            print(f'INVALID NOTATION')
            continue
        else:
            count -= 1
        tuning.append(x)

    user_input = 'N'
    while user_input != 'Y':
        check = f'You Entered {" ".join(tuning)} is this correct? (y/n):\t'
        user_input = input(check).upper()

        if user_input != 'Y':
            print(f'No worries, lets start over.\n')

    print()
    return tuning


def get_root_note():
    root = ''
    user_input = ''
    while user_input != 'Y':
        print(f'CHOOSE A ROOT NOTE.')
        root = str(input('Root Note:\t'))
        root = root.strip()
        root = root.upper()

        if root not in chromatic_scale or root == '' or root == ' ':
            print(f'INVALID NOTATION\n')
            continue
        check = f'You Entered {root} is this correct? (y/n):\t'
        user_input = input(check).upper()

        if user_input != 'Y':
            print(f'OK, lets pick a new root note.\n\n')

    print()
    return root


def display(root_note: str, tuning: str) -> None:  # F
    """Display INDEX - ROOT NOTE - KEY - PROGRESSIONS. DISPLAYS ALL CONTENT"""
    counter = 0

    with open('Scales.json') as f:
        data = json.load(f)
    header = data['Scales'][0]

    # ==============================================
    # PRINT HEADER INFORMATION
    # ==============================================
    for i, key in enumerate(header[root_note]):
        spacer = "-" * (len(root_note) + len(header["names"][i]) + len(key) + 6)

        # display root note name of scale and notes in key
        print(
            f'{i + 1} {root_note} {header["names"][i]} {key}',
            end='')

        # PRINT FRETBOARD
        # ==============================================
        notes = key.split()
        board, frets = display_fretboard(tuning, notes, root_note)

        print(f'\nFRETBOARD')

        print(f'{frets}')

        for string in board:
            print(f'{string}')

        print(f'{frets}')

        # PRINT PROGRESSIONS
        # ==============================================
        print(f'\nPROGRESSIONS')

        for j in header['progressions']:
            t = [int(x) for x in j[1]]  # make list into ints
            w = header[root_note][i].split()  # make list of notes
            s = ''
            # used to format

            for k in t:
                try:
                    s += f' {w[k - 1]} '  # make string of notes
                except:
                    s += ''  # if the string cant be made skip

            print(f'|| {" ".join(str(j[1])):10}{j[0]:20}{s:20}', end='  ')  #

            if counter % 2 == 0:
                print()  # format

            counter += 1
        print('\n')  # format


def display_fretboard(tuning: str, notes: [str], root_note: str) -> [str]:
    if tuning is None:
        tuning = ['E', 'B', 'G', 'D', 'A', 'E']
    else:
        tuning.reverse()

    string_notes = []
    # make strings
    for i in range(len(tuning)):
        string_notes.append((chromatic_scale.index(tuning[i].strip()), chromatic_scale.index(tuning[i]) + 13))

    f_nums = number_frets()
    board = make_fretboard(notes, string_notes, tuning, root_note)

    return board, f_nums


def make_fretboard(_notes: [str], string_notes: [str], tuning: [str], root_note: str) -> [str]:
    f = []
    temp = ''
    s_string = []
    spacer = '-'

    for i in string_notes:
        f.append(chromatic_scale[i[0]: i[1]])

    # name string w/ notes
    for j, string in enumerate(f):
        temp += f'{tuning[j] + "|":5}'

        for i in range(len(string)):
            if string[i] not in _notes:  # if specific note not in the key add blank space
                temp += f'{spacer:5}'

            elif string[i] == root_note:
                temp += f'{string[i]:5}'

            else:  # include the note - it exists in the key
                temp += f'{string[i]:5}'

        s_string.append(temp)
        temp = ''

    return s_string


def number_frets():
    num_frets = ''
    for z in range(0, 13):
        if z == 0:
            num_frets += f'{z:>6} -'
        elif 9 <= z < 12:
            num_frets += f'{z:3} -'
        elif z >= 12:
            num_frets += f'{z:3}'
        else:
            num_frets += f'{z:3} -'
    return num_frets
