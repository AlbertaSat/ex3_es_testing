# ex3_es_testing
Software used for testing the Q7 obc and daughterboard

We will be using openhtf is sparsely documented.

## Setup

Use the following docker command for dev environment if not on linux
```bash
sudo docker run -it --rm -v $(pwd):/app -w /app python:3 bash
```

Create a virtual environment
```bash
python3 -m venv venv
```

Activate the virtual environment
```bash
source venv/bin/activate
```

Install the required packages
```bash
pip install -r requirements.txt
```

## Running the tests

First, modify the `config.yaml` file to match the configuration of the device under test.

Then run the following command to start the tests

```bash
python main.py --config_file q7-config.yaml
# or
python main.py --config_file daedalus-config.yaml
```


## Folder structure

### DUT Folder structure

The DUT folder structure should be as follows:

```
dut/
├── __init__.py
├── main.py
├── XX (folder)
│   ├── __init__.py
│   ├── test.py
│   ├── 0_name (folder)
│   │   ├── __init__.py
│   │   ├── test.py <--- This is the test file ran by the test manager
│   │   ├── remote (folder) <--- This folder contains scripts to be ran on the DUT
│   │   │   ├── example_script.sh
│   │   │   ├── example_script2.py
│   │   ├── data (folder) <--- This folder contains any data files to be used by the test
│   │   │   ├── example_data.csv
│   │   │   ├── example_data2.txt
│   ├── 1_name (folder)
│   │   ├── __init__.py
│   │   ├── test.py <--- This is the test file ran by the test manager
│   │   ├── remote (folder) <--- This folder contains scripts to be ran on the DUT
│   │   │   ├── example_script.sh
│   │   │   ├── example_script2.py
│   │   ├── data (folder) <--- This folder contains any data files to be used by the test
│   │   │   ├── example_data.csv
│   │   │   ├── example_data2.txt
```

## Documentation

### Remote Scripts

Remote scripts are simple python, bash, etc scripts that are ran on the DUT. They are used to interact with the DUT and perform actions that are not possible from the test manager. They are stored in the `remote` folder of the test folder. Scripts should return a 0 exit code if they are successful and a non-zero exit code if they fail.