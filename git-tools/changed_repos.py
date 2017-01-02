import click
from git import Repo


@click.command()
@click.argument('repo_paths', type=click.Path(exists=True), nargs=-1)
def tool(repo_paths):
    """Tool to check which repos have changes to be commited."""
    for repo_path in repo_paths:
        try:
            repo = Repo(repo_path)
            if repo.is_dirty():
                print repo_path
        except Exception as e:
            click.secho(
                'Failed to check repo in {} {}'.format(repo_path, e),
                fg='red', err=True
            )


if __name__ == '__main__':
    tool()
