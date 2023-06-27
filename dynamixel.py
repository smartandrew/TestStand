import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
from dynamixel_sdk import * # Uses Dynamixel SDK library

# Control table address
ADDR_OPERATING_MODE         = 11
ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132
ADDR_GOAL_VELOCITY          = 104
ADDR_PRESENT_VELOCITY       = 128
ADDR_GOAL_CURRENT           = 102
ADDR_PRESENT_CURRENT        = 126
ADDR_GOAL_PWM               = 100
ADDR_PRESENT_PWM            = 124
MINIMUM_POSITION_VALUE      = 0         # Refer to the Minimum Position Limit of product eManual
MAXIMUM_POSITION_VALUE      = 4095      # Refer to the Maximum Position Limit of product eManual
MINIMUM_VELOCITY_VALUE      = -260
MAXIMUM_VELOCITY_VALUE      = 260
MINIMUM_CURRENT_VALUE       = -1188
MAXIMUM_CURRENT_VALUE       = 1188
MINIMUM_PWM_VALUE           = -885
MAXIMUM_PWM_VALUE           = 885
BAUDRATE                    = 57600

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Use the actual port assigned to the U2D2.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = '/dev/ttyUSB0'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

class dynamixel(object):
    def __init__(self, ID, OperatingMode = "Position"):
        self.ID = ID
        self.setMode(OperatingMode)

    def getID(self):
        return self.ID

    def setMode(self, OperatingMode):        
        if OperatingMode == "Current":
            OpMode = 0
        elif OperatingMode == "Velocity":
            OpMode = 1
        elif OperatingMode == "Position":
            OpMode = 3
        elif OperatingMode == "ExtendedPosition":
            OpMode = 4
        elif OperatingMode == "CurrentBasedPosition":
            OpMode = 5
        elif OperatingMode == "PWM":
            OpMode = 16
        else:
            print("Operating Mode has Defualted to 'Position' \n Please input one of the following: \n Current, \n Velocity, \n Position, \n ExtendedPosition, \n CurrentBasedPosition, \n PWM")
                    
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_OPERATING_MODE, OpMode)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            self.OperatingMode = OperatingMode
            print("Mode is now OperatingMode", self.OperatingMode)

    def EnableTorque(self):
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")
    
    def DisableTorque(self):
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
            print("Dynamixel has been disconnected")

    def setPosition(self, dxl_goal_position):
        if (MINIMUM_POSITION_VALUE <= dxl_goal_position) and (dxl_goal_position <= MAXIMUM_POSITION_VALUE):
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_GOAL_POSITION, dxl_goal_position)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Position must be in the range of ", MINIMUM_POSITION_VALUE, "-", MAXIMUM_POSITION_VALUE)

    def getPosition(self):
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, self.ID, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] PresPos:%03d" % (self.ID, dxl_present_position))

    def setVelocity(self, dxl_goal_velocity):
        if (MINIMUM_VELOCITY_VALUE <= dxl_goal_velocity) and (dxl_goal_velocity <= MAXIMUM_VELOCITY_VALUE):
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_GOAL_VELOCITY, dxl_goal_velocity)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Position must be in the range of ", MINIMUM_VELOCITY_VALUE, "-", MAXIMUM_VELOCITY_VALUE)

    def getVelocity(self):
        dxl_present_velocity, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, self.ID, ADDR_PRESENT_VELOCITY)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] PresVel:%03d" % (self.ID, dxl_present_velocity))

    def setCurrent(self, dxl_goal_current):
        if (MINIMUM_CURRENT_VALUE <= dxl_goal_current) and (dxl_goal_current <= MAXIMUM_CURRENT_VALUE):
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, self.ID, ADDR_GOAL_CURRENT, dxl_goal_current)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Position must be in the range of ", MINIMUM_CURRENT_VALUE, "-", MAXIMUM_CURRENT_VALUE)
    
    def getCurrent(self):
        dxl_present_current, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, self.ID, ADDR_PRESENT_CURRENT)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] PresCur:%03d" % (self.ID, dxl_present_current))

    def setPWM(self, dxl_goal_PWM):
        if (MINIMUM_PWM_VALUE <= dxl_goal_PWM) and (dxl_goal_PWM <= MAXIMUM_PWM_VALUE):
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, self.ID, ADDR_GOAL_PWM, dxl_goal_PWM)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Position must be in the range of ", MINIMUM_PWM_VALUE, "-", MAXIMUM_PWM_VALUE)
    
    def getPWM(self):
        dxl_present_PWM, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, self.ID, ADDR_PRESENT_PWM)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] PresPMW:%03d" % (self.ID, dxl_present_PWM))