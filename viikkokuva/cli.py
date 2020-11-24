try:
    import click
    import click_log
except ImportError:
    import sys
    print("cli extras required to run this")
    sys.exit(1)

click_log.basic_config()

import requests

from . import common

PICTURE_CHOICES = [choice.name for choice in common.PictureChoice]


@click.command()
@click.option("--dry-run", is_flag=True, help="Do not actually call the API")
@click.argument("choice", type=click.Choice(PICTURE_CHOICES))
@click_log.simple_verbosity_option()
def main(choice, dry_run):
    """Create task to take weekly/monthly pic in Microsoft To-Do

    The argument is either week or month, for weekly and monthly pictures,
    respectively.

    """
    common.create_task(common.PictureChoice[choice], dry_run=dry_run)
