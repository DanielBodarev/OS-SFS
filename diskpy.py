import os

DISK_BLOCK_SIZE = 512 

ERROR = -1
SUCCESS = 1

open_file = None

def disk_init(filename, nblocks=5):
    global open_file
    disk_open(filename)
    blocks = bytearray([0 for i in range(DISK_BLOCK_SIZE * nblocks)])
    open_file.write(blocks)
    
def disk_open(filename):
    global open_file
    assert(open_file == None), "File already open."
    try:
        open_file = open(filename, 'rb+')
        return SUCCESS
    except:
        print("COULD NOT OPEN {}".format(filename))
        return ERROR
    
def disk_size():
    global open_file
    assert(open_file != None), "NO FILE OPEN"
    return open_file.tell() // DISK_BLOCK_SIZE
    
def disk_read(blocknum):
    global open_file
    assert(open_file != None), "NO FILE OPEN"

    size = disk_size()
    assert(blocknum < size and blocknum >= 0), "BLOCK NUMBER OUT OF RANGE"

    result = []
    start = blocknum * DISK_BLOCK_SIZE
    open_file.seek(start, 0)
    r = open_file.read(DISK_BLOCK_SIZE)
    for byte in r: 
        result.append(ord(byte))
    return result

def disk_write(blocknum, data):
    global open_file
    assert(open_file != None), "NO FILE OPEN"

    try:
        size = disk_size()
        assert(len(data) <= DISK_BLOCK_SIZE), "INPUT DATA TOO LARGE; MAXIMUM {} BYTES; {} GIVEN".format(DISK_BLOCK_SIZE, len(data))
        assert(blocknum < size and blocknum >= 0), "BLOCK NUMBER OUT OF RANGE"

        while len(data) < DISK_BLOCK_SIZE:
            data.append(0)

        blocks = []
        for i in range(size):
            if i == blocknum:
                blocks += data
            else:
                blocks += disk_read(i)

        open_file.write(bytearray(blocks))
        
        return SUCCESS
    except:
        return ERROR
    
def disk_close():
    global open_file
    assert(open_file != None), "NO FILE OPEN"

    try:
        open_file.close()
        open_file = None
        return SUCCESS
    except:
        print("COULD NOT CLOSE STREAM")
        return ERROR

def disk_status():
    global open_file
    assert(open_file != None), "NO FILE OPEN"
    print("DISK HAS {} BLOCKS".format(disk_size()))