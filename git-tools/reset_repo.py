import click
from git import Repo



@click.command()
@click.argument('repo_paths', type=click.Path(exists=True), nargs=-1)
def tool(repo_paths):
    """Tool to automatically reset a branch in one or multiple repos."""
    with click.progressbar(repo_paths) as bar:
        for repo_path in bar:
            try:
                repo = Repo(repo_path)
                repo.head.reset(index=True, working_tree=True)
            except Exception as e:
                click.secho('Failed to reset repo in {} {}'.format(repo_path,e), fg='red', err=True)

    

if __name__ == '__main__':
    tool()