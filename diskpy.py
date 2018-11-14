import os, sys
os.chdir(sys.path[0])

DISK_BLOCK_SIZE = 512 
NUMBER_OF_BLOCKS = 64

open_file = None
file_name = ""

def disk_init(filename, nblocks=NUMBER_OF_BLOCKS):
    global open_file
    open(filename, "wb").close()
    disk_open(filename)
    blocks = bytearray([0 for i in range(DISK_BLOCK_SIZE * nblocks)])
    open_file.write(blocks)
    
def disk_open(filename):
    global open_file
    global file_name
    file_name = filename
    assert(open_file == None), "Close {} before opening another disk".format(file_name)
    try:
        open_file = open(filename, 'rb+')
    except:
        raise Exception("COULD NOT OPEN {}".format(filename))
    
def disk_size():
    global open_file
    global file_name
    assert(open_file != None), "NO DISK OPEN"
    return os.path.getsize(file_name) // DISK_BLOCK_SIZE
    
def disk_read(blocknum):
    global open_file
    assert(open_file != None), "NO DISK OPEN"

    size = disk_size()
    assert(blocknum < size and blocknum >= 0), "BLOCK NUMBER OUT OF RANGE"

    result = []
    start = blocknum * DISK_BLOCK_SIZE
    open_file.seek(start, 0)
    r = open_file.read(DISK_BLOCK_SIZE)
    for byte in r: 
        result.append(byte)
    return result

def disk_write(blocknum, data):
    global open_file
    assert(open_file != None), "NO DISK OPEN"

    size = disk_size()
    assert(len(data) <= DISK_BLOCK_SIZE), "INPUT DATA TOO LARGE; MAXIMUM {} BYTES; {} GIVEN".format(DISK_BLOCK_SIZE, len(data))
    assert(blocknum < size and blocknum >= 0), "BLOCK NUMBER OUT OF RANGE"

    # Fills in the rest of the block with zeros if not already full
    while len(data) < DISK_BLOCK_SIZE:
        data.append(0)

    blocks = []
    for i in range(size):
        if i == blocknum:
            blocks += data
        else:
            blocks += disk_read(i)

    open_file.seek(0, 0)
    open_file.write(bytearray(blocks))
    
def disk_close():
    global open_file
    global file_name
    assert(open_file != None), "NO DISK OPEN"

    try:
        open_file.close()
        open_file = None
    except:
        raise Exception("Could not close {}".format(file_name))

def disk_status():
    global open_file
    global file_name
    assert(open_file != None), "NO FILE OPEN"
    print("DISK {} HAS {} BLOCKS".format(file_name, disk_size()))