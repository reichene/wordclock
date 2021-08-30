#!/usr/bin/python3

# # This program is the first step into python
####################
# Interrupt from keyboard
# https://stackoverflow.com/questions/5114292/break-interrupt-a-time-sleep-in-python

import time
import board
import neopixel


class Wordclock_Words:
    def __init__(self):
        self.hour_words = set()
        self.minute_words = set()
        self.other_words = set()



class Wordclock_Time:
    def __init__(self, old_time):
        self.old_time = old_time

        timestamp = time.localtime()
  
        self.hours = int(time.strftime("%I", timestamp))
        self.seconds = int(time.strftime("%S", timestamp))
        self.minutes = int(time.strftime("%M", timestamp))

        multiplicator_modulo = self.minutes // Wordclock_Runner.modulo_intervall
        self.minutes_modulo = multiplicator_modulo * Wordclock_Runner.modulo_intervall
        self.time = str(self.hours) + str(self.minutes_modulo)

        # clear reference to old Wordclock_Time Instance, otherwise memory keeps objects till
        # clock will be terminated
        if self.old_time != None:
            del self.old_time.old_time




class Wordclock_TimeWordsMapperInterface:
    def define_words(self, hours: int, minutes: int) -> Wordclock_Words:
        """Load in the file for extracting text."""
        pass


class Wordclock_LEDMatrixInterface:
    def display_LED_pin_ids(self, pin_ids: []):
        pass

class Wordclock_LEDMatrixMapperInterface:
    def __init__(self, mapper: Wordclock_TimeWordsMapperInterface, board: Wordclock_LEDMatrixInterface):
        self.mapper = mapper
        self.board = board

    def display_words(self, words: Wordclock_Words):
        pass



class Wordclock_LEDMatrix_10x11_German_Board(Wordclock_LEDMatrixInterface):
    # The number of NeoPixel
    num_pixels = 114
    pixels = []

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    def __init__(self):
        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        pixel_pin = board.D18

        self.pixels = neopixel.NeoPixel(
            pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
        )

    
    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)
        
    
    def display_LED_pin_ids(self, pin_ids: []):

        self.rainbow_cycle(0.001)

        self.pixels.fill(0)
        self.pixels.show()
        
        for i in range(self.num_pixels):
            for arr in pin_ids:
                moep = i + 1
                if  moep in arr:
                    self.pixels[i] = (255,255,255)              


        self.pixels[1] = self.pixels[0] = (255,255,255)
        self.pixels[113] = self.pixels[112] = (255,255,255) 
        self.pixels.show()

      

