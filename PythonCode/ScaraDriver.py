__version__ = '0.1.0'

import Config as cfg
import os
import time
import math

class Scara(object):
    def __init__(self, serial_device):
        self.serial_device = serial_device
        self.x_error = 0.
        self.y_error = 0.
        self.configure()
        self.update_defaults()

    """ Motion stuff """

    def configure(self):
        command_string = 'C0'
        for k, v in cfg.Feather_Parameter_Chars.items():
            command_string += ' {}{}'.format(k, v)
        self.serial_device.command(command_string)

    def home(self):
        print('TODO implement this plz')

    def zero(self):
        self.serial_device.command('G92 X0 Y0')

    def enable(self):
        self.serial_device.command('M17')

    def disable(self):
        self.serial_device.command('M84')

    def user_zero(self):
        self.disable()
        self.lower_pen()
        _ = input('Press enter when zerod...')
        self.enable()
        self.zero()
        self.raise_pen()
        time.sleep(1)

    def park(self):
        self.serial_device.command('G1 X-30 Y90')
        self.serial_device.command('G1 Y130')

    def unpark(self):
        self.serial_device.command('G1 X-30 Y90')
        self.serial_device.command('G1 X0 Y0')

    def raise_pen(self):
        self.serial_device.command('C2')

    def lower_pen(self):
        self.serial_device.command('C1')

    def update_defaults(self, vel = None, acc = None):
        if acc == None:
            acc = cfg.default_accel_mmps2
        if vel == None:
            vel = cfg.default_vel_mmps
        self.serial_device.command('M201 a{} v{}'.format(acc, vel))

    def absolute_move(self, xtar_mm, ytar_mm, velocity_mmps=None):
        # Calculate move
        command = 'G0 X{} Y{}'.format(xtar_mm, ytar_mm)
        if velocity_mmps is not None:
            command += ' F{}'.format(velocity_mmps * 60)
        self.serial_device.command(command)

    def relative_move(self, xtar_mm, ytar_mm, velocity_mmps=None):
        return self.absolute_move(xpos_mm + xtar_mm, ypos_mm + ytar_mm, velocity_mmps)

    def draw_move(self, move):
        x_center = cfg.board_center_x_mm + (move.x - 1) * cfg.box_size_mm
        y_center = cfg.board_center_y_mm + (1 - move.y) * cfg.box_size_mm
        self.absolute_move(x_center, y_center)
        self.send_gcode('draw_x.g')

    def draw_board(self):
        self.send_gcode('board.g')

    def send_gcode(self, filename):
        with open(os.path.join(cfg.gcode_folder, filename)) as f:
            while(True):
                line = f.readline().strip('\n')
                print(line)
                if not line:
                    break
                
                self.serial_device.command(line)

    @property
    def is_homed(self):
        return True

    @property
    def xpos_mm(self):
        return

    @property
    def ypos_mm(self):
        return


    """ Talking stuff """

    def speak_opener(bot_first):
        if bot_first:
            self.serial_device.command('TODO')
        else:
            self.serial_device.command('TODO')

