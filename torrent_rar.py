from unrar import rarfile
import os
import sys

def is_filtered(path, filter_list):
	if filter_list is None:
		return True
	for a in filter_list:
		if a.upper() in path.upper():
			return False
	return True

def get_rars(root_dir, filter_dir=None):
	rar_files = []
	other_files = []
	for root, dirs, files in os.walk(root_dir):
		if is_filtered(root, filter_dir):
			rar_name = None
			for name in files:
				if os.path.splitext(name)[1] == '.rar':
					rar_name = os.path.join(root,name)
					rar_files.append(rar_name)
			if rar_name is None:
				for name in files:
					if os.path.splitext(name)[1] in ['.avi', '.mkv', '.mp4', '.m4v', '.mpeg']:
						other_files.append(os.path.join(root,name))

	return rar_files, other_files

def get_completed(root_dir):
	video_files = []
	for root, dirs, files in os.walk(root_dir):
		for name in files:
			if os.path.splitext(name)[1] in ['.avi', '.mkv', '.mp4', '.m4v', '.mpeg']:
				video_files.append(os.path.join(root,name))
	return video_files

def is_completed(to_check, completed):
	if completed is None:
		return True
	for a in completed:
		if to_check.upper() in a.upper():
			return False
	return True

save_path = '~/torrents/Completed'
save_path = os.path.expanduser(save_path)
base_path = '~/torrents'
base_path = os.path.expanduser(base_path)

all_rar, other_vid = get_rars(base_path, ['sample','completed'])

completed = get_completed(save_path)

print ""
print "Available RARs:"
for rar in all_rar:
	rf = rarfile.RarFile(rar)
	if is_completed(rf.infolist()[0].filename, completed):
		rf.extractall(save_path)
		print "Extracted:  " + os.path.split(rar)[1]
		


	# for f in rf.infolist():
	#     print f.filename

# print ""
# print "Other Available Videos:"
# for vid in other_vid:
# 	print vid



# print ""
# print "Completed Videos:"
# for a in completed:
# 	print a

# print ""
# print "Checking what to extract:"
# for rar in all_rar:
# 	rf = rarfile.RarFile(rar)
# 	for f in rf.infolist():
# 		if is_completed(os.path.split(f.filename)[1], completed):
# 			print "should extract " + f.filename

# print ""
# print "Checking what to copy:"
# for vid in other_vid:
# 	if is_completed(os.path.split(vid)[1], completed):
# 		print "Should copy: " + os.path.split(vid)[1]
