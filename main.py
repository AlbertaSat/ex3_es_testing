import os.path
import time
import argparse

import openhtf as htf
from openhtf.output.callbacks import json_factory
from openhtf.plugs import user_input
from openhtf.util import configuration

import Q7
import Daedalus

configuration.CONF.declare("device", description="The device to test")
configuration.CONF.declare("hostname", description="The hostname of the DUT")
configuration.CONF.declare("username", description="The username of the DUT")
configuration.CONF.declare("password", description="The password of the DUT")
configuration.CONF.declare("tty", description="The path of the tty device for the DUT")

configuration.CONF.declare("use_helper", description="Boolean to enable or disable using the helper device during testing")
configuration.CONF.declare("helper_hostname", description="The hostname of the test helper device")
configuration.CONF.declare("helper_username", description="The username of the test helper device")
configuration.CONF.declare("helper_password", description="The password of the test helper device")
configuration.CONF.declare("helper_tty", description="The path of the tty device for the test helper device")

# Load Configuration from --config_file option
parser = argparse.ArgumentParser("ex3_es_testing")
parser.add_argument("--config_file", dest="config_file", help="The configuration file to use", type=str)
args = parser.parse_args()
with open(args.config_file, "r") as yamlfile:
    configuration.CONF.load_from_file(yamlfile)

def main():
    device = configuration.CONF.device

    if device == "Q7":
        Q7.run_all_tests()
    elif device == "Daedalus":
        Daedalus.test()
        pass
    else:
        print("Device not supported")
        exit(1)

if __name__ == '__main__':
  main()