# Adds superblocks and inodes
def format(filename):
    with open(filename, 'wb') as f:
        f = f.read()