import diskpy as dk
import sfs
import inodehandler as ih

UNUSED = 0
USED = 1
BAD = 2
NO_BITMAP = "NO BITMAP INITIALIZED"

bitmap = None

def init():
    global bitmap
    superblock = sfs.get_superblock()
    bitmap_block = superblock[5]
    bitmap = dk.disk_read(bitmap_block)

    # Always used, meta-blocks
    datablock_start = superblock[7]
    for i in range(datablock_start):
        bitmap[i] = USED

    # Data blocks
    total_inodes = superblock[2] * superblock[3]
    for i in range(total_inodes):
        inode = ih.get_inode(i)
        read_inode(inode)

    # Blocks outside range
    for i in range(superblock[1], len(bitmap)):
        bitmap[i] = BAD

    print("Block bitmap created on block 1")
    save_to_disk()

def read_inode(inode):
    global bitmap
    assert(bitmap != None), NO_BITMAP
    if inode[0] == sfs.VALID_INODE:
        for i in range(2,6):
            if inode[i] > 0:
                bitmap[inode[i]] = USED
    elif inode[0] == sfs.INVALID_INODE:
        for i in range(2,6):
            if inode[i] > 0:
                bitmap[inode[i]] = BAD

def set_used(block):
    global bitmap
    assert(bitmap != None), NO_BITMAP
    assert(block >= 0 and block < len(bitmap)), "BLOCK {} OUT OF RANGE".format(block)
    bitmap[block] = UNUSED

def set_unused(block):
    global bitmap
    assert(bitmap != None), NO_BITMAP
    assert(block >= 0 and block < len(bitmap)), "BLOCK {} OUT OF RANGE".format(block)
    bitmap[block] = UNUSED

def find_unused(limit = -1):
    global bitmap
    assert(bitmap != None), NO_BITMAP
    unused = []
    for i,v in enumerate(bitmap):
        if len(unused) < limit:
            if v == UNUSED:
                unused.append(i)
        else:
            return unused
    return unused

def save_to_disk():
    global bitmap
    assert(bitmap != None), NO_BITMAP
    superblock = sfs.get_superblock()
    bitmap_block = superblock[5]
    dk.disk_write(bitmap_block, bitmap)

def print_bitmap():
    global bitmap
    assert(bitmap != None), NO_BITMAP
    cols = 8
    superblock = sfs.get_superblock()
    nbr_blocks = superblock[1]
    print("BITMAP: 0 = UNUSED, 1 = USED, 2 = BAD")
    string = ""
    for i in range(nbr_blocks):
        string += str(bitmap[i])
        if i > 0 and i % cols == 0 and i < nbr_blocks - 1:
            print(string)
            string = ""
        else:
            string += ", "