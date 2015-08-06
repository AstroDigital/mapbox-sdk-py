import logging

import click

import mapbox


class MapboxException(click.ClickException):
    pass

def _is_numeric(x):
    try:
        float(x)
    except:
        return False
    return True

@click.command(short_help="Geocode an address.")
@click.option('--access-token', help="Your access token")
@click.option('--forward', default=False, help="Perform a forward geocode")
@click.option('--reverse', default=False, nargs=2, type=float, help="Perform a reverse geocode")
@click.pass_context
def geocode(ctx, access_token, forward, reverse):
    """Geocode an address"""
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')
    geocoder = mapbox.Geocoder(access_token=access_token)

    if reverse and forward:
        raise MapboxException('Cannot use forward and reverse geocoding simultaneously')

    if not (reverse or forward):
        raise MapboxException('You must specify --forward or --reverse (but not both)')

    if forward:
        resp = geocoder.forward(forward)
    elif reverse:
        if len(reverse) != 2:
            raise MapboxException('Reverse geocoding requires a query in decimal longitude,latitude format, e.g. --reverse="-100,37.7"')
        resp = geocoder.reverse(str(reverse[0]), str(reverse[1]))

    if resp.status_code == 200:
        click.echo(resp.text)
    else:
        raise MapboxException(resp.text.strip())

if __name__ == '__main__':
    geocode()