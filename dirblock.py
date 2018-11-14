import diskpy as dk
import sfs
import inodebitmap as ibp
import inodehandler as ih

DIR_SIZE = 32
DIRS_PER_BLOCK = dk.DISK_BLOCK_SIZE // DIR_SIZE

def init_dir_block():
    ih.init_dir_inode()
    write_dir(1, ".", False)
    write_dir(1, "..", False)
    ibp.set_used(1)
    write_dir(2, "etc", False)
    ibp.set_used(2)
    write_dir(3, "bin", False)
    ibp.set_used(3)
    print("Successfully added ., .., etc, and bin")

# Returns list of tuples (inode, name)
def get_dirs():
    assert (dk.file_name != None), "NO DISK OPEN"
    data, dblock = get_dir_block()
    result = []
    for i in range(DIRS_PER_BLOCK):
        start = i * DIR_SIZE
        result.append((
            sfs.bytes_to_int(data, start, sfs.FIELD_LENGTH),
            sfs.bytes_to_string(data, start + sfs.FIELD_LENGTH, DIR_SIZE - (sfs.FIELD_LENGTH))))
    return result

def get_dir_block():
    assert (dk.file_name != None), "NO DISK OPEN"
    sb = sfs.get_superblock()
    dentry = sb[4]
    dinode = ih.get_inode(dentry)[2]
    dblock = ih.get_inode(dinode)[2]
    data = dk.disk_read(dblock + sb[7])
    return data, dblock

def write_dir(inode, name, file=True):
    assert (dk.file_name != None), "NO DISK OPEN"

    if file:
        name = "f{}".format(name)
    else:
        name = "d{}".format(name)

    # Gets dir tuples and replaces one
    sb = sfs.get_superblock()
    dirs = get_dirs()
    for i,v in enumerate(dirs):
        if v[0] == sfs.INVALID_INODE:
            dirs[i] = (inode, name)
            break
    data, dblock = get_dir_block()
    field = 0
    for i in dirs:
        field = sfs.add_field(data, i[0], field)
        field = sfs.add_string(data, i[1], field, 28)
    dk.disk_write(dblock + sb[7], data)

def get_inode_by_name(name, file=True):
    if file:
        name = "f{}".format(name)
    else:
        name = "d{}".format(name)
    dirs = get_dirs()
    for d in dirs:
        if d[1] == name:
            return d[0]

def print_dirs():
    dirs = get_dirs()
    print(dirs)

def new_file(filename):
    empty_inode_index = ibp.find_unused(1)[0]
    ih.write_inode(empty_inode_index, [sfs.VALID_INODE, 0, 3, 0, 0, 0, 0])
    write_dir(empty_inode_index, filename, True)