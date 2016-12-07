import click
import pandas
from pygithub3 import Github, exceptions as gh_exceptions
from urlparse import urlparse

def get_user_and_repo(github_url):
    parse = urlparse(github_url)
    path_items = parse.path.strip().split('/')
    if len(path_items) == 3:
        username = path_items[1]
        repo = path_items[2]
        return pandas.Series({"username": username, "repo": repo})
    return pandas.Series({"username": None, "repo": None})

def get_github_info(row):
    try: 
        repo=gh.repos.get(user=row["username"], repo=row["repo"])
        contributors = gh.repos.list_contributors(user=row["username"], repo=row["repo"]).all()
        n_contributors = len(contributors)
        n_commits = sum(map(lambda x: x.contributions, contributors))
        return pandas.Series({
            "forks":repo.forks_count,
            "stars":repo.stargazers_count,
            "created_at":repo.created_at,
            "contributors": n_contributors,
            "commits": n_commits,
        })
    except gh_exceptions.NotFound:
        return None
        
# authenticate github api
with open('./config.json') as config_file:    
    config = json.load(config_file)
    
gh = Github(user=config.get('github_username'), token=config.get('github_token'))

@click.command()
@click.option('--n', default=50)
@click.argument('android_repos', type=click.Path(exists=True))
def tool(n,android_repos):
    """Tool to get repositories information given a file with GitHub links."""
    df = pandas.read_csv(android_repos)
    #get username and repos and clean NAs
    df = df.join(df['github_link'].apply(get_user_and_repo))
    df = df.dropna(subset=["username","repo"], how="any")
    #github info
    df=df.head(int(n*1.2))
    df = df.join(df.apply(get_github_info, axis="columns"))
    df.head(n).to_csv("experiment_table.csv")
    
if __name__ == '__main__':
    tool()