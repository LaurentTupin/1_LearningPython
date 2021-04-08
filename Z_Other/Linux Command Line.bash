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
# delet the directory
rmdir department/legal

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










