from . import i2c_7
from . import gpio_9
import openhtf as htf
from openhtf.plugs.user_input import UserInput

def run_all_tests():
    print("CT Tests")
    UserInput.prompt("Press Enter to start CT-7 (i2c) test")
    i2c_7.setup()
    i2c_7.run_test()
    i2c_7.teardown()

    UserInput.prompt("Press Enter to start CT-9 (gpio) test")
    gpio_9.setup()
    gpio_9.run_test()
    gpio_9.teardown()
    pass