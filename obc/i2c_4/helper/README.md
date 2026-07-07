I2C test helper for the Cora Z7.

Cora acts as compatible I2C slave.

I2C's is on PMod JA

I2C 0 (SDA: 2 SCL: 1) runs at 100KHz w/ address 0x30
 
I2C 1 (SDA: 4 SCL: 3) runs at 100KHz and 400KHz w/ address 0x31

Steps:
source ~/Xilinx/Vivado/2021.2/settings64.sh
source ~/Xilinx/Vitis/2021.2/settings64.sh

Launch vivado

Open cora_peripheral project in vivado

RUn synthesis, implementation and generate bitstream

Launch Vitis IDE from viviado

Import the vitis_export_archive.ide.zip