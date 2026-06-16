import openhtf as htf
from openhtf.plugs.user_input import UserInput  
from util.ssh_plug import SSHPlug

test_number = 9
test_description = "gpio"

# GPIOS:
# Daedalus Name	Vivado EMIO GPIO #	SW GPIO #	Zybo Package Pin	Zybo Pmod	Protocol	Internal Pullup/pulldown
# UHF_UART_RX	0	54	MIO-10	JF - 2	Digital Input	No
# SBAND_TR	1	55	W16	JE - 2	Digital Input	No
# STACK_SBAND_n_RESET	2	56	J15	JE - 3	Digital Output	No
# Q7_DFGMKnifeEN	3	57	H15	JE - 4	Digital Output	Pulldown
# Q7_StarboardKnifeEN	4	58	V13	JE - 7	Digital Output	Pulldown
# SwitchDeployable_S	5	59	U17	JE - 8	Digital Input	No
# SwitchDeployable_P	6	60	T17	JE - 9	Digital Input	No
# Starboard_IR_Sens	7	61	Y17	JE - 10	Digital Input	Pulldown
# SP_nAlert	8	62	N15	JA - 1	Digital Input	No
# SP_SHDN	9	63	L14	JA - 2	Digital Output	No
# GPS_nAlert	10	64	K16	JA - 3	Digital Input	No
# GPS_SHDN	11	65	K14	JA - 4	Digital Output	No
# Port_IR_Sens	12	66	N16	JA - 7	Digital Input	Pulldown
# STACK_SBAND_STX_EN	13	67	L15	JA - 8	Digital Output	Pulldown
# DFGM_IR_Sens	14	68	J16	JA - 9	Digital Input	Pulldown
# TS_Alert	15	69	J14	JA - 10	Digital Input	No
# TS_RS	16	70	V15	JC - 1	Digital Output	Pulldown
# GPS_RSTN	17	71	W15	JC - 2	Digital Output	Pullup
# HUB_RESET_L	18	72	T11	JC - 3	Digital Output	Pullup
# HUB_HS_IND	19	73	T10	JC - 4	Digital IO	Pulldown
# Q7_PortKnifeEN	22	76	T12	JC - 9	Digital Output	Pulldown
# HUB_SETUP_IND	23	77	U12	JC - 10	Digital Input	Pulldown


GPIOS = {
    # "name": "[up|down|none]",
    "UHF_UART_RX": "none",
    "SBAND_TR": "none",
    "STACK_SBAND_n_RESET": "none",
    "Q7_DFGMKnifeEN": "down",
    "Q7_StarboardKnifeEN": "down",
    "SwitchDeployable_S": "none",
    "SwitchDeployable_P": "none",
    "Starboard_IR_Sens": "down",
    "SP_nAlert": "none",
    "SP_SHDN": "none",
    "GPS_nAlert": "none",
    "GPS_SHDN": "none",
    "Port_IR_Sens": "down",
    "STACK_SBAND_STX_EN": "down",
    "DFGM_IR_Sens": "down",
    "TS_Alert": "none",
    "TS_RS": "down",
    "GPS_RSTN": "up",
    "HUB_RESET_L": "up",    
    "HUB_HS_IND": "down",
    "Q7_PortKnifeEN": "down",
    "HUB_SETUP_IND": "down",
}

# prepare dut for test
def setup():
    print(f"{test_description}_{test_number} setup")
    pass

# do post test stuff
def teardown():
    print(f"{test_description}_{test_number} teardown")
    pass

@htf.plug(ssh=SSHPlug, user_input=UserInput)
def run_test():
    print(f"{test_description}_{test_number} test")

    failed_gpios = []

    # For each GPIO
    for gpio, pull in GPIOS.items():
        # gpioset $(gpiofind <gpio_pin>)=0
        ssh.run_command(f"gpioset $(gpiofind {gpio})=0")
        # User prompt if DMM matches expected value
        prompt = user_input.prompt(f"Please verify that GPIO {gpio} is LOW on the DMM and then type y for yes or n for no and then press Enter to continue.")
        if prompt.lower() != "y":
            print(f"GPIO {gpio} LOW test failed, user indicated value was not LOW")
            failed_gpios.append(gpio)
        else:
            print(f"GPIO {gpio} LOW test passed, user indicated value was LOW") 
        # gpioset $(gpiofind <gpio_pin>)=1
        ssh.run_command(f"gpioset $(gpiofind {gpio})=1")
        # User prompt if DMM matches expected value
        prompt = user_input.prompt(f"Please verify that GPIO {gpio} is HIGH on the DMM and then type y for yes or n for no and then press Enter to continue.")
        if prompt.lower() != "y":
            print(f"GPIO {gpio} HIGH test failed, user indicated value was not HIGH")
            failed_gpios.append(gpio)
        else:
            print(f"GPIO {gpio} HIGH test passed, user indicated value was HIGH")

        # reset gpio to input
        # gpioget $(gpiofind <gpio_pin>)
        ssh.run_command(f"gpioget $(gpiofind {gpio})")

        if pull == "none":
            continue

        # Gpio get to test if pullup/pulldown is working, user should see expected value on DMM
        # gpioget $(gpiofind <gpio_pin>)
        out, err = ssh.run_command(f"gpioget $(gpiofind {gpio})")
        if pull == "up":
            expected = "1"
        elif pull == "down":    
            expected = "0"
        else:
            print(f"Invalid pull value {pull} for GPIO {gpio}, skipping pull test")
            continue

        if expected in out: 
            print(f"GPIO {gpio} pull {pull} test passed, value {out.strip()} matches expected {expected}")
            
        else:
            print(f"GPIO {gpio} pull {pull} test failed, value {out.strip()} does not match expected {expected}")
            failed_gpios.append(gpio)
        # prompt user to verify pullup is correct
        prompt = user_input.prompt(f"Please verify that GPIO {gpio} is {'HIGH' if pull == 'up' else 'LOW'} on the DMM due to the pull {pull} and then press Enter to continue.")

    if failed_gpios:    
        print(f"GPIO pull tests failed for the following GPIOs: {', '.join(failed_gpios)}")
        return htf.PhaseResult.FAIL_AND_CONTINUE
    else:
        print("GPIO pull tests passed for all GPIOs")
    pass