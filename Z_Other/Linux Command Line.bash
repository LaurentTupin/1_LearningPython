# GIT
sudo apt install git
git clone git://github.com/scottsimpson/commandlinebasics

# Structure
Command: ls
Options: -lh
Arguments: /usr/bin

# Text Navigation Shortcuts
press tab TWICE to have suggestions of command that start with the char you filled
CTL + A: move to begining of line
CTL + E: move to end of line
CTL + <= : move to left one word
CTL + => : move to right one word
CTL + U: Crop from cursor to start
CTL + K: Crop from cursor to end
CTL + Y: Paste Cropped Text
CTL + SHIFT + C: Copy to clipboard
CTL + SHIFT + V: Paste from clipboard
Up Arrow: Recall previous commands
Down Arrow: Scroll previous commands
CTL + R: Search commands history
CTL + C: Cancel command

# Documentation
h
	# help
man ls
ls --help
	# will tell information about a command
apropos
	# give list of command and their description
	

# Commands
ls
	# list content of directory
ls -l
	# long listing
	#  show file with its characteristics
ls -l Desktop/
	# long listing in Desktop/
clear
	# clear the screen

# FILE
file txtFile.txt
	# kind of file it is
stat txtFile.txt
	# extend information of the file
cd
	# change directory
cd.. 
	# go a folder upward
cd../..
	# go 2 folder upward
cd../../finance
	# go 2 folder upward + Go to folder Finance
pwd
	# check where you are : your current directory
cd -
	# going back to the previous current directory you were in
cd
	# go back to your home folder

# Focus on ls
ls
	# list content of directory
ls -l
	# long listing
	#  	show file with its characteristics
	#	d/-   directory / file
	#	Authorization
	# 	size in BITES
ls -lh
	# size readable: k , M, G
	
# Create folder
mkdir new_folder
mkdir department/new_folder
mkdir department/new_folder department/new_folder2 department/new_folder3
# Parent + child folder
mkdir -p department/parent_new_folder/child_new_folder
# Remove empty directory
rmdir department/legal/folder_to_delete
	# only delete the folder if he is empty

# Copy files
cp file.txt file_copy.txt
cp file.txt department/legal/

# Moving a file
mv file.txt department/legal/
mv department/legal/file.txt .
	#   . is the current folder, check with LS that the file is right there

# Several file at a time
mv *.txt department/legal/
	# All txt file has gone to LEGAL
mv department/legal/* .
	# All the files in LEGAL in current folder

# Delete files
rm file.txt
	# NO TRASH CAN !!!!
	# DELETED FOREVER
rm file?.txt	
	# delete file2, file3, file4  .txt

# Delete all files in a Directory
rm -r department/legal/
# delete the directory
rmdir department/legal

# Delete all files in a Directory + the sub-Dirs + the Directory
rm -rf department/legal/

# Find files
find . -name "poe*"
find . -name "d*"
find ~/Documents/ -name "d*"

# User roles and sudo
ls /root
	# cant work: Perimission denied
sudo ls /root
sudo -k
	# Give up privilege - password not saved anymore
sudo -s
	# Go to be a SUPER USER
exit
	# Exit SUPER USER privilege



# File Permissions
rwxrwxrwx
rwxr-xr-x
	# 3 first letter: User
	# 3 after: group
	# 3 ending: Others
	# Read / write / execute
	
# Change permissions
chmod 

# Tableau des valeurs
		Read : 4		Write: 2		Execute: 1			Result		Letters 
User	r 				w				x					7			u+rwx
Group	r				-				x					5			g=r
Others	r				-				-					4			o-rwr
All																		a=rwx
	# + Add permissions
	# - Remove permissions
	# = Reset permissions (add permissions but remove all the one not here)

# Exemples
chmod 777 filename.sh
chmod a=rwx filename.sh
==>	rwxrwxrwx
chmod 755 filename.sh
chmod u+rwx, g=rx, o=rx filename.sh
==> rwxr-xr-x
chmod 700 filename.sh
chmod u=rwx, g-rwx, o-rwx filename.sh
==>	rwx------

# Print out content of file
cat filename.sh
	"
	#! /usr/bin/env bash
	echo -e "Hello From test Script"
	"

# Create Blank Files
touch newFile.sh

# open the file in text editor
nano newFile.sh

# Links (pointer of file)
	# Hard link (link to the underlying data and not to the file itself)
	# All file are actually HARD LINK to their underlying datas
ln fileToLink.txt linkName.txt
	# Symbolic (link to the original file) (relative path) 
ln -s fileToLink.txt linkName.txt


# Pipe
Send command as input for another command
#wc: function that say: nb of rows, nb of words, nb of char (+1)
echo "hello"
	hello
echo "hello" | wc
	1	1	6

# cat (Print content of file) / head (First 10 lines) / tail (Last 10 lines)
head -n5 file.txt	
	# First 5 rows
cat file.txt | cat -n
	# Ca numerote le texte
cat file.txt | cat -n | tail -n5
	# Last 5 lines with numerotation  (51 to 55)
cat file.txt | tail -n5 | cat -n 
	# Last 5 lines with numerotation  (1 to 5)
# less: navigate through a long file (f / b / space / enter)
less file.txt

# grep : print depending on patterns / regex
grep "the" file.txt
	# Will show the text with 'the' highlighted (only the rows with 'the' present
grep -n "the" file.txt
	# With numerotation of lines
grep -i "the" file.txt
	# Case NON Sensitive
grep -v "the" file.txt
	# print all the one WITHOUT 'the'

# REGEX : -E
grep -E "[hijk]" file.txt
	# []: means 'or'
grep -E "\w{6,}" file.txt
	# words of 6 or more characters













