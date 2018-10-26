import os

DISK_BLOCK_SIZE = 512 

def disk_init(filename, nblocks=100):
    with open(filename, 'wb+') as f:
        blocks = [0 for i in range(DISK_BLOCK_SIZE)]
        [f.write(blocks) for i in range(nblocks)]
    
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

    old_file = "OLD_"+filename

    assert(len(data) <= DISK_BLOCK_SIZE), "INPUT DATA TOO LARGE; MAXIMUM {} BYTES; {} GIVEN".format(DISK_BLOCK_SIZE, len(data))

    with open(filename, "wb+") as new, open(old_file, "rb") as old:
        for line in old:
            new.write(line)
    
    
def disk_close(stream):
    try:
        stream.close()
    except:
        print("COULD NOT CLOSE STREAM")

disk_write("hello.123", 0, [22 for i in range(DISK_BLOCK_SIZE)])