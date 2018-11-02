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
    try:
        dk.disk_init(name, size)
    except Exception as e:
        print(e)

def close_disk():
    try:
        dk.disk_close()
    except Exception as e:
        print(e)

def open_disk():
    name = inp("Which disk should be opened?")
    try:
        dk.disk_open(name)
    except Exception as e:
        print(e)

def disk_status():
    try:
        dk.disk_status()
    except Exception as e:
        print(e)

def create_buffer():
    global buffer
    buffer = [0 for i in range(dk.DISK_BLOCK_SIZE)]
    print("Created Buffer")

def copy_buffer():
    global buffer
    if buffer is None:
        print(noBuffer)
        return
    block = get_number("Which block?")
    try:
        from_disk = dk.disk_read(block)
        print(from_disk)
        buffer = from_disk
        print("Copied from block {} into buffer".format(block))
    except Exception as e:
        print(e)

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
    try:
        dk.disk_write(block, as_byte_array)
        print("Wrote from buffer to disk.")
    except Exception as e:
        print(e)

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
        prompt = inp("What would you like to do?")
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