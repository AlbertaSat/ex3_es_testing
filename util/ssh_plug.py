import openhtf as htf
from openhtf.core import base_plugs
from openhtf.output.callbacks import json_factory
from openhtf.plugs import user_input
from openhtf.util import configuration
import paramiko
import scp

CONF = configuration.CONF

HOSTNAME = CONF.declare(
    'hostname',
    description='The hostname of the SSH server'
)

USERNAME = CONF.declare(
    'username',
    description='The username for the SSH server'
)

PASSWORD = CONF.declare(
    'password',
    description='The password for the SSH server'
)

class SSHPlug(base_plugs.BasePlug):
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = None
        self.scp_client = None

    def open(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, username=self.username, password=self.password)
        self.scp_client = scp.SCPClient(self.client.get_transport())

    def close(self):
        if self.scp_client:
            self.scp_client.close()
        if self.client:
            self.client.close()

    def run_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read(), stderr.read()

    def send_file(self, local_path, remote_path):
        self.scp_client.put(local_path, remote_path)

    def receive_file(self, remote_path, local_path):
        self.scp_client.get(remote_path, local_path)

    def __str__(self):
        return f'SSHPlug(hostname={self.hostname}, username={self.username})'
    
    def tearDown(self):
        self.close()

ssh_plug_configured = configuration.bind_init_args(SSHPlug, hostname=HOSTNAME, username=USERNAME, password=PASSWORD)

@htf.plug(ssh=ssh_plug_configured)
def test_ssh_connection(test, ssh):
    ssh.open()
    stdout, stderr = ssh.run_command('echo "Hello, DUT!"')
    test.logger.info('STDOUT: %s', stdout)
    test.logger.info('STDERR: %s', stderr)
    ssh.close()

if __name__ == '__main__':
    test = htf.Test(test_ssh_connection)
    test.add_output_callbacks(json_factory.OutputToJSON('./{dut_id}.ssh.json', indent=2))
    test.execute(test_start=user_input.prompt_for_test_start())