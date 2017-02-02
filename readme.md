XLIFF Hell

Python3 scripts for living in my own XLIFF Hell


- const.py: 
  put your app source path in here.

- export-localized-strings.sh: 
  run this first to export your XLIFF.

- correct-en-xliff.py: 
  no idea why, but XCode ignores all of the text strings in my plist and settings.nib. It also does some other weird stuff. This script corrects that. It modifies the XLIFF that you get from XCode. Run this before getting the XLIFF translated.

- import-localized-strings.sh: 
  run this on the xliff file you get back from the translator. Takes the language code of the file as input. Expecting you'll get it.xliff back from the translator for Italian so use import-localized-strings.sh it

- xliff-to-settings.py:
  after importing the xliff, run this to import the forgotten settings.bundle translations. as in python3 xliff-to-settings.py it

- xliff-to-plist.py:
  same as xliff-to-settings for the plist strings
