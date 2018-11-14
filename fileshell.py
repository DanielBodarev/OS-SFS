import diskpy as dk
import sys
import sfs
import bitmap as bp
import inodebitmap as ibp 
import dirblock as db

buffer = None
noBuffer = "BUFFER DOES NOT EXIST"
current_dir = "."
DIR_SEP = "/"

def inp(prompt):
    return input(prompt + "\n >> ")

def create_disk():
    name = inp("What should be the name of the disk?")
    #size = get_number("How many blocks should the disk have?")
    try:
        dk.disk_init(name)#, size)
        print("Disk '{}' initialized".format(name))
    except Exception as e:
        print(e)

def close_disk():
    try:
        dk.disk_close()
        print("Disk '{}' closed".format(dk.file_name))
    except Exception as e:
        print(e)

def open_disk():
    name = inp("Which disk should be opened?")
    try:
        dk.disk_open(name)
        print("Disk '{}' opened".format(name))
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

def format_disk():
    try:
        sfs.format()
        bp.init()
        ibp.init()
        db.init_dir_block()
        print("Successfuly formatted disk.")
    except Exception as e:
        print(e)

def dir_disk():
    try:
        db.print_dirs()
    except Exception as e:
        print(e)

def create_file_disk():
    filename = inp("What should the name of the file be?")
    try:
        db.new_file(filename)
        print("Successfully created {}".format(filename))
    except Exception as e:
        print(e)

def bitmap_init_disk():
    try:
        bp.init()
    except Exception as e:
        print(e)

def create_file():
    print("Created file '{}' in directory '{}'".format("XXXX", "YYYY"))

def mkdir():
    start = inp("Where should the new directory be created?")
    new = inp("What should be the name of the new directory?")
    print("Created directory '{}' in directory '{}'".format(new, start))

def pwd():
    global current_dir
    print("Current dir: {}".format(current_dir))

def cd():
    global current_dir
    new_dir = inp("What directory?")
    current_dir = current_dir + DIR_SEP + new_dir
    print("Changed to directory path '{}'".format(current_dir))

def print_dir():
    print("[Contents of current dir]")

def cmds():
    print("{:>20} - {:>20}".format("Command", "Description"))
    for k in commands:
        com = k if k in commands else ""
        desc = descriptions[k] if k in descriptions else ""
        print("{:>20} - {:>20}".format(com, desc))

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
        prompt = inp("What would you like to do? [cmds for help]")
        if prompt in commands:
            commands[prompt]()
        elif prompt == "ext":
            return
        else:
            print("'{}' is not a valid command".format(prompt))

commands = {"buffer create":create_buffer, "disk create":create_disk, "disk close":close_disk, "disk open":open_disk,
"disk status":disk_status, "buffer copy":copy_buffer, "buffer fill":fill_buffer, "buffer print":print_buffer, 
"buffer write":write_buffer, "disk format":format_disk, "disk dir":dir_disk, "disk file create":create_file_disk, 
"disk bitmap init":bitmap_init_disk, "create file":create_file, "mkdir":mkdir, "pwd":pwd, "cd":cd, "dir":print_dir, "cmds":cmds}

descriptions = {"disk write":"Write a buffer (block size) to disk", "disk read":"read a block from disk to a buffer",
"disk open":"open a disk with a filename", "disk close":"close the disk", "disk create":"Initialize a disk to a set number of blocks",
"buffer print":"display content of default buffer", "buffer fill":"fill the buffer with a number", "disk_format":"format the disk",
"create file":"create a file at current directory", "mkdir":"create a directory at current directory",
"pwd":"current directory path", "cd":"change directory", "dir":"display contents of current directory",
"cmds":"display a list of commands"}

if __name__ == "__main__":
    start()