from rar_handler import My_Rar
import os
import sys
from keith.file_mngr import My_Files

# Define Variables
save_path = '~/torrents/extracted'
base_path = '~/torrents/completed'
video_ext = ['.avi', '.mkv', '.mp4', '.m4v', '.mpeg']

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
	sys.exit()

# Print out what needs to be done
print ""
print "The following need to be extracted:"
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