import click
import diskpy as dk

@click.group()
def cli():
    pass

@cli.command('create')
@click.argument('filename', type=click.File('wb'))
@click.option('--size', default=5, help="Size of disk")
def create(filename, size):
    dk.disk_init(filename, size)
    click.echo("Successfully created {}".format(filename))

@cli.command('open')
@click.argument('filename', type=click.STRING)
def open(filename):
    result = dk.disk_open(filename)
    if result == dk.SUCCESS:
        click.echo("Successfully opened {}".format(filename))

if __name__ == '__main__':
    cli()