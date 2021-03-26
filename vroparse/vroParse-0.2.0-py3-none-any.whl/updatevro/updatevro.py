##  Created by Jim Sadlek
##  Copyright © 2021 VMware, Inc. All rights reserved.
##
import xml.dom.minidom
import sys
import os.path
import argparse

Description = """
This script updates vRO Workflow XML that contain embedded Scriptable Tasks with code previously parsed out and stored in '.parsevro' folders.
By: Jim Sadlek - VMware, Inc.

This must be run from the vRO Package's top-level folder, which contains a 'workflows/src/main/resources/Workflow' subfolder.
This is usually run before a 'mvn package vrealize:push' command when using vRealize Build Tools, or importing from a folder with native vRO.'
"""
parser = argparse.ArgumentParser(description=Description,formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v','--verbose',action='store_true',help='Display verbose logging output')
args = parser.parse_args()

#####################################
## update xml scriptable task elements 
## with edited program code from
## discrete files stored in the form: <path>/.parsevro/<wfName>_<taskName>_<displayName>.js
def updateXML(xmlfile):
  dirName = os.path.dirname(xmlfile)
  wfName = os.path.splitext(os.path.basename(xmlfile))[0]
  subDirName = "%s/.parsevro" % (dirName)

  # use the parse() function to load and parse an XML file
  doc = xml.dom.minidom.parse(xmlfile)
  
  # get a list of XML tags from the document and print each one
  wfItems = doc.getElementsByTagName("workflow-item")
  if args.verbose: print("%d workflow-item(s): (not all are Scriptable Tasks)" % wfItems.length)

  for wfItem in wfItems:
    typeAttr = wfItem.getAttribute("type")
    #print("type: %s" % typeAttr)
    if typeAttr == "task":
      taskName = wfItem.getAttribute("name")
      if args.verbose: print("\ttaskName: %s" % taskName)

      displayNameItem = wfItem.getElementsByTagName("display-name")[0]
      for node in displayNameItem.childNodes:
        displayName = node.data
        if args.verbose: print("\tdisplay-name: %s" % displayName)

      for scriptItem in wfItem.getElementsByTagName("script"):
        for node in scriptItem.childNodes:
          script = node.data
          #print("\nscript: \n%s" % script)

      fileName = "%s/%s_%s_%s.js" % (subDirName, wfName, taskName, displayName)
      if args.verbose: print("\tReading contents of fileName:\n\t%s" % fileName)

      if not os.path.isfile(fileName):
        print("%s does not exist.  Please run parsevro again."%fileName)
        continue
        
      # Fix for TKTVSDL-388
      # check for file names in absolute file path form
      prefix = is_filename_safe(subDirName, fileName)
      if prefix == subDirName:
        try:
          with open(fileName,"r") as f:
            script = f.read()

        except IOError:
          print ("Error: reading file: ", fileName)


      scriptItem.childNodes[0].data = script

    try:
        with open(xmlfile,"w+") as f:
            doc.writexml(f)

    except IOError:
        print ("Error: writing XML file: ", xmlfile)

#####################################
## provided by vSDL Service Desk team
## TKTVSDL-388
def is_filename_safe(dirName, fileName):
    if not dirName.endswith('/'):
        dirName += '/'
    abs_dirname = os.path.abspath(dirName)
    abs_filename = os.path.abspath(fileName)
    return os.path.commonprefix([abs_dirname,abs_filename])

###########
## main
def main():
  rootDir = './workflows/src/main/resources/Workflow'
  rootDir = os.path.abspath(rootDir)
  
  if not os.path.isdir(rootDir):
    print("Looking for XML files in %s"%rootDir)
    print("Are you in the right location?  CD to the top leve of a 'mixed' project that contains the %s sub folder structure."%rootDir)
    exit

  print("Updating XML ...")
  
  for dirName, subdirList, fileList in os.walk(rootDir):

    if os.path.basename(dirName) == ".parsevro":
      continue

    if len(fileList) > 0:
      for filename in fileList:
        if filename.endswith(".xml"):
          if args.verbose: print("\n*** PROCESSING Workflow XML filename: %s"%filename) 
          updateXML(dirName+"/"+filename)


#if __name__ == "__main__":
#  main()