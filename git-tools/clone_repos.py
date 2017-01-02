import click
import pandas
from pygithub3 import Github
from git import Repo
import json
import os

# authenticate github api
with open('./config.json') as config_file:    
    config = json.load(config_file)
    
gh = Github(user=config.get('github_username'), token=config.get('github_token'))

def gitclone(repo_link, clone_dir):
    try:
        Repo.clone_from(repo_link, clone_dir)
    except Exception as e:
        click.secho('Failed cloning {}'.format(repo_link), fg='red', err=True)
    

@click.command()
@click.option('--clone_dir', default=None, help='Directory where to clone forks. When absent, repositories are not cloned')
@click.argument('csv_file', type=click.Path(exists=True))
def tool(clone_dir, csv_file):
    """Tool to automatically fork and clone repos from csv file. It assumes CSV
    file has at least columns "username" and "repo" """

    df = pandas.read_csv(csv_file)
    for _,(username, repo) in df[["username","repo"]].iterrows():
        try:
            click.secho('Forking {}/{}...'.format(username,repo), fg='blue') 
            fork = gh.repos.forks.create(user=username, repo=repo)
            if clone_dir:
                click.secho('Cloning...', fg='blue') 
                gitclone(fork.clone_url, os.path.join(clone_dir,repo))
            click.secho('Done.', fg='green')
        except Exception as e:
            click.secho('Failed forking {}/{}'.format(username,repo), fg='red', err=True)
    
if __name__ == '__main__':
    tool()