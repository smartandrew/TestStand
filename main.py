from dynamixel import dynamixel

print("beep boop")

wheelFrontLeft1 = dynamixel(ID = 1)
wheelFrontLeft2 = dynamixel(ID = 2)
wheelFrontLeft3 = dynamixel(ID = 3)


print("beep boop")

print(wheelFrontLeft1.getID())
print(wheelFrontLeft1.getPosition())
wheelFrontLeft1.EnableTorque()

print(wheelFrontLeft2.getID())
print(wheelFrontLeft2.getPosition())
wheelFrontLeft2.EnableTorque()

print(wheelFrontLeft3.getID())
print(wheelFrontLeft3.getPosition())
wheelFrontLeft3.EnableTorque()

wheelFrontLeft1.setPosition(2048)
wheelFrontLeft2.setPosition(2048)
wheelFrontLeft3.setPosition(2048)

print("beep boop")