#!/bin/sh
#
# Run TnT for English texts
# reading the input from stdin and writing the output stdout
#
# oeze, Mon Mar 29 01:14:49 CEST 2004

#--- Edit this line if necessary ----------------
TNTHOME=`dirname \`dirname \\\`fullname $0\\\`\``
#------------------------------------------------
cd $TNTHOME
$TNTHOME/tnt $* - 
