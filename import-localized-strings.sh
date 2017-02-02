#!/bin/sh

#  import-localized-strings.sh
#  localization
#
#  Created by Daniel Loughney on 1/4/17.
#

if [ $# -ne 1 ]
then
	echo "usage $0 language"
	exit 1
fi

xcodebuild -verbose -importLocalizations -localizationPath "$1.xliff"
