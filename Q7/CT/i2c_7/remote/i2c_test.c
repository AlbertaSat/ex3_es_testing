// Usage: i2c_test <bus number>
// This test creates 1KBit of data and checksums it before writing to an
// EEPROM connected to the specified I2C bus. The test then reads the 
// data back and checks that the checksum matches.

// CRC-32 implementation from https://web.mit.edu/freebsd/head/sys/libkern/crc32.c

#include <stdio.h>
#include <stdlib.h>
#include <zlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include <string.h>

#define EEPROM_ADDR 0x50
#define DATA_LEN 16 // 128 bytes (1Kbit) of data to write to EEPROM
#define PAGE_SIZE 1


int i2c_page_write(int file, unsigned char mem_addr, unsigned char *data, unsigned long len) {
    if (len > PAGE_SIZE) {
        fprintf(stderr, "Data length exceeds page size\n");
        return -1;
    }
    
    // Buffer to hold memory address and data for page write
    unsigned char buf[PAGE_SIZE + 2];
    buf[0] = mem_addr; // address
    memcpy(buf + 1, data, len);

    struct i2c_msg msg = {
        .addr = EEPROM_ADDR,
        .flags = 0, // write
        .len = (unsigned short)(len + 1),
        .buf = buf
    };

    struct i2c_rdwr_ioctl_data ioctl_data = {
        .msgs = &msg,
        .nmsgs = 1
    };

    printf("Sending message: ");
    for (int i = 0; i < len + 1; i++) {
        printf("%02x ", buf[i]);
        if ((i + 1) % 16 == 0) {
            printf("\n");
        }
    }
    printf("\n");

    if (ioctl(file, I2C_RDWR, &ioctl_data) < 0) {
        perror("Failed to write to EEPROM");
        return -1;
    }

    usleep(100000); // wait for EEPROM write cycle to complete
    return len;
}



int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <bus_number>\n", argv[0]);
        return 1;
    }

    // Get bus number from command line argument
    int bus_number = atoi(argv[1]);
    printf("Testing I2C bus number %d\n", bus_number);

    // Create random 1K data to write to EEPROM
    unsigned long len = DATA_LEN;
    unsigned char data[len];
    for (int i = 0; i < len; i++) {
        data[i] = (rand() % 256);
    }
    printf("Data created for writing to EEPROM\n");
    printf("Data length: %lu bytes\nData: ", len);
    // print data in hex format, 16 bytes per line
    for (int i = 0; i < len; i++) {
        printf("%02x ", data[i]);
        if ((i + 1) % 16 == 0) {
            printf("\n");
        }
    }

    // Calculate CRC-32 checksum of data
    uLong crc = crc32(0L, Z_NULL, 0);
    crc = crc32(crc, data, len);
    printf("Data CRC-32 checksum: %08lx\n", crc);

    // Open I2C device file for the specified bus number
    int file;
    char bus_file[20];
    snprintf(bus_file, sizeof(bus_file), "/dev/i2c-%d", bus_number);
    if ((file = open(bus_file, O_RDWR)) < 0) {
        perror("Failed to open I2C bus");
        return -1;
    }

    // Write data to EEPROM in page-sized chunks
    for (unsigned long offset = 0; offset < len; offset += PAGE_SIZE) {
        unsigned char mem_addr = (unsigned char)(offset & 0xFF); // memory address to write to
        unsigned char *chunk = data + offset; // pointer to current chunk
        unsigned long chunk_len = (offset + PAGE_SIZE <= len) ? PAGE_SIZE : (len - offset); // length of current chunk
        if (i2c_page_write(file, mem_addr, chunk, chunk_len) < 0) {
            fprintf(stderr, "Failed to write data to EEPROM at offset %lu\n", offset);
            close(file);
            return -1;
        }
        printf("Written %lu bytes to EEPROM at memory address 0x%02x\n", chunk_len, mem_addr);
        printf("Chunk data: ");
        for (unsigned long i = 0; i < chunk_len; i++) {
            printf("%02x ", chunk[i]);
            if ((i + 1) % 16 == 0) {
                printf("\n");
            }
        }
	printf("\n");
    }

    // Read data back from EEPROM and verify checksum
    unsigned char read_data[len];
    struct i2c_msg msgs[2] = {
        {
            .addr = EEPROM_ADDR,
            .flags = 0, // write
            .len = 1,
            .buf = (unsigned char[]){0} // memory address to read from
        },
        {
            .addr = EEPROM_ADDR,
            .flags = I2C_M_RD, // read
            .len = (unsigned short)len,
            .buf = read_data
        }
    };

    struct i2c_rdwr_ioctl_data ioctl_data = {
        .msgs = msgs,
        .nmsgs = 2
    };

    if (ioctl(file, I2C_RDWR, &ioctl_data) < 0) {
        perror("Failed to read from EEPROM");
        close(file);
        return -1;
    }

    printf("Data: ");
    for (unsigned long i = 0; i < len; i++) {
        printf("%02x ", read_data[i]);
        if ((i + 1) % 16 == 0) {
            printf("\n");
        }
    }
    printf("\n");

    // Calculate CRC-32 checksum of read data
    uLong read_crc = crc32(0L, Z_NULL, 0);
    read_crc = crc32(read_crc, read_data, len);
    printf("Read data CRC-32 checksum: %08lx\n", read_crc);


    if (crc == read_crc) {
        printf("Data verification passed!\n");
    } else {
        fprintf(stderr, "Data verification failed!\n");
        close(file);
        return -1;
    }

    close(file);
    return 0;
}
