#! /bin/bash
# EAGLE CAD X/Y extractor script
# Spencer Wright
# 2015.01.21
#
# Questions? email snwright@gmail.com
#
# This work is licensed under CC-BY 4.0
# http://creativecommons.org/licenses/by/4.0/
#
# This shell script takes a plain text file (the result of exporting a partlist from EAGLE CAD) as argument
# and creates a new CSV file formatted with part names, x positions, and y positions.
# usage: go to the directory where this file is stored, then type:
# 		./xy_script.sh [filename]
# And the script will generate a file named [filename_xy] that contains:
#		Part name,xpos,ypos,
#		C1,45,14,
#		C2,24.9,52,
#		C3,24.9,53.2,
#		...
# 

partlist="$1"						#sets variable from stdin
xy=$1_xy							#sets filename for output

touch $1_xy							#creates output file
echo Part\ name,xpos,ypos, > $xy		#writes column names to first line of output

tail -n +12 $partlist |				#skips the first 11 lines of the file, which contain eagle output
awk 'match($0, /\([^)]+\)/) {print $1,substr($0, RSTART, RLENGTH)}' |	#parses each line and returns the first word (part namesme), plus the entire (x,y) coordinate
sed -e 's/ (/,/' |					#removes the space after the part name and the first paren and replaces them with a comma
sed -e 's/ /,/' |					#removes the space between xpos and ypos and replaces it with a comma
sed -e 's/)/,/' >>$xy				#removes the close paren and replaces it with a comma