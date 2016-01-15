import sys
import struct 
import time

from enum import Enum

fd = sys.stdin

THRESHOLD = 1200
DEBUG = False

TICK = 15 # Sample count
TICK_MINLENGTH = TICK / 2
SEGMENT_MAXLENGTH = TICK * 5.0 + 5.0 * (TICK * 2.0/3.0)

value = False
last_value = False

msg = None

#fd = open("testdata_new_44kHz.dat")

class State(Enum):
    idle                = 0
    preamble_found      = 1
    payload_found       = 2
    reading_sync        = 3

state = State.idle


def tick_comparison(value, factor=1):
    if abs(value - TICK*factor) <= TICK/3:
        return True
    else:
        return False


def signal_recognition():
    samplecount_one     = 0
    samplecount_zero    = 0

    state_signal        = 0

    global value
    global last_value

    while True:
        try:
            last_value = value

            if struct.unpack('h', fd.read(2))[0] > THRESHOLD:
                value = True
            else:
                value = False

        except:
            print("EOF")
            sys.exit(0)

        if state_signal == 0:
            if value and last_value:
                state_signal = 1;

        elif state_signal == 1:
            if not value and not last_value:
                state_signal = 2

                if samplecount_one < TICK_MINLENGTH:
                    raise Exception("tick underflow")
            else:
                samplecount_one += 1

        elif state_signal == 2:
            if value and last_value:
                if DEBUG:
                    print (samplecount_one, samplecount_zero)
                return (samplecount_one, samplecount_zero)
            else:
                samplecount_zero += 1

                if samplecount_zero > SEGMENT_MAXLENGTH:
                    raise Exception("segment overflow")


def reading_preamble():
    try:
        first = signal_recognition()

        if not (tick_comparison(first[0], 1) and tick_comparison(first[1], 1)):
            return False

        second = signal_recognition()

        if not (tick_comparison(second[0], 3) and tick_comparison(second[1], 1)):
            raise Exception("reading preamble failed")

        third = signal_recognition()

        if not (tick_comparison(third[0], 1) and tick_comparison(third[1], 1)):
            raise Exception("reading preamble failed")

        if DEBUG:
            print([first, second, third])
        return True
    except Exception as e:
        if DEBUG:
            raise e # Exception("reading preamble failed")
        else:
            pass


def reading_postamble():

    first = signal_recognition()

    if not (tick_comparison(first[0], 1) and tick_comparison(first[1], 1)):
        raise Exception("reading postamble bit 1 failed")


def parse_message():

    byte = [None] * 9

    for i in range(0, 9):
        signal = signal_recognition()

        if (tick_comparison(signal[0], 2) and tick_comparison(signal[1], 3)):
            byte[i] = 0
        elif (tick_comparison(signal[0], 4) and tick_comparison(signal[1], 1)):
            byte[i] = 1
        else:
            raise Exception("\ninvalid bit pattern in bit {}".format(i))

    parity = 0
    for i in range(0, 8):
        parity += byte[i]

    parity %= 2
    if parity != byte[8]:
        raise Exception("Parity check failed")

    decimal = 0
    for i in range(0, 8):
        decimal += 2**i * byte[i]

    return str(unichr(decimal))


def listen():

    global state
    global msg

    try:
        if state == State.idle:
            if reading_preamble():
                state = State.preamble_found 
                if DEBUG:
                    print("preamble_found")

        elif state == State.preamble_found:
            msg = parse_message()
            if msg is not None:
                state = State.payload_found
                if DEBUG:
                    print("payload_found: {}".format(msg))

        elif state == State.payload_found:
            reading_postamble()
            state = State.idle
            sys.stdout.write(msg)
            sys.stdout.flush()
        else:
            raise Exception("state illegal")

    except Exception as e:
        print(e)
        state = State.idle


if __name__ == "__main__":
    time.sleep(2)
    print("\n\n")

    try:
        while True:
            listen()

    except KeyboardInterrupt:
        # print(state)
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(0)

