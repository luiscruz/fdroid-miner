import click
from git import Repo


@click.command()
@click.argument('branch')
@click.argument('repo_paths', type=click.Path(exists=True), nargs=-1)
def tool(branch, repo_paths):
    """Tool to automatically create a branch in one or multiple repos."""
    with click.progressbar(repo_paths) as bar:
        for repo_path in bar:
            try:
                git = Repo(repo_path).git
                git.checkout('HEAD', b=branch)
            except Exception as e:
                click.secho(
                    'Failed to create branch in {} {}'.format(repo_path, e),
                    fg='red', err=True
                )

if __name__ == '__main__':
    tool()
