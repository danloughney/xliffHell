from __future__ import print_function
import xml.etree.ElementTree as ET
import re
import os
from xml.dom import minidom
from const import *

xliff = "./en.xliff"

ET.register_namespace("", _namespace)


def ns(tag):
    global namespace
    return namespace + tag

def createXLIFFFileNode(tree, originalPath):
    global namespace
    
    # create the file object, header and body
    #<file original="Localizable.strings" source-language="en" datatype="plaintext">
    #<header>
    #    <tool tool-id="com.apple.dt.xcode" tool-name="Xcode" tool-version="8.2.1" build-num="8C1002"/>
    #</header>
    
    # if this <file> exists, first remove it
    for fileNode in tree.findall("./{0}file".format(namespace)):
        if (fileNode.attrib["original"] == originalPath):
            tree.getroot().remove(fileNode)

    fileElement = ET.SubElement(tree.getroot(), ns("file"), { "original" : originalPath,
                                "source-language" : "en",
                                "datatype" : "plaintext" })
    headerElement = ET.SubElement(fileElement, ns("header"))
    ET.SubElement(headerElement, "tool", { "tool-id" : "com.apple.dt.xcode",
                              "tool-name" : "Xcode",
                              "tool-version" : "8.2.1",
                              "build-num" : "8C1002"})
    bodyElement = ET.SubElement(fileElement, ns("body"))

    return bodyElement

def writeXLIFF(root):
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")

    with open(xliff, "w", encoding='utf-8') as f:
        f.write(xmlstr)
        f.close()

def getRootStringsToXLIFF(tree, sourcePath):
    print("getRootStringsToXLIFF")
    
    global xliff
    
    bodyElement = createXLIFFFileNode(tree, sourcePath)
    
    # create all of the trans-units
    #<trans-unit id="%@ from %@ dated %@">
    #    <source>%1$@ from %2$@ dated %3$@</source>
    #    <note>{photo or video} from {some name} dated {some date}</note>
    #        </trans-unit>
    
    with open(sourcePath, "r", encoding="utf-16") as f:
        for line in f:
            x = line.split("=")
            if (len(x) == 2):
                ID = x[0].replace('"', '').replace(' ', '')
                text = x[1].replace("\n", "").replace(";", "").replace(' "', '').replace('"', '')
                        
                transElement = ET.SubElement(bodyElement, ns("trans-unit"), { "id" : ID })
                sourceElement = ET.SubElement(transElement, "source")
                sourceElement.text = text
                noteElement = ET.SubElement(transElement, "note")
                noteElement.text = ID

def getPListStringsToXLIFF(xliffTree, sourcePath):
    print("getPListStringsToXLIFF")
    global namespace
    
    key = ""
    value = ""
    
    bodyElement = createXLIFFFileNode(xliffTree, "wevew/Base.lproj/Info.plist")

    plistTree = ET.parse(sourcePath)
    for element in plistTree.iter():
        if (key != ""):
            value = element.text
        
            transElement = ET.SubElement(bodyElement, ns("trans-unit"), { "id" : key })
            sourceElement = ET.SubElement(transElement, "source")
            sourceElement.text = value

            print("writing", key, value)
            key = ""
            value = ""
        
        if (element.text == "NSBluetoothPeripheralUsageDescription" or
            element.text == "NSCameraUsageDescription" or
            element.text == "NSLocationWhenInUseUsageDescription" or
            element.text == "NSMicrophoneUsageDescription" or
            element.text == "NSPhotoLibraryUsageDescription" or
            element.text == "CFBundleName" or
            element.text == "CFBundleShortVersionString"):
                key = element.text


def removeLocalizedStringsSection(tree):
    #for some reason, xcode is dropping two of these sections into the XLIFF on export
    print("\nremoveLocalizedStringsSection")
    
    for fileNode in tree.findall("./{0}file".format(namespace)):
        if (fileNode.attrib["original"] == "Localizable.strings"):
            print("removing Localizable.strings")
            tree.getroot().remove(fileNode)

def main():
    os.system("pwd")
    
    tree = ET.parse(xliff)

    getRootStringsToXLIFF(tree, appPath + "wevew/settings.bundle/en.lproj/root.strings")

    getPListStringsToXLIFF(tree, appPath + "wevew/Base.lproj/Info.plist")

    removeLocalizedStringsSection(tree)
    
    writeXLIFF(tree.getroot())


if __name__ == "__main__":
    main()


