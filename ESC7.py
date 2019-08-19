# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?
# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
import threading
import smbus
import math
import threading
# esc's gpio number to set

esc_nums = [
    4,
    16,
    20,
    26,
]

# esc's speed lu,ld,ru,rd
speeds = [900 for _ in range(len(esc_nums))]

# left-up, left-down, right-up, right-down
# motor arrangement of quad drone X
# 3 1
# 2 4
direction = {
    "1" : 0,
    "2" : 1,
    "3" : 2,
    "4" : 3,
}

# max or min speed
max_value = 2000
min_value = 900

mutex = threading.Lock()

# code of gyro.py
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

init_x_rotation = 10000
init_y_rotation = 10000

bus = smbus.SMBus(1)  # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68  # via i2cdetect


class PgioPi:
    '''
        GPIO ESC CONTROLL
    '''
    def __init__(self,esc_nums):
        self.pies = [pigpio.pi() for _ in range(len(esc_nums))]
        for idx in range(len(esc_nums)):
            self.pies[idx].set_servo_pulsewidth(esc_nums[idx],0)

    def checkValue(self,num,val,dist,op):
        MAX_DIST = 50
        if op=="+":
            if 1000 <= val+dist <= 2500:
                for i in range(len(esc_nums)):
                    if num==i:
                        continue
                    if abs(val+dist-self.pies[i].get_servo_pulsewidth(esc_nums[i]))>=MAX_DIST:
                        return False
                return True
        else:
            if 1000 <= val-dist <= 2500:
                for i in range(len(esc_nums)):
                    if num==i:
                        continue
                    if abs(val-dist-self.pies[i].get_servo_pulsewidth(esc_nums[i]))>=MAX_DIST:
                        return False
                return True
        return False

    def control_speed(self,scale,op):
        inp = input("control - [ 1, 2, 3, 4, all ]: ")
        inp = list(inp)
        mutex.acquire()
        if ''.join(inp)=="all":
            for idx in range(len(esc_nums)):
                if op=="+":
                    self.pies[idx].set_servo_pulsewidth(esc_nums[idx],self.pies[idx].get_servo_pulsewidth(esc_nums[idx])+scale)
                else:
                    self.pies[idx].set_servo_pulsewidth(esc_nums[idx],self.pies[idx].get_servo_pulsewidth(esc_nums[idx])-scale)
            print("Now speed : ")
            for idx in range(len(esc_nums)):
                print("%d %d"%(idx+1,self.pies[idx].get_servo_pulsewidth(esc_nums[idx])),end=" ")
            print()
        elif set(inp).issubset(set(["1","2","3","4"])):
            for val in inp:
                speed_num = direction[val]
                if op=="+":
                    self.pies[speed_num].set_servo_pulsewidth(esc_nums[speed_num],self.pies[speed_num].get_servo_pulsewidth(esc_nums[speed_num])+scale)
                else:
                    self.pies[speed_num].set_servo_pulsewidth(esc_nums[speed_num],self.pies[speed_num].get_servo_pulsewidth(esc_nums[speed_num])-scale)
                print("Now speed ",val," : %d"%(self.pies[speed_num].get_servo_pulsewidth(esc_nums[speed_num])))
        else:
            print("You select wrong motor!")
        print("==============================================")
        mutex.release()

    def manual_drive(self): #You will use this function to program your ESC if required
        print("You have selected manual option so give a value between 0 and you max value")
        while True:
            inp = input()
            if inp == "s":
                self.stop()
                break
            elif inp == "control":
                self.control()
                break
            elif inp == "arm":
                self.arm()
                break
            else:
                try:
                    inp = int(inp)
                    for idx in range(len(esc_nums)):
                        self.pies[idx].set_servo_pulsewidth(esc_nums[idx],inp)
                except:
                    self.control()
                    break

    def calibrate(self):   #This is the auto calibration procedure of a normal ESC
        for idx in range(len(esc_nums)):
            self.pies[idx].set_servo_pulsewidth(esc_nums[idx],0)
        print("Disconnect the battery and press Enter")
        inp = input()
        if inp == '':
            for idx in range(len(esc_nums)):
                self.pies[idx].set_servo_pulsewidth(esc_nums[idx],max_value)
            print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
            inp = input()
            if inp == '':
                for idx in range(len(esc_nums)):
                    self.pies[idx].set_servo_pulsewidth(esc_nums[idx],min_value)
                print("Wierd eh! Special tone")
                time.sleep(7)
                print("Wait for it ....")
                time.sleep (5)
                print("Im working on it, DONT WORRY JUST WAIT.....")
                for idx in range(len(esc_nums)):
                    self.pies[idx].set_servo_pulsewidth(esc_nums[idx],0)
                time.sleep(2)
                print("Arming ESC now... wait")
                for idx in range(len(esc_nums)):
                    self.pies[idx].set_servo_pulsewidth(esc_nums[idx],min_value)
                time.sleep(1)
                print("See.... uhhhhh")
                self.control() # You can change this to any other function you want

    def control(self):
        print("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
        time.sleep(1)
        #print("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
        th.start()
        for idx in range(len(esc_nums)):
            self.pies[idx].set_servo_pulsewidth(esc_nums[idx],1000)
        #print("Now speed : %d %d %d %d"%(speeds[0],speeds[1],speeds[2],speeds[3]))
        print("Now Speed : ")
        for idx in range(len(esc_nums)):
            print(self.pies[idx].get_servo_pulsewidth(esc_nums[idx]),end=" ")
        print()
        while True:
            inp = input("Controls - [inc] = increase, [dec] = decreaase, [s or stop] = stop, [speed] = see all motor's speed\nInput Control : ")
            if inp=="inc":
                print("You select Increase Speed!")
                spd = input("input speed : ")
                self.control_speed(int(spd),"+")
            elif inp=="dec":
                print("You select Decrease Speed!")
                spd = input("input speed : ")
                self.control_speed(int(spd),"-")
            elif inp == "s" or inp == "stop":
                print("Motors will be stop..")
                self.stop()          #going for the stop function
                break
            elif inp == "speed":
                for idx in range(len(esc_nums)):
                    print("Motor %d's speed : %d"%(idx+1,speeds[idx]))
                print("==============================================")
            elif inp == "manual":
                self.manual_drive()
                break
            elif inp == "arm":
                self.arm()
                break
            else:
                print("WHAT DID I SAID!! Press inc, dec or s[top]!")
                print("==============================================")
        pid = os.popen('cat /var/run/pigpio.pid').read().rstrip()
        os.system("sudo kill -9 %s"%(pid))

    def arm(self): #This is the arming procedure of an ESC
        print("Connect the battery and press Enter")
        inp = input()
        if inp == '':
            for idx in range(len(esc_nums)):
                self.pies[idx].set_servo_pulsewidth(esc_nums[idx],0)
            time.sleep(1)
            for idx in range(len(esc_nums)):
                self.pies[idx].set_servo_pulsewidth(esc_nums[idx],max_value)
            time.sleep(1)
            for idx in range(len(esc_nums)):
                self.pies[idx].set_servo_pulsewidth(esc_nums[idx],min_value)
            time.sleep(1)
            self.control()

    def stop(self): #This will stop every action your Pi is performing for ESC ofcourse.
        mutex.acquire()
        for idx in range(len(esc_nums)):
            self.pies[idx].set_servo_pulsewidth(esc_nums[idx],0)
        for idx in range(len(esc_nums)):
            self.pies[idx].stop()
        th.do_run = False
        mutex.release()
        th.join()

    def balance(self, mode, inc):
        inc_arr = [1, 1, 1, 1]
        if mode == 'w':
            inc_arr[1] *= -1
            inc_arr[3] *= -1
        elif mode == 's':
            inc_arr[0] *= -1
            inc_arr[2] *= -1
        elif mode == 'a':
            inc_arr[1] *= -1
            inc_arr[2] *= -1
        elif mode == 'd':
            inc_arr[0] *= -1
            inc_arr[3] *= -1



    def run_gyro(self):
        d=20
        e=30
        global mutex, esc_nums, init_x_rotation, init_y_rotation
        while True:
            # Aktivieren, um das Modul ansprechen zu koennen
            bus.write_byte_data(address, power_mgmt_1, 0)

            gyroskop_xout = read_word_2c(0x43)
            gyroskop_yout = read_word_2c(0x45)
            gyroskop_zout = read_word_2c(0x47)

            beschleunigung_xout = read_word_2c(0x3b)
            beschleunigung_yout = read_word_2c(0x3d)
            beschleunigung_zout = read_word_2c(0x3f)

            beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
            beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
            beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0

            x_rotation = get_x_rotation(beschleunigung_xout_skaliert,beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
            y_rotation = get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert,beschleunigung_zout_skaliert)

            print("X Rotation: ", x_rotation)
            print("Y Rotation: ", y_rotation)
            time.sleep(1)

            if init_x_rotation == 10000 or init_x_rotation == 10000:
                init_x_rotation = x_rotation
                init_y_rotation = y_rotation

            print("First X Rotation: ", init_x_rotation)
            print("First Y Rotation: ", init_y_rotation)

            x_diff = init_x_rotation - x_rotation
            y_diff = init_y_rotation - y_rotation
            print(x_diff,y_diff)
            mutex.acquire()
            if abs(y_diff) > 10:
                # y axis correcting
                if y_diff > 0:
                    if self.checkValue(0,self.pies[0].get_servo_pulsewidth(esc_nums[0]),d,"+"):
                        self.pies[0].set_servo_pulsewidth(esc_nums[0], self.pies[0].get_servo_pulsewidth(esc_nums[0]) + d)
                    if self.checkValue(1,self.pies[1].get_servo_pulsewidth(esc_nums[1]),e,"-"):
                        self.pies[1].set_servo_pulsewidth(esc_nums[1], self.pies[1].get_servo_pulsewidth(esc_nums[1]) - e)
                    if self.checkValue(2,self.pies[2].get_servo_pulsewidth(esc_nums[2]),e,"-"):
                        self.pies[2].set_servo_pulsewidth(esc_nums[2], self.pies[2].get_servo_pulsewidth(esc_nums[2]) - e)
                    if self.checkValue(3,self.pies[3].get_servo_pulsewidth(esc_nums[3]),d,"+"):
                        self.pies[3].set_servo_pulsewidth(esc_nums[3], self.pies[3].get_servo_pulsewidth(esc_nums[3]) + d)
                else:
                    if self.checkValue(0,self.pies[0].get_servo_pulsewidth(esc_nums[0]),e,"-"):
                        self.pies[0].set_servo_pulsewidth(esc_nums[0], self.pies[0].get_servo_pulsewidth(esc_nums[0]) - e)
                    if self.checkValue(1,self.pies[1].get_servo_pulsewidth(esc_nums[1]),d,"+"):
                        self.pies[1].set_servo_pulsewidth(esc_nums[1], self.pies[1].get_servo_pulsewidth(esc_nums[1]) + d)
                    if self.checkValue(2,self.pies[2].get_servo_pulsewidth(esc_nums[2]),d,"+"):
                        self.pies[2].set_servo_pulsewidth(esc_nums[2], self.pies[2].get_servo_pulsewidth(esc_nums[2]) + d)
                    if self.checkValue(3,self.pies[3].get_servo_pulsewidth(esc_nums[3]),e,"-"):
                        self.pies[3].set_servo_pulsewidth(esc_nums[3], self.pies[3].get_servo_pulsewidth(esc_nums[3]) - e)
            if abs(x_diff) > 10:
                # x axis correcting
                if x_diff > 0:
                    if self.checkValue(0,self.pies[0].get_servo_pulsewidth(esc_nums[0]),e,"-"):
                        self.pies[0].set_servo_pulsewidth(esc_nums[0], self.pies[0].get_servo_pulsewidth(esc_nums[0]) - e)
                    if self.checkValue(1,self.pies[1].get_servo_pulsewidth(esc_nums[1]),d,"+"):
                        self.pies[1].set_servo_pulsewidth(esc_nums[1], self.pies[1].get_servo_pulsewidth(esc_nums[1]) + d)
                    if self.checkValue(2,self.pies[2].get_servo_pulsewidth(esc_nums[2]),e,"-"):
                        self.pies[2].set_servo_pulsewidth(esc_nums[2], self.pies[2].get_servo_pulsewidth(esc_nums[2]) - e)
                    if self.checkValue(3,self.pies[3].get_servo_pulsewidth(esc_nums[3]),d,"+"):
                        self.pies[3].set_servo_pulsewidth(esc_nums[3], self.pies[3].get_servo_pulsewidth(esc_nums[3]) + d)
                else:
                    if self.checkValue(0,self.pies[0].get_servo_pulsewidth(esc_nums[0]),d,"+"):
                        self.pies[0].set_servo_pulsewidth(esc_nums[0], self.pies[0].get_servo_pulsewidth(esc_nums[0]) + d)
                    if self.checkValue(1,self.pies[1].get_servo_pulsewidth(esc_nums[1]),e,"-"):
                        self.pies[1].set_servo_pulsewidth(esc_nums[1], self.pies[1].get_servo_pulsewidth(esc_nums[1]) - e)
                    if self.checkValue(2,self.pies[2].get_servo_pulsewidth(esc_nums[2]),d,"+"):
                        self.pies[2].set_servo_pulsewidth(esc_nums[2], self.pies[2].get_servo_pulsewidth(esc_nums[2]) + d)
                    if self.checkValue(3,self.pies[3].get_servo_pulsewidth(esc_nums[3]),e,"-"):
                        self.pies[3].set_servo_pulsewidth(esc_nums[3], self.pies[3].get_servo_pulsewidth(esc_nums[3]) - e)

            mutex.release()

            print(self.pies[2].get_servo_pulsewidth(esc_nums[2]), self.pies[0].get_servo_pulsewidth(esc_nums[0]))
            print(self.pies[1].get_servo_pulsewidth(esc_nums[1]), self.pies[3].get_servo_pulsewidth(esc_nums[3]))

def read_byte(reg):
    return bus.read_byte_data(address, reg)

def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


if __name__=="__main__":
    pies = PgioPi(esc_nums)
    print("For first time launch, select calibrate")
    print("Type the exact word for the function you want")
    th = threading.Thread(target=pies.run_gyro)
    #This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.
    inp = input("select = c[alibrate] or arm or control or s[top] : ")
    if inp == "manual":
        pies.manual_drive()
    elif inp == "calibrate" or inp == "c":
        pies.calibrate()
    elif inp == "arm":
        pies.arm()
    elif inp == "control":
        pies.control()
    elif inp == "s" or inp == "stop":
        pies.stop()
    else :
        print("Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!")
