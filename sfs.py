import diskpy as dk
import math

FIELD_LENGTH = 4
MAGIC = 0xf0f03410
INODE_RATIO = 0.1
INODE_SIZE = 32
INODES_PER_BLOCK = dk.DISK_BLOCK_SIZE // INODE_SIZE
VALID_INODE = 1
INVALID_INODE = 0

# Adds superblocks and inodes
def format(filename):

    # Gets the file as an array of bytes
    data = []
    with open(filename, 'rb') as f:
        r = f.read()
        for b in r:
            data.append(int(b))

    assert(len(data) > dk.DISK_BLOCK_SIZE), "File {} is too small".format(filename)

    result = superblock(data)

    inodes(data, result)

    with open(filename, 'wb') as f:
        f.write(bytearray(data))


# Adds superblock
def superblock(data):

    # Keeps track of which field writing to
    field = 0

    # Adds magic numbers
    add_field(data, MAGIC, field)

    # Increment to next field
    field += FIELD_LENGTH

    # Gets nblocks as byte array and adds to array
    nblocks = len(data) // dk.DISK_BLOCK_SIZE
    add_field(data, nblocks, field)

    field += FIELD_LENGTH
    
    # Adds ninodeblocks
    ninodeblocks = math.ceil(nblocks * INODE_RATIO)
    add_field(data, ninodeblocks, field)

    field += FIELD_LENGTH

    # Adds ninodes
    add_field(data, INODES_PER_BLOCK, field)

    # Returns number of inode blocks
    return ninodeblocks

def inodes(data, ninodeblocks):
    for i in range(ninodeblocks):

        # i + 1 to skip over the superblock
        add_inode_block(data, i + 1)

def add_inode_block(data, block):
    field = block * dk.DISK_BLOCK_SIZE

    for i in range(INODES_PER_BLOCK):

        # "isvalid" field
        add_field(data, VALID_INODE, field)
        field += FIELD_LENGTH

        # "size" field
        add_field(data, INODE_SIZE, field)
        field += FIELD_LENGTH

        # direct[0]
        field += FIELD_LENGTH

        # direct[1]
        field += FIELD_LENGTH

        # direct[2]
        field += FIELD_LENGTH

        # direct[3]
        field += FIELD_LENGTH

        # direct[4]
        field += FIELD_LENGTH

        # indirect
        field += FIELD_LENGTH

def add_field(data, number, field):
    number = number.to_bytes(FIELD_LENGTH, 'big')
    for i in range(FIELD_LENGTH):
        data[field + i] = number[i]

format("t.1")