class Wordclock_LEDMatrix_10x11_German(Wordclock_LEDMatrixMapperInterface):

    # constants words
    ES = "ES"
    IST = "IST"
    UHR = "UHR"
    EIN = "EIN"
    EINS = "EINS"
    ZWEI = "ZWEI"
    DREI = "DREI"
    VIER = "VIER"
    FUENF = "FÜNF"
    SECHS = "SECHS"
    SIEBEN = "SIEBEN"
    ACHT = "ACHT"
    NEUN = "NEUN"
    ZEHN = "ZEHN"
    ELF = "ELF"
    ZWOELF = "ZWÖLF"
    ZWANZIG = "ZWANZIG"
    VIERTEL = "VIERTEL"
    DREIVIERTEL = "DREIVIERTEL"
    HALB = "HALB"
    VOR = "VOR"
    NACH = "NACH"

    def __init__(self, mapper: Wordclock_TimeWordsMapperInterface, board: Wordclock_LEDMatrixInterface):
        Wordclock_LEDMatrixMapperInterface.__init__(self, mapper, board)

        self.matrix_raw = {
            "ESKISTLFÜNF": {Wordclock_LEDMatrix_10x11_German.ES: {"other": True},
                            Wordclock_LEDMatrix_10x11_German.IST: {"other": True},
                            Wordclock_LEDMatrix_10x11_German.FUENF: {"minutes": True}},
            "ZEHNZWANZIG": {Wordclock_LEDMatrix_10x11_German.ZEHN: {"minutes": True},
                            Wordclock_LEDMatrix_10x11_German.ZWANZIG: {"minutes": True}},
            "DREIVIERTEL": {Wordclock_LEDMatrix_10x11_German.DREIVIERTEL: {"minutes": True},
                            Wordclock_LEDMatrix_10x11_German.DREI: {"minutes": True},
                            Wordclock_LEDMatrix_10x11_German.VIER: {"minutes": True},
                            Wordclock_LEDMatrix_10x11_German.VIERTEL: {"minutes": True}},
            "TGNACHVORJM": {Wordclock_LEDMatrix_10x11_German.NACH: {"minutes": True},
                            Wordclock_LEDMatrix_10x11_German.VOR: {"minutes": True}},
            "HALBQZWÖLFP": {Wordclock_LEDMatrix_10x11_German.HALB: {"minutes": True},
                            Wordclock_LEDMatrix_10x11_German.ZWOELF: {"hours": True}},
            "ZWEINSIEBEN": {Wordclock_LEDMatrix_10x11_German.ZWEI: {"hours": True}, Wordclock_LEDMatrix_10x11_German.EIN: {"hours": True},
                            Wordclock_LEDMatrix_10x11_German.EINS: {"hours": True}, Wordclock_LEDMatrix_10x11_German.SIEBEN: {"hours": True}},
            "KDREIRHFÜNF": {Wordclock_LEDMatrix_10x11_German.DREI: {"hours": True},
                            Wordclock_LEDMatrix_10x11_German.FUENF: {"hours": True}},
            "ELFNEUNVIER": {Wordclock_LEDMatrix_10x11_German.ELF: {"hours": True},
                            Wordclock_LEDMatrix_10x11_German.NEUN: {"hours": True}, Wordclock_LEDMatrix_10x11_German.VIER: {"hours": True}},
            "WACHTZEHNRS": {Wordclock_LEDMatrix_10x11_German.ACHT: {"hours": True}, Wordclock_LEDMatrix_10x11_German.ZEHN: {"hours": True}},
            "BSECHSFMUHR": {Wordclock_LEDMatrix_10x11_German.SECHS: {"hours": True}, Wordclock_LEDMatrix_10x11_German.UHR: {"other": True}},
        }

        self.build_word_letter_matrix(False, 2)

    def display_words(self, words):
        #print(words.minute_words)
        #print(words.hour_words)
        #print(words.other_words)

        self.board.display_LED_pin_ids(self.get_letter_ids(words))


    def build_word_letter_matrix(self, reverse_soldering, amnt_none_letter_led):
        total_rows = len(self.matrix_raw)  # led stripes
        matrix = []



        for row_index in range(len(self.matrix_raw)):

            row_text = list(self.matrix_raw.keys())[row_index]
            single_row = self.matrix_raw.get(row_text)

            # ROW LEVEL
            #################################################

            for word, word_properties in single_row.items():
                index_start_word = row_text.find(word)
            #ROW#######################################
                row = row_index + 1

            #COLUMN#####################################
                word_dict = dict()
                word_dict = word_properties
                word_dict["word"] = word

                # build letter matrix for word
                for letter_index in range(len(word)):
                    column_index = index_start_word + 1 + letter_index

                 #Y-Stripe - SOLDERING
                 ########################
                    is_Y_soldering_bottem = True
                  # cross soldering
                  # E = 10 + B = 1 instead of E = 1 and B = 10
                    reversed_row = total_rows - row_index
                    moep = 0
                    if ((column_index % 2 == 0 and is_Y_soldering_bottem == False) or
                            (not (column_index % 2 == 0) and is_Y_soldering_bottem == True)):
                        moep = reversed_row
                    else:
                        moep = row

                    y_unique_pin_id = 0
                    if (column_index - 1) > 0:
                        y_unique_pin_id = (column_index - 1) * total_rows

                    y_unique_pin_id += moep

                  #X-Stripe - SOLDERING
                  ########################
                    # total letters = word_length
                    # cross soldering
                    # moep_x = 0
                    #is_X_soldering_righthand = True
                    # if ((row % 2 == 0 and is_X_soldering_righthand == False) or
                    #         (not (row % 2 == 0) and is_X_soldering_righthand == True)):
                    #     moep_x = len(row_text) - (index_start_word + letter_index)
                    # else:
                    #     moep_x = column_index

                    # x_unique_pin_id = 0
                    # if (row - 1) > 0:
                    #     x_unique_pin_id = (row - 1) * len(row_text)

                    # x_unique_pin_id += moep_x

                    ################
                    # revert stripe
                    ################
                    if reverse_soldering == True:
                        y_unique_pin_id = self.revert_soldering(
                            (len(row_text) * total_rows), y_unique_pin_id)

                    ###############
                    # Add letters to table
                    ###############

                    letter_dict = dict()
                    letter_dict = {
                        "letter": word[letter_index],
                        "letter_id": ( y_unique_pin_id + amnt_none_letter_led ),
                        "row": row,
                        "column": column_index}

                    if "letters" not in word_dict:
                        word_dict["letters"] = []

                    word_dict["letters"].append(letter_dict)

                matrix.append(word_dict)
        self.matrixLED = matrix

    def revert_soldering(self, total_number_letters, letter_id):
        i = 1
        mumu = []
        while i < (total_number_letters + 1):
            mumu.append(i)
            i += 1

        reversed_list = []
        for i in reversed(mumu):
            reversed_list.append(i)

        return reversed_list[mumu.index(letter_id)]

    def get_letter_ids(self, words: Wordclock_Words):
        letter_ids = []
        letter_ids.append(self.find_letters_in_word(
            "minutes", words.minute_words))
        letter_ids.append(self.find_letters_in_word("hours", words.hour_words))
        letter_ids.append(self.find_letters_in_word(
            "other", words.other_words))

        return letter_ids

    def find_letters_in_word(self, word_type, words):
        letter_ids = []
        for wo in words:
            for word3 in self.matrixLED:
                if word3["word"] != wo:
                    continue
                if word_type in word3:
                    for letter in word3["letters"]:
                        letter_ids.append(letter["letter_id"])
        return letter_ids





