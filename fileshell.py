import click
import diskpy as dk

@click.group()
def top():
    pass

@top.group()
def disk():
    pass

@top.group()
@click.pass_context
def buffer(ctx):
    if ctx.obj is None:
        ctx.obj = []

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

@buffer.command('create')
@click.pass_context
def create_buffer(ctx):
    ctx.obj = [0 for i in range(dk.DISK_BLOCK_SIZE)]
    click.echo("Created buffer successfully")

@buffer.command('fill')
@click.argument('byte', type=click.INT)
@click.pass_context
def fill_buffer(ctx, byte):
    for i in enumerate(ctx.obj):
        ctx.obj[i] = byte
    click.echo("Filled buffer with values {}".format(byte))

@buffer.command('write')
@click.argument('filename', type=click.STRING)
@click.argument('block', type=click.INT)
@click.pass_context
def write_buffer(ctx, filename, block):
    as_byte_array = bytearray(ctx.obj)
    result = dk.disk_write(filename, block, as_byte_array)
    if result == dk.SUCCESS:
        click.echo("Successfully wrote buffer to block {} in disk {}".format(block, filename))

@buffer.command('copy')
@click.argument('filename', type=click.STRING)
@click.argument('block', type=click.INT)
@click.pass_context
def copy_buffer(ctx, filename, block):
    from_disk = dk.disk_read(filename, block)
    ctx.obj = from_disk
    click.echo("Successfully copied block {} from disk {} into buffer".format(block, filename))

@buffer.command('print')
@click.pass_context
def print_buffer(ctx):
    click.echo("Buffer:")
    click.echo(ctx.obj)

if __name__ == '__main__':
    top()
