# import serial
import random
import time


NUMPIXELS = 300


def minimax(x):
    return min(max(0, x), 255)


def bytize(pos, brt):
    return bytes(str((brt << 8) + pos) + stop, 'ascii')


def lshift_(v, n):
    return (v << n) % 256


def bytize3(pos, r, g, b, stop):
    return bytes(str(lshift_(r, 24) + lshift_(g, 16) + lshift_(b, 8) + pos) + stop, 'ascii')


# serA = serial.Serial('/dev/ttyACM0', 9600)
# serB = serial.Serial('/dev/ttyACM1', 9600)
# run = InstallRun(**{'serA':serA,'serB':serB})

class Cereal():

    def __init__(self, **params):
        self.label = str(params['label'])

    def write(self, msg):
        print(self.label+": ("+str(len(str(msg)))+") "+str(msg))


class InstallRun():

    def __init__(self, **params):
        print("Start")
        self.serA = Cereal(**{'label': 'serA'})  # params['serA']
        self.serB = Cereal(**{'label': 'serB'})  # params['serB']
        self.pointsA = [[0, 0, 0] for i in range(NUMPIXELS)]
        self.pointsB = [[0, 0, 0] for i in range(NUMPIXELS)]
        self.pointsC = [[0, 0, 0] for i in range(NUMPIXELS)]
        self.pointsD = [[0, 0, 0] for i in range(NUMPIXELS)]
        self.clear_points()
        time.sleep(1)
        print("A")
        self.flash_points(32)
        time.sleep(1)
        self.clear_points()
        time.sleep(1)
        print("B")
        self.flash_points(32)
        time.sleep(1)
        self.flash_points(24)
        time.sleep(1)
        print("C")
        self.clear_points()
        time.sleep(1)
        self.flash_points(24)
        time.sleep(1)
        self.flash_points(48)
        time.sleep(1)
        self.clear_points()
        time.sleep(1)
        self.flash_points(132)

    def clear_points(self):
        for i in range(NUMPIXELS):
            self.pointsA[i] = [0, 0, 0]
            self.pointsB[i] = [0, 0, 0]
            self.pointsC[i] = [0, 0, 0]
        self.transmit()

    def flash_points(self, b):
        b_ = minimax(b)
        for i in range(NUMPIXELS):
            self.pointsA[i] = [b_, b_, b_]
            self.pointsB[i] = [b_, b_, b_]
            self.pointsC[i] = [b_, b_, b_]
        self.transmit()

    def transmit(self):
        for i in range(NUMPIXELS):
            self.serA.write(
                bytize3(i, self.pointsA[i][0], self.pointsA[i][1], self.pointsA[i][2], "x"))
            self.serA.write(
                bytize3(i, self.pointsB[i][0], self.pointsB[i][1], self.pointsB[i][2], "y"))
            self.serB.write(
                bytize3(i, self.pointsC[i][0], self.pointsC[i][1], self.pointsC[i][2], "x"))
            self.serB.write(
                bytize3(i, self.pointsD[i][0], self.pointsD[i][1], self.pointsD[i][2], "y"))
            time.sleep(0.01)

    # def relay_points(self, pts):
    # """
    # """

    # for idx, pt in enumerate(pts_):
    #         # print("x")
    #         # print(idx)
    #         # print(pt)
    #         # print(pts_[int(idx/9)][idx % 5])
    #     self.ser.write(bytize(idx, pt))

    # def run_steps(self, n=1, delay=1.0):
    #     for i in range(n):
    #         self.current_mode = random.randint(0, 3)
    #         chosen_mode = self.modes[self.current_mode]
    #         num_iters = 5  # random.randint(0, 99)
    #         for j in range(num_iters):
    #             if len(chosen_mode) > 1:
    #                 print("---->")
    #                 print(chosen_mode[1])
    #                 if self.current_mode > 2 and self.current_mode < 7:
    #                     self.gs.grid_apply_f(
    #                         grid_setone, kwargs={'val': 127, 'r': 0, 'c': 0})
    #                 newgrid = self.gs.grid_apply_f(
    #                     chosen_mode[0], kwargs=chosen_mode[1])
    #             else:
    #                 newgrid = self.gs.grid_apply_f(chosen_mode[0])
    #             # self.state_log = self.state_log + [[chosen_mode[0], self.gs.grid]]
    #             # send grid_diffs
    #             print("--------")
    #             self.relay_points(newgrid)                        # SER
    #             time.sleep(delay)

    #     return n
