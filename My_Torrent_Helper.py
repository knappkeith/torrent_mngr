#!/usr/local/bin/python
from rar_handler import My_Rar
import os
import sys
from keith.file_mngr import My_Files
from tv_shows import TV_Shows

# Define Variables
save_path = '~/torrents/extracted'
base_path = '~/torrents/completed'
video_ext = ['.avi', '.mkv', '.mp4', '.m4v', '.mpeg']
network_path = '/Volumes/Public/Shared Videos/TV Shows'
# network_path = '/Users/keith/torrents/test_network'

# Initialize Needed Classes
my_rar = My_Rar(base_path, save_path)
my_completed = My_Files(save_path)

# Get Completed File Names
my_completed.filter_files(video_ext, False)
my_completed_files = my_completed.file_name_only(my_completed.filtered_files)

# Remove Completed Files
my_rar.remove_extracted_names(my_completed_files)

# Get Total Size
my_rar.get_total_size()

# Check for rars to Extract
if not my_rar.rar_objs:
	print 'Nothing to Extract, all up-to-date'
else:

	# Print out what needs to be done
	print ""
	print "The following needs to be extracted:"
	for i in my_rar.rar_ext_names:
		print i
	print ""
	print "A total of " + str(len(my_rar.rar_objs)) + " file(s) and " + str(my_rar.total_size/1024/1024) + " Mb."

	# Ask to continue
	answer = raw_input('Would you like to continue(Y/N)?:')
	if not (answer.upper() == 'Y' or answer.upper() == 'YES'):
		print 'nevermind'
		sys.exit()

	# Extract ALL THE THINGS
	my_rar.extract_all()

# Check for Network Path
if not os.path.isdir(network_path):
	print 'The Network Path %s is not currently available!' % network_path
	sys.exit()

# Ask to continue
answer = raw_input('Would you like to start copying to the Network(Y/N)?:')
if not (answer.upper() == 'Y' or answer.upper() == 'YES'):
	print 'nevermind'
	sys.exit()

# Get all of the TV Shows from both directories
a = TV_Shows(save_path)
b = TV_Shows(network_path)

# Determine which files need to be copied
a.determine_copy(b.show_directory)

# print each file to copy
for show in a.show_directory:
	for season in a.show_directory[show]:
		for episode in a.show_directory[show][season]:
			print 'Episode %s in season %s of %s needs to be copied' % (episode, season, show)