import click
import pandas

@click.command()
@click.argument('csv_file', type=click.Path(exists=True))
def tool(csv_file):
    df = pandas.read_csv(csv_file)
    for i,link in df["github_link"].iteritems():
        print link
        # gh.repos.create.fork()
if __name__ == '__main__':
    tool()