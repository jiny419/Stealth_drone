import smbus
import math
import time

# bus = smbus.SMBus(0) fuer Revision 1
bus = smbus.SMBus(1)

# via i2cdetect
address = 0x68

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

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

def start():
    res = ""
    # Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)

    res += "Gyroskop<br/>"
    res += "--------<br/>"

    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)

    res += "gyroskop_xout: "+("%5d" % gyroskop_xout)+" skaliert: "+str(gyroskop_xout / 131)+"<br/>"
    res += "gyroskop_yout: "+("%5d" % gyroskop_yout)+" skaliert: "+str(gyroskop_yout / 131)+"<br/>"
    res += "gyroskop_zout: "+("%5d" % gyroskop_zout)+" skaliert: "+str(gyroskop_zout / 131)+"<br/>"

    res += "<br/>Beschleunigungssensor<br/>"
    res += "---------------------<br/>"

    beschleunigung_xout = read_word_2c(0x3b)
    beschleunigung_yout = read_word_2c(0x3d)
    beschleunigung_zout = read_word_2c(0x3f)

    beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
    beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
    beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0

    res += "beschleunigung_xout: "+("%6d" % beschleunigung_xout)+" skaliert: "+str(beschleunigung_xout_skaliert)+"<br/>"
    res += "beschleunigung_yout: "+("%6d" % beschleunigung_yout)+" skaliert: "+str(beschleunigung_yout_skaliert)+"<br/>"
    res += "beschleunigung_zout: "+("%6d" % beschleunigung_zout)+" skaliert: "+str(beschleunigung_zout_skaliert)+"<br/>"

    x_rotation = get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
    y_rotation = get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)

    res += "X Rotation: "+str(x_rotation)+"<br/>"
    res += "Y Rotation: "+str(y_rotation)+"<br/>"

    return res
