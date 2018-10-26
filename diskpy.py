DISK_BLOCK_SIZE = 512 

def disk_init(filename, nblocks=100):
    with open(filename, 'wb+') as f:
        test = [0 for i in range(nblocks * DISK_BLOCK_SIZE)]
        f.write(bytearray(test))
    
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
    pass
    
    
def disk_close(stream):
    try:
        stream.close()
    except:
        print("COULD NOT CLOSE STREAM")