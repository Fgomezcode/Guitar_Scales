#selection = str(input("Which major key would you like to view (e B G D A E - case sensitive):\t")).capitalize()
def cleanProgressions():
    try:
        progressions_raw_file = 'Progressions.txt'
        inFile = open(progressions_raw_file, 'r')
        progs = inFile.readlines()
        inFile.close()
        progressions_clean = []
        # format and append list to a main lis
        for x in progs:
            y = x.replace('â€“', '')
            progressions_clean.append(y.split())
        return progressions_clean
    except FileNotFoundError:
        print('Failed to find Scale_Names.txt')
        x = input("Press any key to quit")

def getNames():
    try:
        scaleFile = 'Scale_Names.txt'
        rFile = open(scaleFile)
        scale_names = rFile.readlines()
        rFile.close()
        master_scales = []
        for name in scale_names:
            master_scales.append(name.replace('\n', ''))
        return master_scales
    except FileNotFoundError:
        print('Failed to find Scale_Names.txt')
        x = input("Press any key to quit")

def getSteps():
    try:
        stepFile = 'Scale_Steps.txt'
        rFile = open(stepFile)
        step_info = rFile.readlines()
        rFile.close()
        master_steps = []
        for a in step_info:
            master_steps.append(a.replace('\n', ''))
        return master_steps
    except FileNotFoundError:
        print('Failed to find Scale_Steps.txt')
        x = input("Press any key to quit.")

clean_prog = cleanProgressions()
scale_names = getNames()
scale_steps = getSteps()

