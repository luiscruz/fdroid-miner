import xml.etree.cElementTree as ET
import codecs

file_out = "./android_repos.txt"
file_in = "./fdroid.xml"
with codecs.open(file_out, "w") as fo:
    lines = list()
    for _, element in ET.iterparse(file_in):
        if element.tag == "application":
            for source_node in element.iter('source'):
                repo_link = source_node.text
                # get only github repos
                if repo_link and "github" in repo_link:
                    lines.append(repo_link)
    print "Saving %d repositories to \"%s\"."%(len(lines), file_out)
    fo.writelines("\n".join(lines))