class Wordclock_TimeWordsMapper_StandardGerman(Wordclock_TimeWordsMapperInterface):

    def define_words(self, hours: int, minutes: int) -> Wordclock_Words:
        words = Wordclock_Words()

       # print("the time", hours, minutes)

        # constants hours words
        hours_dictionary = {
            1: Wordclock_LEDMatrix_10x11_German.EINS,
            2: Wordclock_LEDMatrix_10x11_German.ZWEI,
            3: Wordclock_LEDMatrix_10x11_German.DREI,
            4: Wordclock_LEDMatrix_10x11_German.VIER,
            5: Wordclock_LEDMatrix_10x11_German.FUENF,
            6: Wordclock_LEDMatrix_10x11_German.SECHS,
            7: Wordclock_LEDMatrix_10x11_German.SIEBEN,
            8: Wordclock_LEDMatrix_10x11_German.ACHT,
            9: Wordclock_LEDMatrix_10x11_German.NEUN,
            10: Wordclock_LEDMatrix_10x11_German.ZEHN,
            11: Wordclock_LEDMatrix_10x11_German.ELF,
            12: Wordclock_LEDMatrix_10x11_German.ZWOELF
        }
        #####################################
        # DEFINE OTHER WORD OUTPUT
        #####################################
        words.other_words.add(Wordclock_LEDMatrix_10x11_German.ES)
        words.other_words.add(Wordclock_LEDMatrix_10x11_German.IST)

        if minutes == 0:
            words.other_words.add(Wordclock_LEDMatrix_10x11_German.UHR)

        #####################################
        # DEFINE HOURS WORD OUTPUT
        #####################################

        # exactly 1 oclock = EIN X EINS
        if minutes == 0 and hours == 1:
            words.hour_words.add(Wordclock_LEDMatrix_10x11_German.EIN)

        # next hour ... minutes before half <next hour> = 25
        elif minutes > 24:
            if hours < 12:
                words.hour_words.add(hours_dictionary.get(hours+1))
            else:
                words.hour_words.add(hours_dictionary.get(1))

        # current hour
        else:
            words.hour_words.add(hours_dictionary.get(hours))

        #####################################
        # DEFINE MINUTES WORD OUTPUT
        #####################################
        # 5, 55, 35, 25 => FÜNF
        if minutes in {5, 55, 35, 25}:
            words.minute_words.add(Wordclock_LEDMatrix_10x11_German.FUENF)

        # 10, 50 => ZEHN
        if minutes in {10, 50}:
            words.minute_words.add(Wordclock_LEDMatrix_10x11_German.ZEHN)

        # 20, 40 => ZWANZIG
        if minutes in {20, 40}:
            words.minute_words.add(Wordclock_LEDMatrix_10x11_German.ZWANZIG)

        # 15, 45 => VIERTEL
        if minutes in {15, 45}:
            words.minute_words.add(Wordclock_LEDMatrix_10x11_German.VIERTEL)

            # <Minutes> < 30 && <Minutes> != 25 => NACH
        if (minutes < 30 and minutes != 25 and minutes != 0) or minutes == 35:
            words.minute_words.add(Wordclock_LEDMatrix_10x11_German.NACH)

        # <Minutes> > 30 && <Minutes> != 35 => VOR
        if (minutes > 30 and minutes != 35 and minutes != 0) or minutes == 25:
            words.minute_words.add(Wordclock_LEDMatrix_10x11_German.VOR)

        # 30 => HALB
        if minutes in {30, 35, 25}:
            words.minute_words.add(Wordclock_LEDMatrix_10x11_German.HALB)

        return words


