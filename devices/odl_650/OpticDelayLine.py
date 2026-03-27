import serial
import time
import re


class OpticDelayLine:
    def __init__(self, port):
        self.MIN_TIME_DELAY = 0
        self.MAX_TIME_DELAY = 342.037
        self.MIN_STEP = 0
        self.MAX_STEP = 330712
        self.TIME_TO_STEP = self.MAX_STEP / self.MAX_TIME_DELAY
        self.ser = serial.Serial(port=port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, timeout=0.1)

    def initialize(self):  # use only after each power up or reset
        self.ser.write('E0\r\n'.encode('ascii'))
        self.ser.read(size=9).decode('ascii')
        self.ser.write('FH\r\n'.encode('ascii'))
        time.sleep(4)
        self.ser.read(size=5).decode('ascii')
        self.ser.write('GR\r\n'.encode('ascii'))  # go to the home position
        time.sleep(4)
        self.ser.read(size=5).decode('ascii')
        self.ser.write('T000.000\r\n'.encode('ascii'))  # set 0 delay time on home position
        self.ser.read(size=18).decode('ascii')

    def disconnect(self):
        self.ser.close()

    def date(self):
        self.ser.write('D?\r\n'.encode('ascii'))
        string = self.ser.read(size=18).decode('ascii')  # 12 bytes with status and 6 bytes for 'Done'
        string = string.split('\r', 2)
        data = string[0]
        status = string[1]
        if status == '\nDone':
            return data
        else:
            print('Error: ' + data)

    def status_query(self):
        self.ser.write('Q?\r\n'.encode('ascii'))
        string = self.ser.read(size=11).decode('ascii')  # 5 bytes with status and 6 bytes for 'Done'
        string = string.split('\r', 2)
        data = string[0]
        status = string[1]
        if status == '\nDone':
            return data
        else:
            print('Error: ' + data)

    def get_time_delay(self):
        self.ser.write('T?\r\n'.encode('ascii'))
        string = self.ser.read(20).decode('ascii')
        string = string.split('\r', 2)
        data = string[0]
        status = string[1]
        if status == '\nDone':
            return (re.findall(r"[-+]?\d*\.\d+|\d+", data))[0]
        else:
            print('Error: ' + data)

    def get_step(self):  # TODO remove function
        self.ser.write('S?\r\n'.encode('ascii'))
        string = self.ser.read(20).decode('ascii')
        string = string.split('\r', 2)
        data = string[0]
        status = string[1]
        if status == '\nDone':
            return (re.findall(r"[-+]?\d*\.\d+|\d+", data))[0]
        else:
            print('Error: ' + data)

    def set_time_delay(self, time_delay):
        if self.MIN_TIME_DELAY <= time_delay <= self.MAX_TIME_DELAY:
            step = round(time_delay * self.TIME_TO_STEP)
            command = 'S' + str(step) + '\r\n'
            self.ser.write(command.encode('ascii'))
            time.sleep(2)
            status = self.ser.read(size=18).decode('ascii')
            if status != 'Done\r\n':
                print('Error' + status)
        else:
            print('Wrong time delay')

    def increase_time_delay(self, increment):
        delta_step = round(increment * self.TIME_TO_STEP)
        current_step = int(self.get_step())
        if self.MIN_STEP <= current_step+delta_step <= self.MAX_STEP:
            command = 'S+' + str(delta_step) + '\r\n'
            self.ser.write(command.encode('ascii'))
            time.sleep(0.3)
            status = self.ser.read(size=18).decode('ascii')
            if status != 'Done\r\n':
                print('Error' + status)
        else:
            print('Range error')

    def decrease_time_delay(self, increment):
        delta_step = round(increment * self.TIME_TO_STEP)
        current_step = int(self.get_step())
        if self.MIN_STEP <= current_step+delta_step <= self.MAX_STEP:
            command = 'S-' + str(delta_step) + '\r\n'
            self.ser.write(command.encode('ascii'))
            time.sleep(0.3)
            status = self.ser.read(size=18).decode('ascii')
            if status != 'Done\r\n':
                print('Error' + status)
        else:
            print('Range error')

    def go_to_home_position(self):
        self.ser.write('GR\r\n'.encode('ascii'))
        time.sleep(2)
        status = self.ser.read(size=7).decode('ascii')
        if status != 'Done\r\n':
            print('Error' + status)

    def go_to_end_position(self):
        self.ser.write('GF\r\n'.encode('ascii'))
        time.sleep(2)
        status = self.ser.read(size=7).decode('ascii')
        if status != 'Done\r\n':
            print('Error' + status)

    def reset(self):
        self.ser.write('RESET\r\n'.encode('ascii'))
        time.sleep(5)
        for i in range(3):
            data = self.ser.readline()
            print(data.decode('ascii'))

"""
def main():
    line = OpticDelayLine()
    line.initialize()
    print(line.get_time_delay())
    # line.increase_time_delay(0.1)
    # print(line.get_time_delay())
    line.disconnect()

if __name__ == '__main__':
    main()
"""