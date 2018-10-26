import os

DISK_BLOCK_SIZE = 512 

def disk_init(filename, nblocks=100):
    with open(filename, 'wb+') as f:
        blocks = bytearray([0 for i in range(DISK_BLOCK_SIZE * nblocks)])
        f.write(blocks)
    
def disk_open(filename):
    try:
        return open(filename, 'rb')
    except:
        print("COULD NOT OPEN {}".format(filename))
    
def disk_size(filename):
    return os.path.getsize(filename) // DISK_BLOCK_SIZE
    
def disk_read(filename, blocknum):
    size = disk_size(filename)
    assert(blocknum < size and blocknum >= 0), "BLOCK NUMBER OUT OF RANGE"

    with open(filename, 'rb') as f:
        r = f.read()
        result = []
        start = blocknum + DISK_BLOCK_SIZE
        end = start + DISK_BLOCK_SIZE
        for i in range(start, end):
            result.append(int(r[i]))
        return result

def disk_write(filename, blocknum, data):
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
    
def disk_close(stream):
    try:
        stream.close()
    except:
        print("COULD NOT CLOSE STREAM")

disk_init("t.1", 2)
disk_write("t.1", 1, [255 for i in range(DISK_BLOCK_SIZE)])