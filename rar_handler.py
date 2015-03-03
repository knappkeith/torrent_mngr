from unrar import rarfile
import os
from keith.file_mngr import My_Files

class My_Rar(object):

	def __init__(self, rar_dir, save_dir):
		#Start the class
		#check to make sure dirs are valid
		rar_dir = os.path.expanduser(rar_dir)
		if os.path.isdir(rar_dir):
			self.rar_dir = os.path.expanduser(rar_dir)
		else:
			raise NameError('Invalid RAR Directory')
		save_dir = os.path.expanduser(save_dir)
		if os.path.isdir(save_dir):
			self.save_dir = os.path.expanduser(save_dir)
		else:
			raise NameError('Invalid Save Directory')

		# Set up all the things
		self._get_rars_files()
		self._get_rar_objs()
		self._get_extracted_names()
		self.get_total_size()
		self.total_size = 0


	def _get_rars_files(self):
		# Initialize My_File object
		self.rar_files = My_Files(self.rar_dir)

		# Filter out everything but .rar
		self.rar_files.filter_files(['.rar'], False)


	def _get_rar_objs(self):
		self.rar_objs = []
		for i in self.rar_files.filtered_files:
			self.rar_objs.append(rarfile.RarFile(i))
	

	def _get_extracted_names(self):
		self.rar_ext_names = []
		for i in self.rar_objs:
			self.rar_ext_names.append(i.infolist()[0].filename)
	

	def remove_extracted_names(self, extracted_names):
		# Remove RARs that have been extracted already
		extract_list = list(extracted_names)
		if not self.rar_objs:
			return
		for i in extract_list:
			try:
				self.rar_ext_names.remove(i)
				try:
					self.rar_objs.remove(self._find_rar_by_name(i))
				except:
					print "Unable to remove %s from Extract queue" % str(i) 
			except:
				print i + " does not exist as a RAR extraction!"


	def get_total_size(self):
		self.total_size = 0
		for rar_obj in self.rar_objs:
			self.total_size += rar_obj.infolist()[0].file_size


	def _find_rar_by_name(self, name):
		for rar_obj in self.rar_objs:
			if rar_obj.infolist()[0].filename == name:
				return rar_obj
		return None


	def extract(self, rar_to_extract, extract_path=None):
		# Extract one current RAR
		if extract_path is None:
			extract_path = self.save_dir
		target_path = os.path.expanduser(extract_path)
		if not os.path.isdir(target_path):
			raise NameError('Invalid Target Directory')
		rar_to_extract.extractall(target_path)
		print "%s was extracted to % s" % (rar_to_extract.filename, rar_to_extract.infolist()[0].filename)
		

	def extract_all(self, extract_path=None):
		# Extract all current RAR
		if extract_path is None:
			extract_path = self.save_dir
		for rar in self.rar_objs:
			self.extract(rar, extract_path)
