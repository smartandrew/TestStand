from dynamixel import dynamixel
import time

print("beep boop")

motor1 = dynamixel(ID = 1, op = 0)
motor2 = dynamixel(ID = 2, op = "Velocity")
motor3 = dynamixel(ID = 3, op = 16)

print(motor1.ID)
print(motor1.getID())
print(motor1.OperatingMode)
print(motor1.getOperatingMode())

motor1.EnableTorque()
motor2.EnableTorque()
motor3.EnableTorque()

motor1.getMode()
motor2.getMode()
motor3.getMode()

motor1.setCurrent(100)
motor2.setVelocity(50)
motor3.setPWM(800)

time.sleep(15)

motor1.setMode("Position")
motor2.setMode("CurrentBasedPosition")
motor3.setMode("ExtendedPosition")

motor1.getMode()
motor2.getMode()
motor3.getMode()

motor1.setPosition(0)
motor2.setPosition(0)
motor3.setPosition(0)

time.sleep(15)

motor2.setPosAndCurrent(40, 5000)

time.sleep(10)

motor1.getPosition()
motor1.getCurrent()
motor1.getVelocity()
motor1.getPWM()

print("beep boop")

motor1.DisableTorque()
motor2.DisableTorque()
motor3.DisableTorque()