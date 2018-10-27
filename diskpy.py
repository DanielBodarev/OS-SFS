import os

DISK_BLOCK_SIZE = 512 

ERROR = -1
SUCCESS = 1

open_files = dict()

def disk_init(filename, nblocks=5):
    with open(filename, 'wb+') as f:
        blocks = bytearray([0 for i in range(DISK_BLOCK_SIZE * nblocks)])
        f.write(blocks)
    
def disk_open(filename):
    try:
        open_files[filename] = open(filename, 'rb')
        return SUCCESS
    except:
        print("COULD NOT OPEN {}".format(filename))
        return ERROR
    
def disk_size(filename):
    return os.path.getsize(filename) // DISK_BLOCK_SIZE
    
def disk_read(filename, blocknum):
    size = disk_size(filename)
    assert(blocknum < size and blocknum >= 0), "BLOCK NUMBER OUT OF RANGE"

    with open(filename, 'rb') as f:
        r = f.read()
        result = []
        start = blocknum * DISK_BLOCK_SIZE
        end = start + DISK_BLOCK_SIZE
        for i in range(start, end):
            result.append(ord((r[i])))
        return result

def disk_write(filename, blocknum, data):
    try:
        size = disk_size(filename)
        assert(len(data) <= DISK_BLOCK_SIZE), "INPUT DATA TOO LARGE; MAXIMUM {} BYTES; {} GIVEN".format(DISK_BLOCK_SIZE, len(data))
        assert(blocknum < size and blocknum >= 0), "BLOCK NUMBER OUT OF RANGE"

        while len(data) < DISK_BLOCK_SIZE:
            data.append(0)

        blocks = []
        for i in range(size):
            if i == blocknum:
                blocks += data
            else:
                blocks += disk_read(filename, i)

        with open(filename, 'wb') as f:
            f.write(bytearray(blocks))
        
        return SUCCESS
    except:
        return ERROR
    
def disk_close(filename):
    try:
        open_files[filename].close()
        del open_files[filename]
        return SUCCESS
    except:
        print("COULD NOT CLOSE STREAM")
        return ERROR

def disk_status(filename):
    print("DISK {} HAS {} BLOCKS".format(filename, disk_size(filename)))