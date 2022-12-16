from pathlib import Path
import json


# CREATE THE JSON FILE

def get_progressions() -> [str]:
    """Open file containing progressions and return their numerical values plus name"""
    values = {'I': 1, 'i': 1, 'II': 2, 'ii': 2, 'iidim': 2, 'III': 3, 'iii': 3, 'IV': 4, 'iv': 4, 'V': 5,
              'v': 5, 'VI': 6, 'vi': 6, 'VII': 7, 'vii': 7, 'VIII': 8}

    progressions = []

    with open('ScaleProgressions.txt') as file:
        scale_progressions = file.readlines()
    file.close()
    a = ''
    b = ''

    for prog in scale_progressions:
        prog = prog.strip()
        prog = prog.split(' - ')

        a = ' - '.join(prog)

        for note in prog:
            b += f'{values[note]}'
        progressions.append((a, b))
        b = ''
    return progressions


def get_scale_names() -> [str]:
    """Open file containing name of scales returns its contents."""
    names = []
    with open('ScaleNames.txt') as file:
        scale_names = file.readlines()
    file.close()

    for name in scale_names:
        names.append(name.strip())

    return names


def get_scale_steps() -> [str]:
    """Open file containing steps returns its contents."""
    with open('ScaleSteps.txt') as file:
        key_steps = file.readlines()
    file.close()
    return key_steps


def clean_input(s: str) -> [str]:
    """Sanitize step input - return list"""
    s = 'r ' + s
    s = s.upper()
    s = s.strip()
    s = s.split(' ')
    return s


def generate_steps() -> [str]:
    """Sanitize all steps pulled from file"""
    _steps_from_file = get_scale_steps()

    keys = []
    for step in _steps_from_file:
        keys.append(clean_input(step))
    return keys


def translate_steps_to_notes(ch_scale: [str], root: int):
    steps = generate_steps()
    step_values = {'R': 0, 'H': 1, 'W': 2, 'WH': 3}
    return_list = []
    t_scale = ''

    for j, step in enumerate(steps):
        buffer = root

        for i in range(len(step)):
            temp = step_values[step[i]]  # int
            buffer += temp
            t_scale += f'{ch_scale[buffer]} '
        t_scale = t_scale.rstrip()
        return_list.append(t_scale)
        t_scale = ''

    return return_list


def generate_keys() -> [str]:  # remove root note will get passed in other function
    """generates notes based on given steps"""

    # Two octaves to allow full cycle - without doing any math to manipulate the scale
    scales = []
    names = get_scale_names()
    progressions = get_progressions()
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',
                       'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    scale_dict = {}
    p_note = []
    t = []
    s = ''
    for note in chromatic_scale[:12]:
        root_index = chromatic_scale.index(note)
        scales.append(translate_steps_to_notes(chromatic_scale, root_index))

    # Make dictionary
    for i, note in enumerate(chromatic_scale[:12]):
        scale_dict[note] = scales[i]

    return scale_dict, names, progressions


def make_json_file():
    scales, names, progs = generate_keys()

    sk = list(scales.keys())
    data = {}
    for key in scales.keys():
        data[key] = {
            'keys': scales[key],
        }

    final = {'Scales': [{
        sk[0]: data[sk[0]]['keys'],
        sk[1]: data[sk[1]]['keys'],
        sk[2]: data[sk[2]]['keys'],
        sk[3]: data[sk[3]]['keys'],
        sk[4]: data[sk[4]]['keys'],
        sk[5]: data[sk[5]]['keys'],
        sk[6]: data[sk[6]]['keys'],
        sk[7]: data[sk[7]]['keys'],
        sk[8]: data[sk[8]]['keys'],
        sk[9]: data[sk[9]]['keys'],
        sk[10]: data[sk[10]]['keys'],
        sk[11]: data[sk[11]]['keys'],
        'names': names,
        'progressions': progs}
    ]}
    with open('Scales.json', 'w', encoding='utf-8') as outfile:
        json.dump(final, outfile, indent=4, ensure_ascii=False)


make_json_file()
