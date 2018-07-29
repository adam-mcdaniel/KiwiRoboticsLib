from collections import deque


class Motor:
    def __init__(self):
        self.spin = False

    def start(self):
        self.spin = True


class Handler(deque):
    def __init__(self, *args):
        self += args

    def run(self, method, *args):
        list(map(lambda m: method(m, *args), self))


h = Handler(Motor(), Motor(), Motor())

for motor in h:
    print(motor.spin)

h.run(Motor.start)

for motor in h:
    print(motor.spin)
