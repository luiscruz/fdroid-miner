import xml.etree.cElementTree as ET
import codecs
import click
import requests
import os

@click.command()
@click.option('--no-cache', default=False, is_flag=True, help='Force downloading F-droid metadata.')
def tool(no_cache):
    file_out = "./android_repos.csv"
    file_in = "./fdroid.xml"
    if not os.path.isfile(file_in) or no_cache:
        url = "https://f-droid.org/repo/index.xml"
        response = requests.get(url, stream=True)
        with open(file_in, "wb") as handle:
            with click.progressbar(response.iter_content(), label='Downloading F-Droid metadata') as bar:
                for data in bar:
                    handle.write(data)
    lines = list()
    for _, element in ET.iterparse(file_in):
        if element.tag == "application":
            for source_node in element.iter('source'):
                repo_link = source_node.text
                last_updated = element.find("lastupdated").text
                app_id = element.find("id").text
                category = element.find("category").text
                # get only github repos
                if repo_link and "github" in repo_link:
                    lines.append((last_updated,repo_link,app_id,category))
    print "Saving %d repositories to \"%s\"."%(len(lines), file_out)
    lines.sort()
    with codecs.open(file_out, "w") as fo:
        fo.write("last_updated,github_link,app_id,category\n")
        fo.writelines("\n".join([",".join(line) for line in lines[::-1]]))
        fo.write("\n")
if __name__ == '__main__':
    tool()