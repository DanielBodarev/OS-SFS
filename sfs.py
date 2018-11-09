import diskpy as dk 
import math

BYTE_ORDER = 'little'
ENCODE = 'utf-8'
FIELD_LENGTH = 4
MAGIC = 0xf0f03410
INODE_BLOCK_COUNT = 3
INODE_SIZE = 32
INODES_PER_BLOCK = dk.DISK_BLOCK_SIZE // INODE_SIZE
VALID_INODE = 1
INVALID_INODE = 0

# Adds superblocks and inodes
def format():
    assert(dk.open_file != None), "NO DISK OPEN"
    dk.disk_init(dk.file_name)
    superblock()
    empty_inode_blocks()
    dir_inode()

def dir_inode():
    sb = get_superblock()
    # Sets inode dir
    inode = get_inode(0)
    inode[0] = VALID_INODE
    inode[2] = 0
    write_inode(0, inode)

    # Writes empty dir nodes
    field = 0
    data = dk.disk_read(inode[2] + sb[7])
    for i in range(16):
        field = add_field(data, 0, field)
        field = add_field(data, 0, field)
        field = add_string(data, "", field, 24)

    dk.disk_write(inode[2] + sb[7], data)

# Adds superblock
def superblock():

    # Gets data
    data = dk.disk_read(0)

    # Keeps track of which field writing to
    field = 0

    # Adds magic numbers - 0
    field = add_field(data, MAGIC, field)

    # Writes number of blocks - 1
    field = add_field(data, dk.NUMBER_OF_BLOCKS, field)
    
    # Adds ninodeblocks - 2
    field = add_field(data, INODE_BLOCK_COUNT, field)

    # Adds ninodes - 3
    field = add_field(data, INODES_PER_BLOCK, field)

    # Adds dentry - 4
    field = add_field(data, 0, field)

    # datablock bitmap - 5
    field = add_field(data, 1, field)

    # inode bitmap - 6
    field = add_field(data, 2, field)

    # first datablock - 7
    field = add_field(data, 3 + INODE_BLOCK_COUNT, field)
    
    # first inode block - 8
    field = add_field(data, 3, field)

    # Writes data
    dk.disk_write(0, data)

def empty_inode_blocks():
    sb = get_superblock()
    for i in range(INODE_BLOCK_COUNT):
        # i + INODE_START to skip over the superblock
        data = dk.disk_read(i + sb[8])
        field = 0
        for i in range(INODES_PER_BLOCK):

            # "isvalid" field
            field = add_field(data, INVALID_INODE, field)

            # "size" field
            field = add_field(data, INODE_SIZE, field)
            
            # Dirs 1 -> 5
            for i in range(5):
                field = add_field(data, 0, field)

        dk.disk_write(i + sb[8], data)

def get_superblock():
    assert (dk.file_name != None), "NO DISK OPEN"
    result = []
    sb = dk.disk_read(0)
    for i in range(len(sb) // FIELD_LENGTH):
        result.append(bytes_to_int(sb, i * FIELD_LENGTH))
    return result
    
def get_inode(nbr):
    assert (dk.file_name != None), "NO DISK OPEN"
    sb = get_superblock()
    inode_block, inode_start = divmod(nbr, INODES_PER_BLOCK)
    assert (inode_block >= 0 and inode_block < INODE_BLOCK_COUNT * INODES_PER_BLOCK), "Invalid inode requested: {}".format(nbr)
    ib = dk.disk_read(inode_block + sb[8])
    result = []
    for i in range(7):
        result.append(bytes_to_int(ib, inode_start + (i * FIELD_LENGTH)))
    return result

def write_inode(nbr, data):
    assert (dk.file_name != None), "NO DISK OPEN"
    assert (len(data) == 7), "Inode has 7 fields, not {}".format(len(data))
    sb = get_superblock()
    inode_block, inode_start = divmod(nbr, INODES_PER_BLOCK)
    assert (inode_block >= 0 and inode_block < INODE_BLOCK_COUNT * INODES_PER_BLOCK), "Invalid inode requested"
    ib = dk.disk_read(inode_block + sb[8])
    for v in data:
        inode_start = add_field(ib, v, inode_start)
    dk.disk_write(inode_block + sb[8], ib)

def get_dirs():
    assert (dk.file_name != None), "NO DISK OPEN"
    data, dblock = get_dir_block()
    result = []
    for i in range(16):
        start = i * 32
        result.append((
            bytes_to_int(data, start, 4),
            bytes_to_int(data, 4 + start, 4),
            bytes_to_string(data, 8 + start, 24)))
    return result

def get_dir_block():
    assert (dk.file_name != None), "NO DISK OPEN"
    sb = get_superblock()
    dentry = get_superblock()[4]
    dinode = get_inode(dentry)[2]
    dblock = get_inode(dinode)[2]
    data = dk.disk_read(dblock + sb[7])
    return data, dblock

def write_dir(tup):
    assert (dk.file_name != None), "NO DISK OPEN"
    assert (len(tup) == 3), "TUPLE HAS 3 FIELDS"
    sb = get_superblock()
    dirs = get_dirs()
    for i,v in enumerate(dirs):
        if v[1] == 0:
            dirs[i] = tup
            break
    data, dblock = get_dir_block()
    field = 0
    for i in dirs:
        field = add_field(data, i[0], field)
        field = add_field(data, i[1], field)
        field = add_string(data, i[2], field, 24)
    dk.disk_write(dblock + sb[7], data)

def new_file(filename):
    nbr = -1
    for i in range(1, INODE_BLOCK_COUNT * INODES_PER_BLOCK):
        n = get_inode(i)
        if n[0] == INVALID_INODE:
            nbr = i
            break
    assert(nbr != -1), "COULD NOT FIND EMPTY INODE"
    write_inode(nbr, [VALID_INODE, 0, 3, 0, 0, 0, 0])
    write_dir((nbr, len(filename), filename))

def print_dirs():
    dirs = get_dirs()
    exist = []
    for d in dirs:
        if len(d[2]) > 0:
            exist.append(d[2])
    print(exist)

def add_field(data, number, field, length = FIELD_LENGTH):
    number = number.to_bytes(length, BYTE_ORDER)
    for i in range(length):
        data[field + i] = number[i]
    return field + length

def add_string(data, string, field, length = 24):
    string = string.encode(ENCODE)
    for i in range(length):
        if i < len(string):
            data[field + i] = string[i]
        else:
            data[field + i] = 0
    return field + length

def bytes_to_int(data, start = 0, length = FIELD_LENGTH):
    return int.from_bytes(data[start : start + length], BYTE_ORDER)

def bytes_to_string(data, start = 0, length = 24):
    as_bytes = bytes(data[start : start + length])
    return as_bytes.decode(ENCODE).rstrip("\x00")