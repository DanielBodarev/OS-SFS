import diskpy as dk
import sfs
import inodebitmap as ibp

def get_inode(nbr):
    assert (dk.file_name != None), "NO DISK OPEN"
    sb = sfs.get_superblock()
    inode_block, inode_start = divmod(nbr, sfs.INODES_PER_BLOCK)
    assert (inode_block >= 0 and inode_block < sfs.INODE_BLOCK_COUNT * sfs.INODES_PER_BLOCK), "Invalid inode requested: {}".format(nbr)
    ib = dk.disk_read(inode_block + sb[8])
    result = []
    for i in range(8):
        result.append(sfs.bytes_to_int(ib, inode_start + (i * sfs.FIELD_LENGTH)))
    return result

def write_inode(nbr, data):
    assert (dk.file_name != None), "NO DISK OPEN"
    assert (len(data) == 8), "Inode has 8 fields, not {}".format(len(data))
    sb = sfs.get_superblock()
    inode_block, inode_start = divmod(nbr, sfs.INODES_PER_BLOCK)
    assert (inode_block >= 0 and inode_block < sfs.INODE_BLOCK_COUNT * sfs.INODES_PER_BLOCK), "Invalid inode requested"
    ib = dk.disk_read(inode_block + sb[8])
    for v in data:
        inode_start = sfs.add_field(ib, v, inode_start)
    dk.disk_write(inode_block + sb[8], ib)

    ibp.set_used(nbr)

def init_dir_inode():
    # Sets inode dir
    inode = get_inode(0)
    inode[0] = sfs.VALID_INODE
    inode[2] = 0
    ibp.set_used(0)
    write_inode(0, inode)
    print("Created dir inode at inode 0")

    # Writes empty dir nodes
    #field = 0
    #data = dk.disk_read(sb[5])
    #for i in range(16):
    #    field = sfs.add_field(data, 0, field)
    #    field = sfs.add_string(data, "", field, 28)

    #dk.disk_write(sb[5], data)