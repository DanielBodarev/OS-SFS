import diskpy as dk 
import math
import inodehandler as ih

BYTE_ORDER = 'little'
ENCODE = 'utf-8'
FIELD_LENGTH = 4
MAGIC = 0xf0f03410
INODE_BLOCK_COUNT = 3
INODE_SIZE = 32
INODES_PER_BLOCK = dk.DISK_BLOCK_SIZE // INODE_SIZE
VALID_INODE = 1
VALID_INODE_DIR = 2
BAD_INODE = 3
INVALID_INODE = 0

# Adds superblocks and inodes
def format():
    assert(dk.open_file != None), "NO DISK OPEN"
    dk.disk_close()
    dk.disk_init(dk.file_name)
    superblock()
    print("Superblock created on block 0")
    empty_inode_blocks()
    print("{} Inodeblocks created on blocks 3-5".format(INODE_BLOCK_COUNT))

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
    field = add_field(data, 1, field)

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
        # i + sb[8] to skip over the superblock
        data = dk.disk_read(i + sb[8])
        field = 0
        for i in range(INODES_PER_BLOCK):

            # "isvalid" field
            field = add_field(data, INVALID_INODE, field)

            # "size" field
            field = add_field(data, INODE_SIZE, field)

            # dir1,...dir5, indir
            for i in range(6):
                field = add_field(data, 0, field)

        dk.disk_write(i + sb[8], data)

def get_superblock():
    assert (dk.file_name != None), "NO DISK OPEN"
    result = []
    sb = dk.disk_read(0)
    for i in range(len(sb) // FIELD_LENGTH):
        result.append(bytes_to_int(sb, i * FIELD_LENGTH))
    return result

def add_field(data, number, field, length = FIELD_LENGTH):
    number = number.to_bytes(length, BYTE_ORDER)
    for i in range(length):
        data[field + i] = number[i]
    return field + length

def add_string(data, string, field, length = 28):
    string = string.encode(ENCODE)
    for i in range(length):
        if i < len(string):
            data[field + i] = string[i]
        else:
            data[field + i] = 0
    return field + length

def bytes_to_int(data, start = 0, length = FIELD_LENGTH):
    return int.from_bytes(data[start : start + length], BYTE_ORDER)

def bytes_to_string(data, start = 0, length = 28):
    as_bytes = bytes(data[start : start + length])
    return as_bytes.decode(ENCODE).rstrip("\x00")