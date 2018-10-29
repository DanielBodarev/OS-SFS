import diskpy as dk
import sys

buffer = None
noBuffer = "BUFFER DOES NOT EXIST"

def inp(prompt):
    return input(prompt + "\n >> ")

def create_disk():
    name = inp("What should be the name of the disk?")
    size = get_number("How many blocks should the disk have?")
    dk.disk_init(name, size)
    print("Created disk '{}' with {} blocks".format(name, size))

def close_disk():
    name = inp("Which disk should be closed?")
    dk.disk_close(name)
    print("Closed disk '{}'".format(name))

def open_disk():
    name = inp("Which disk should be opened?")
    dk.disk_open(name)
    print("Opened disk '{}'".format(name))

def disk_status():
    name = inp("Which disk should display status?")
    dk.disk_status(name)

def create_buffer():
    global buffer
    buffer = [0 for i in range(dk.DISK_BLOCK_SIZE)]
    print("Buffer created successfully")

def copy_buffer():
    global buffer
    if buffer is None:
        print(noBuffer)
        return
    name = inp("From which disk should the buffer copy?")
    block = get_number("Which block on that disk?")
    from_disk = dk.disk_read(name, block)
    buffer = from_disk
    print("Copied from '{}' block {} into buffer".format(name, block))

def fill_buffer():
    global buffer
    if buffer is None:
        print(noBuffer)
        return
    byte = get_number("What byte should the buffer be filled with?")
    for i, v in enumerate(buffer):
        buffer[i] = byte
    print("Filled buffer with {}".format(byte))

def print_buffer():
    global buffer
    if buffer is None:
        print(noBuffer)
        return
    print(buffer)

def write_buffer():
    global buffer
    if buffer is None:
        print(noBuffer)
        return
    name = inp("Which disk should the buffer be written into?")
    block = get_number("Which block on that disk?")
    as_byte_array = bytearray(buffer)
    result = dk.disk_write(name, block, as_byte_array)
    if result == dk.SUCCESS:
        print("Successfully wrote buffer to block {} in disk '{}'".format(block, name))
    else:
        print("Could not write buffer to block {} in disk '{}'".format(block, name))

def get_number(prompt):
    p = inp(prompt)
    try:
        p = int(p)
        return p
    except:
        print("{} is not a valid number".format(p))
        return get_number(prompt)

def start():
    while True:
        prompt = inp("[-] What would you like to do?")
        if prompt in commands:
            commands[prompt]()
        elif prompt == "exit":
            return
        else:
            print("'{}' is not a valid command".format(prompt))

commands = {"buffer create":create_buffer, "disk create":create_disk, "disk close":close_disk, "disk open":open_disk,
"disk status":disk_status, "buffer copy":copy_buffer, "buffer fill":fill_buffer, "buffer print":print_buffer, "buffer write":write_buffer}

if __name__ == "__main__":
    start()