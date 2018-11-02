import diskpy as dk
import sys

# NOTE: HERE ARE ALL THE INITIAL COMMANDS:
# ext
# disk create
# disk open
# disk close 
# disk status
# buffer create
# buffer copy
# buffer write
# buffer print
# buffer fill
# SECONDARY PROMPTS WILL BE SELF-EXPLANATORY

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
    result = dk.disk_close()
    if result == dk.SUCCESS:
        print("Closed disk")
    else:
        print("Could not close disk")

def open_disk():
    name = inp("Which disk should be opened?")
    dk.disk_open(name)
    print("Opened disk")

def disk_status():
    dk.disk_status()

def create_buffer():
    global buffer
    buffer = [0 for i in range(dk.DISK_BLOCK_SIZE)]
    print("Buffer created successfully")

def copy_buffer():
    global buffer
    if buffer is None:
        print(noBuffer)
        return
    block = get_number("Which block?")
    from_disk = dk.disk_read(block)
    buffer = from_disk
    print("Copied from block {} into buffer".format(block))

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
    block = get_number("Which block on that disk?")
    as_byte_array = bytearray(buffer)
    result = dk.disk_write(block, as_byte_array)
    if result == dk.SUCCESS:
        print("Successfully wrote buffer to block {} in disk".format(block))
    else:
        print("Could not write buffer to block {} in disk".format(block))

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
        elif prompt == "ext":
            return
        else:
            print("'{}' is not a valid command".format(prompt))

commands = {"buffer create":create_buffer, "disk create":create_disk, "disk close":close_disk, "disk open":open_disk,
"disk status":disk_status, "buffer copy":copy_buffer, "buffer fill":fill_buffer, "buffer print":print_buffer, "buffer write":write_buffer}

if __name__ == "__main__":
    start()