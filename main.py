import os.path
import time

import openhtf as htf
from openhtf.output.callbacks import json_factory
from openhtf.plugs import user_input
from openhtf.util import configuration

import Q7
import Daedalus

configuration.CONF.declare("device", description="The device to test")

# The @htf.measures annotation notifies the OpenHTF framework that this test
# phase will be taking a measurement that we'd like to call
# 'hello_world_measurement'.  Measurements can be accessed and set via
# the 'test' object, always passed as the first argument to test phases.
@htf.measures(htf.Measurement('hello_world_measurement'))
def hello_world(test):
  """A hello world test phase."""
  # At the heart of an OpenHTF test script are the test phases, such as
  # this one.  Any callable can be used as a test phase, so long as it
  # accepts a single argument that is the 'test' object.  This test object
  # is how you will interact with the OpenHTF test framework once a test is
  # running.  See other examples for more complex cases, but here is a good
  # example of the sort of minimal functionality you're likely to use.

  # The test.logger attribute is a Python logger instance that is configured
  # to log to the test record we will output at the end of the test.  This
  # is the recommended way to do any logging within test phases (this is also
  # how to get logs to show up in the frontend).
  test.logger.info('Hello World!')

  # As described above, this is how measurements are set.  The value that has
  # been set can also be accessed, but should only be set once (this will be
  # enforced in the future, for now it's best-practice).
  test.measurements.hello_world_measurement = 'Hello Again!'

def main():
#   test = htf.Test(hello_world)
#   test.add_output_callbacks(
#       json_factory.OutputToJSON('./{dut_id}.result.json', indent=2))
#   test.execute(test_start=user_input.prompt_for_test_start())
    device = configuration.CONF.device

    if device == "Q7":
        Q7.test()
    elif device == "Daedalus":
        Daedalus.test()
        pass
    else:
        print("Device not supported")
        exit(1)

if __name__ == '__main__':
  main()