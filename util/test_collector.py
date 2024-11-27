# DUT Folder structure:
# dut/
# ├── __pycache__
# ├── __init__.py
# ├── main.py
# ├── XX (folder)
# │   ├── __init__.py
# │   ├── main.py
# │   ├── 0_name (folder)
# │   │   ├── __init__.py
# │   │   ├── test.py <--- This is the test file ran by the test manager
# │   │   ├── remote (folder) <--- This folder contains scripts to be ran on the DUT
# │   │   │   ├── example_script.sh
# │   │   │   ├── example_script2.py
# │   │   ├── data (folder) <--- This folder contains any data files to be used by the test
# │   │   │   ├── example_data.csv
# │   │   │   ├── example_data2.txt
# │   ├── 1_name (folder)
# │   │   ├── __init__.py
# │   │   ├── test.py <--- This is the test file ran by the test manager
# │   │   ├── remote (folder) <--- This folder contains scripts to be ran on the DUT
# │   │   │   ├── example_script.sh
# │   │   │   ├── example_script2.py
# │   │   ├── data (folder) <--- This folder contains any data files to be used by the test
# │   │   │   ├── example_data.csv
# │   │   │   ├── example_data2.txt
# ├── YY (folder)
# │   ├── __init__.py
# │   ├── main.py
# │   ├── 0_name (folder)
# │   │   ├── __init__.py
# │   │   ├── test.py <--- This is the test file ran by the test manager
# │   │   ├── remote (folder) <--- This folder contains scripts to be ran on the DUT
# │   │   │   ├── example_script.sh
# │   │   │   ├── example_script2.py
# │   │   ├── data (folder) <--- This folder contains any data files to be used by the test
# │   │   │   ├── example_data.csv
# │   │   │   ├── example_data2.txt
# │   ├── 1_name (folder)
# │   │   ├── __init__.py
# │   │   ├── test.py <--- This is the test file ran by the test manager
# │   │   ├── remote (folder) <--- This folder contains scripts to be ran on the DUT
# │   │   │   ├── example_script.sh
# │   │   │   ├── example_script2.py
# │   │   ├── data (folder) <--- This folder contains any data files to be used by the test
# │   │   │   ├── example_data.csv
# │   │   │   ├── example_data2.txt
#

# Test data sturcture
# [
#     {
#         "name": "XX",
#         "tests": [
#             {
#                 "id": "0",
#                 "name": "name",
#              },
#             {
#                 "id": "1",
#                 "name": "name",
#             }
#         ]
#     },
# ]