class Wordclock_Runner:
    modulo_intervall = 5
    hour_in_seconds = 60

    @staticmethod
    def start():

        # Todo
        # - Interrupt from IO
        # = Replace "While True"

        runner = Wordclock_Runner(Wordclock_LEDMatrix_10x11_German(
            Wordclock_TimeWordsMapper_StandardGerman(), 
            Wordclock_LEDMatrix_10x11_German_Board()))

        while True:
            runner.read_time()

            if runner.is_trigger_fired() == True:
                runner.handle_change()
                runner.make_runner_sleep()

    def __init__(self, matrixLED: Wordclock_LEDMatrixInterface):
        self.time = None
        self.matrixLED = matrixLED

    def is_trigger_fired(self):
        if self.time.old_time != None:
            if self.time.old_time.time != self.time.time:
                return True
        else:
            return True

    def read_time(self):
        self.time = Wordclock_Time(self.time)

    def handle_change(self):

        if self.time.old_time != None:
            # Clock is running
            print("change time", self.time.old_time.time, self.time.time, self.time.minutes_modulo)
        else:
            # Initial run: clock was restarted
            print("restart", self.time.time, self.time.minutes_modulo)

        # control LED matrix
        #################################
        self.matrixLED.display_words(self.matrixLED.mapper.define_words(
            self.time.hours, self.time.minutes_modulo))

    def make_runner_sleep(self):
        # load reduction:  make clock sleep while no changes need to be triggered
        if (self.time.minutes % Wordclock_Runner.modulo_intervall) == 0 and self.time.seconds == 0:
            # print("sleep")
            time.sleep(Wordclock_Runner.hour_in_seconds *
                       Wordclock_Runner.modulo_intervall)









