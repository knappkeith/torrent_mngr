import rarfile
import os

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


base_path = '~/torrents'
all_rar, other_vid = get_rars(os.path.expanduser(base_path), ['sample','completed'])
for rar in all_rar:
	rf = rarfile.RarFile(rar)
	for f in rf.infolist():
	    print f.filename, f.file_size

for vid in other_vid:
	print vid