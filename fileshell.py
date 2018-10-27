import click
import diskpy as dk

@click.group()
def top():
    pass

@top.group()
def disk():
    pass

@top.group()
def buffer():
    pass

@disk.command('create')
@click.argument('filename', type=click.File('wb'))
@click.option('--size', default=5, help="Size of disk")
def create_disk(filename, size):
    dk.disk_init(filename, size)
    click.echo("Successfully created {}".format(filename))

@disk.command('open')
@click.argument('filename', type=click.STRING)
def open_disk(filename):
    result = dk.disk_open(filename)
    if result == dk.SUCCESS:
        click.echo("Successfully opened {}".format(filename))

@disk.command('status')
@click.argument('filename', type=click.STRING)
def status_disk(filename):
    dk.disk_status(filename)

@disk.command('close')
@click.argument('filename', type=click.STRING)
def close_disk(filename):
    result = dk.disk_close(filename)
    if result == dk.SUCCESS:
        click.echo("Successfully closed {}".format(filename))

buffers = dict()

@buffer.command('create')
@click.argument('buffername', type=click.STRING)
def create_buffer(buffername):
    buffers[buffername] = [0 for i in range(dk.DISK_BLOCK_SIZE)]
    click.echo("Created buffer under name {}".format(buffername))
    click.echo(buffers)

@buffer.command('fill')
@click.argument('buffername', type=click.STRING)
@click.argument('byte', type=click.INT)
def fill_buffer(buffername, byte):
    for i in enumerate(buffers[buffername]):
        buffers[buffername][i] = byte
    click.echo("Filled buffer {} with values{}".format(buffername, byte))

@buffer.command('write')
@click.argument('filename', type=click.STRING)
@click.argument('buffername', type=click.STRING)
@click.argument('block', type=click.INT)
def write_buffer(filename, buffername, block):
    as_byte_array = bytearray(buffers[buffername])
    result = dk.disk_write(filename, block, as_byte_array)
    if result == dk.SUCCESS:
        click.echo("Successfully wrote {} to block {} in disk {}".format(buffername, block, filename))

@buffer.command('copy')
@click.argument('filename', type=click.STRING)
@click.argument('buffername', type=click.STRING)
@click.argument('block', type=click.INT)
def copy_buffer(filename, buffername, block):
    from_disk = dk.disk_read(filename, block)
    buffers[buffername] = from_disk
    click.echo("Successfully wrote {} to block {} in disk {}".format(buffername, block, filename))

@buffer.command('print')
@click.argument('buffername', type=click.STRING)
def print_buffer(buffername):
    click.echo("Buffer {}:".format(buffername))
    click.echo(buffers[buffername])

""" 
@buffer.command('list')
def list_buffers():
    click.echo("All buffers:", [key for key in buffers])

@buffer.command('drop')
@click.argument('buffername', type=click.STRING)
def drop_buffer(buffername):
    del buffers[buffername]
    click.echo("Deleted buffer with name {}".format(buffername)) 
"""

if __name__ == '__main__':
    top()
