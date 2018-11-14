import diskpy as dk
import sfs
import inodehandler as ih

UNUSED = 0
USED = 1
BAD = 2
NO_BITMAP = "NO INODE INODE BITMAP INITIALIZED"

ibitmap = None

def init():
    global ibitmap
    superblock = sfs.get_superblock()
    ibitmap_block = superblock[6]
    ibitmap = dk.disk_read(ibitmap_block)

    # First inode is bad
    ibitmap[0] = BAD

    total_inodes = superblock[2] * superblock[3]
    for i in range(1, total_inodes):
        inode = ih.get_inode(i)
        read_inode(inode, i)

    # Inodes outside range
    for i in range(total_inodes, len(ibitmap)):
        ibitmap[i] = BAD

    print("Inode bitmap created on block 2")
    save_to_disk()

def read_inode(inode, i):
    global ibitmap
    assert(ibitmap != None), NO_BITMAP
    if inode[0] == sfs.VALID_INODE or inode[0] == sfs.VALID_INODE_DIR:
        ibitmap[i] = USED
    elif inode[0] == sfs.INVALID_INODE:
        ibitmap[i] = UNUSED
    elif inode[0] == sfs.BAD_INODE:
        ibitmap[i] = BAD

def set_used(inode):
    global ibitmap
    assert(ibitmap != None), NO_BITMAP
    assert(inode >= 0 and inode < len(ibitmap)), "INODE {} OUT OF RANGE".format(inode)
    ibitmap[inode] = UNUSED
    save_to_disk()

def set_unused(inode):
    global ibitmap
    assert(ibitmap != None), NO_BITMAP
    assert(inode >= 0 and inode < len(ibitmap)), "INODE {} OUT OF RANGE".format(inode)
    ibitmap[inode] = UNUSED
    save_to_disk()

def find_unused(limit = -1):
    global ibitmap
    assert(ibitmap != None), NO_BITMAP
    unused = []
    for i,v in enumerate(ibitmap):
        if len(unused) < limit:
            if v == UNUSED:
                unused.append(i)
        else:
            return unused
    return unused

def save_to_disk():
    global ibitmap
    assert(ibitmap != None), NO_BITMAP
    superblock = sfs.get_superblock()
    ibitmap_block = superblock[6]
    dk.disk_write(ibitmap_block, ibitmap)

def print_bitmap():
    global ibitmap
    assert(ibitmap != None), NO_BITMAP
    cols = 8
    superblock = sfs.get_superblock()
    nbr_inodes = superblock[2] * superblock[3]
    print("INODE BITMAP: 0 = UNUSED, 1 = USED, 2 = BAD")
    string = ""
    for i in range(nbr_inodes):
        string += str(ibitmap[i])
        if i > 0 and i % cols == 0 and i < nbr_inodes - 1:
            print(string)
            string = ""
        else:
            string += ", "