import codecs
from urlparse import urlparse

file_in = "./android_repos.txt"
file_out = "./android_repos_ghsearch.txt"
with codecs.open(file_in, 'r') as fi:
    lines = []
    for url in fi:
        parse = urlparse(url)
        path_items = parse.path.strip().split('/')
        if len(path_items) == 3:
            username = path_items[1]
            repo = path_items[2]
            lines.append("%s %s 50\n"%(username, repo))
    #persist data    
    with codecs.open(file_out, "w") as fo:
        fo.writelines(lines)
    