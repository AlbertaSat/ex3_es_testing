# Goal of this test is to verify the I2C interface works and to verify stability of the I2C bus.
# Connected to test device 24AA00T-I/OT EEPROM
# Test should create data to write to EEPROM, get a checksum of the data, write the data to the EEPROM, read the data back, and verify the checksum matches.
# The test runs on the test PC and will run commands using SSH to the DUT to perform the I2C operations using i2c-tools.
# Should use SSH plug for openhtf in util/ssh_plug.py
# There are a number of busses under /dev/*_i2c
import openhtf as htf
from openhtf.plugs.user_input import UserInput
from util.ssh_plug import SSHPlug
import hashlib


test_number = 7
test_description = "i2c"
# busses = {
#    name: number,
# }
busses = {}

# prepare dut for test
@htf.plug(ssh=SSHPlug)
def setup(ssh):
    print(f"{test_description}_{test_number} setup")
    # identify all busses from symlink /dev/*_i2c and add to busses list
    out, err = ssh.run_command("ls -l /dev/*_i2c")
    # parse output to get bus numbers
    for line in out.splitlines():
        if "/dev/i2c-" in line:
            bus_number = line.split("/dev/i2c-")[1].split()[0]
            bus_name = line.split("/dev/")[1].split()[0]
            busses[bus_name] = bus_number
    print(f"Identified I2C busses: {busses}")

    # Put i2c_test binary on DUT
    ssh.send_file("Q7/CT/i2c_7/i2c_test", "/tmp/i2c_test")
    ssh.run_command("chmod +x /tmp/i2c_test")
    pass

# do post test stuff
@htf.plug(ssh=SSHPlug)
def teardown(ssh):
    print(f"{test_description}_{test_number} teardown")
    pass

@htf.plug(ssh=SSHPlug, user_input=UserInput)
def run_test(ssh):
    print(f"{test_description}_{test_number} test")
    # For each bus, run i2c_test binary and verify it can read/write to the EEPROM correctly
    # Binary takes bus number as argument and performs read/write test, returns 0 on success and 1 on failure
    bus_fails = []
    for bus_name, bus_number in busses.items():
        # run I2C test 10 times on each bus to verify stability
        run_fails = 0
        for i in range(10):
            print(f"[{i+1}/10] Testing I2C bus {bus_name} with bus number {bus_number}")
            out, err = ssh.run_command(f"/tmp/i2c_test {bus_number}")
            if err:
                print(f"Error running i2c_test on bus {bus_name}: {err}")
                run_fails += 1
            if out.strip() == "0":
                print(f"I2C test passed on bus {bus_name}")
            else:
                print(f"I2C test failed on bus {bus_name} with output: {out.strip()}")
                run_fails += 1
        if run_fails > 0:
            bus_fails.append(bus_name)

    if bus_fails:
        print(f"I2C tests failed on the following buses: {', '.join(bus_fails)}")
        return htf.PhaseResult.FAIL_AND_CONTINUE
    else:
        print("I2C tests passed for all buses")
    pass