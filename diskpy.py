import os

DISK_BLOCK_SIZE = 512 

def disk_init(filename, nblocks=100):
    with open(filename, 'wb+') as f:
        block = bytearray([0 for i in range(DISK_BLOCK_SIZE)])
        for i in range(nblocks):
            f.write(block)
    
def disk_open(filename):
    try:
        return open(filename, 'rb')
    except:
        print("COULD NOT OPEN {}".format(filename))
    
def disk_size(filename):
    pass 
    
def disk_read(filename, blocknum):
    pass

def disk_write(filename, blocknum, data):
    assert(len(data) <= DISK_BLOCK_SIZE), "INPUT DATA TOO LARGE; MAXIMUM {} BYTES; {} GIVEN".format(DISK_BLOCK_SIZE, len(data))

    while len(data) < DISK_BLOCK_SIZE:
        data.append(0)

    old_file = "OLD_"+filename
    if os.path.exists(old_file):
        os.remove(old_file)
    os.rename(filename, old_file)
    
    assert(blocknum >= 0 and blocknum * DISK_BLOCK_SIZE < os.path.getsize(old_file)), "BLOCK NUMBER OUT OF RANGE"

    with open(filename, "wb+") as new, open(old_file, "rb") as old:

        for i, line in enumerate(old):
            if i == blocknum:
                new.write(bytearray(data))
            else:
                new.write(line)
    
    
def disk_close(stream):
    try:
        stream.close()
    except:
        print("COULD NOT CLOSE STREAM")

disk_init("t.1", 2)
disk_write("t.1", 1, [255 for i in range(DISK_BLOCK_SIZE)])