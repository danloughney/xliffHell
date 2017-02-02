# after completing translation, create the pList files for the app since the import tool cannot
# provide the target language code (it, ru, etc.)
# the translated XLIFF must be in the local directory
#
from __future__ import print_function
import xml.etree.ElementTree as ET
import sys
import os
from const import namespace, appPath

def writeSettingsFromNode(targetLanguage, treeNode):
    langFolder = "{0}.lproj".format(targetLanguage)
    
    settingsPath = treeNode.attrib["original"].replace("en.lproj", langFolder)
    print(settingsPath)

    with open(settingsPath, 'w', encoding='utf-16') as f:
        for transUnit in treeNode.findall("./{0}body/{0}trans-unit".format(namespace)):
            id = transUnit.attrib["id"]
            source = transUnit.find("{0}source".format(namespace))
            target = transUnit.find("{0}target".format(namespace))

            f.write('/* {0} */\n'.format(source.text))
            f.write('"{0}" = "{1}";\n'.format(id, target.text))
            f.write('\n')

def main():    
    os.system("pwd")
    
    targetLanguage = sys.argv[1]
    
    tree = ET.parse("./final translations/{0}.xliff".format(targetLanguage))
    
    # set the target language on the file node
    for fileNode in tree.findall("./{0}file".format(namespace)):
        if ("settings.bundle" in fileNode.attrib["original"]):
            writeSettingsFromNode(targetLanguage, fileNode)

if __name__ == "__main__":
    main()