class MusicKey:
    def __init__(self, note, names, steps, progs ):

        self.root_note = note.upper()
        # ======= LIST GENERATION FROM FILES =============
        self.scale_names = names # list of names
        self.scale_steps = steps # list steps
        self.clean_progs = progs
        #=================================================
        self.prog_numbers = self.getProgNumbers(self.clean_progs) # list of interger values for chord progressions
        self.steps = self.generate_steps(self.scale_steps) # Tonal Values not Alpha values
        self.scales = self.generate_scales(self.steps, self.scale_names)
        self.chords = self.generate_chord_progressions(self.scales,self.scale_names, self.prog_numbers)
        self.fretboard = self.display_info(self.scales, self.scale_names,self.chords,self.scale_steps, self.clean_progs)

    def getProgNumbers(self,clean_progs):
        # convert from roman numerals - for scale
        roman_to_int = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8}
        prog_numbers = []
        tempt_list = []

        for prog in clean_progs:
            # for every number in progression (prog) - for item in list
            for p in prog:
                z = p.replace('dim', '')
                for x in p:
                    z = z.upper()
                tempt_list.append(roman_to_int[z])
            prog_numbers.append(tempt_list)
            tempt_list = []

        return prog_numbers

    def generate_steps(self, scale_steps)->[str]:
        '''
            CONVERT STEP TEXT TO TONAL VALUES
        '''
        return_steps = []
        step_counter = 0
        temp_step = [0]
        for step in scale_steps:
            for s in step:
                if s == 'w' or s == 'W':
                    step_counter += 2
                    temp_step.append(step_counter)
                if s == 'h' or s == 'H':
                    step_counter += 1
                    temp_step.append(step_counter)
                if s == 'wh' or s == 'WH':
                    step_counter += 3
                    temp_step.append(step_counter)
            return_steps.append(temp_step)
            temp_step = [0]
            step_counter = 0
        return return_steps

    def generate_scales(self, scales, names):
        '''
            Turn tonal value from generate steps to musical Notes
        '''
        chromatic_scale = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#','A']
        temp_scales = []
        loop_scales = []
        temp_index = 0
        starting_note = chromatic_scale.index(self.root_note) # Index of root note

        #return this
        final_scales = {}
        for scale in scales:
            for x in range(len(scale)):
                temp_index = starting_note + scale[x]
                if temp_index > 12:
                    temp_index -= 12
                loop_scales.append(str(chromatic_scale[temp_index]).strip("[ ]").replace("'", ''))
            temp_scales.append(loop_scales)
            loop_scales= []

        #PUSH TO RETURN VALUE - format strings
        for x, scale in enumerate(temp_scales):
            y =  (str(scale).strip("[ ]").replace("'", ''))
            final_scales[names[x]] = y
        #==========================
        return final_scales

    def generate_chord_progressions(self,scales,names, progNumbers):
        current_scale = []
        prog_title = ''
        formatted_scale = ''
        chord_progressions = []
        temp_scale = []


        for name in names:
            for prog in progNumbers:
                prog_title = " ".join(str(p) for p in prog)
                for p in prog:
                    formatted_scale += (scales[name].split()[p-1]).replace(',', '  ')
                temp_scale.append(f'{prog_title:<7} PROGRESSION - {formatted_scale:15}')
                formatted_scale = ''
            chord_progressions.append(temp_scale)
            temp_scale =[]

        return chord_progressions

    def display_info(self, scales, names, chords, scale_steps,clean_progs):
        notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
        # STRINGS
        string_low_E = ['E', 'F', 'F#', 'G', 'G#','A', 'A#', 'B', 'C', 'C#', 'D', 'D#','E']
        string_A = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#','A']
        string_D = ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#','A', 'A#', 'B', 'C', 'C#','D']
        string_G = ['G', 'G#','A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#','G']
        string_B = ['B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#','A', 'A#', 'B']
        string_high_E = ['E', 'F', 'F#', 'G', 'G#','A', 'A#', 'B', 'C', 'C#', 'D', 'D#','E']

        all_strings = [string_low_E, string_A, string_D, string_G, string_B, string_high_E]
        all_strings.reverse()

        print('\t\t\t\t***********************************************************************')
        print(f'\t\t\t\t\t\t\tSCALES AND CHORD PROGRESSIONS IN THE KEY OF {self.root_note}')
        print('\t\t\t\t***********************************************************************')

        def helper_fret_print(scales, names, all_strings, chords, scale_steps,clean_progs):

            spacer = '    '  # 3 spaces left and right
            sharp_spacer = '   '  # 3 space left one space right
            padding = '      '

            def number_frets():
                for z in range(0, 13):
                    if z == 0:
                        print('', end='    -  ')
                    elif 9 <=z <12:
                        print(z, end=' - ')
                    elif z >= 12:
                        print(z, end= ' ')
                    else:
                        print(z, end=' -  ')
                print()

            for x, name  in enumerate(names):
                print('======================================================================================================================')
                print(f'{x +1}. {self.root_note}  {name.upper()} {scales[names[x]]}  {scale_steps[x]}')
                print('==============================================')
                number_frets()
                for string in all_strings:
                    for y, s in enumerate(string):
                        current_scale = scales[names[x]].split(', ')
                        if s in  current_scale:
                            # adjust padding
                            if '#' in s:
                                padding = sharp_spacer
                            else:
                                padding = spacer
                            #=============================
                            if y == 0:
                                print(f'{s}||', end= padding)
                            else:
                                print(s, end= padding)
                        else:
                            padding =  spacer
                            if y == 0 and s in current_scale:
                                print(f'{s}||', end= padding)
                            elif y == 0:
                                print(f'x||', end= padding)
                            else:
                                print('x', end= padding)
                    print()
                number_frets()
                print('==============================================')
                print(f'{self.root_note}  {name.upper()} CHORD PROGRESSIONS')
                print('==============================================')

                for z in range(0, len(chords[x]),2):
                    if z + 1 < len(chords[x]):
                        print(f'|| {chords[x][z]:35}{" - ".join(clean_progs[z]):20}|| {chords[x][z + 1]:35}{" - ".join(clean_progs[z +1]):30}')
                    else:
                        print(f'|| {chords[x][z]:35}{" - ".join(clean_progs[z])}')

                print('\n\n')
        helper_fret_print(scales, names, all_strings, chords, scale_steps,clean_progs)

def menu()->str:

    prompt = input("Enter a note ( A - G ) either natural or sharp (#) ('Q' to quit program):\t")
    return prompt.upper()

def main():
    selection = menu()

    while selection != 'Q':
        try:
            note = MusicKey(selection, scale_names, scale_steps, clean_prog )
            selection = menu()
            del note
        except ValueError:
            selection = menu()

if __name__ == '__main__':
    main()