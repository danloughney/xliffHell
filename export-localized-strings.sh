#!/bin/sh

#  export-localized-strings.sh
#  localization
#
#  Created by Daniel Loughney on 1/4/17.
#
set -o verbose

xcodebuild -exportLocalizations -exportLanguage en -localizationPath wevew/localization -exportLanguage en -verbose
