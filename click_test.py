import click

@click.command()
@click.option('-m', '--mac', help="enter partial mac address to search")
def parse(mac):
    return mac

if __name__ == '__main__':
    parsed_mac = parse(standalone_mode=False)
    print(parsed_mac)