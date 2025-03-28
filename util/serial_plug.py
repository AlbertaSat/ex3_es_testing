import openhtf as htf
from openhtf.plugs import BasePlug
from openhtf.util import configuration
import serial
import time

CONF = configuration.CONF

TTY = CONF.declare(
    'tty',
    description='The serial port to use for communication',
    default_value='/dev/ttyUSB0',
)

class SerialPlug(BasePlug):
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def open(self):
        self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        time.sleep(2)  # Wait for the connection to establish

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def send_command(self, command):
        if not self.connection or not self.connection.is_open:
            raise RuntimeError("Serial connection is not open")
        self.connection.write((command + '\n').encode())
        time.sleep(0.1)
        response = self.connection.read_all().decode()
        return response

    def send_file(self, local_path, remote_path):
        with open(local_path, 'rb') as file:
            data = file.read()
        self.send_command(f'cat > {remote_path} <<EOF\n{data.decode()}\nEOF')

    def receive_file(self, remote_path, local_path):
        response = self.send_command(f'cat {remote_path}')
        with open(local_path, 'w') as file:
            file.write(response)

    def execute_program(self, program_path, args=''):
        return self.send_command(f'{program_path} {args}')
    
    def __str__(self):
        return f'SerialPlug(port={self.port}, baudrate={self.baudrate}, timeout={self.timeout})'
    
    def tearDown(self):
        self.close()

serial_plug_configured = configuration.bind_init_args(SerialPlug, port=TTY)

@htf.plug(serial=serial_plug_configured)
def test_serial_connection(test, serial):
    serial.open()
    response = serial.send_command('echo "Hello, DUT!"')
    test.logger.info('Response: %s', response)
    serial.close()


# Example usage
if __name__ == '__main__':
    test = htf.Test(test_serial_connection)
    test.execute()