# Module to Manage the TV Show info
# Uses Guessit, looks at the file name and parses info
# https://github.com/wackou/guessit

import os
from guessit import guess_file_info
from keith.file_mngr import My_Files

class TV_Shows(object):
	def __init__(self, path):
		self.video_ext = ['.avi', '.mkv', '.mp4', '.m4v', '.mpeg']
		path = os.path.expanduser(path)
		if os.path.isdir(path):
			self.path = path
			my_files = My_Files(self.path)
			my_files.filter_files(self.video_ext, False)
			self.tv_files = my_files.filtered_files
		elif os.path.isfile(path):
				self.path = path
				self.tv_files = list(path)
		else:
			raise NameError('Invalid File Path')

	def get_all_show_info(self):
		self.tv_infos = {}
		for tv_file in self.tv_files:
			self.tv_infos[tv_file] = guess_file_info(tv_file)

	def parse_desired_info(self, show_info):
		my_info = {}
		if show_info['type'] != 'episode':
			print 'Not a TV Show'
			return None
		if not 'series' in show_info:
			raise NameError("Show cannot be determined.")
		else:
			my_info['show'] = show_info['series']
		if not 'season' in show_info:
			if not 'seasonList' in show_info:
				raise NameError("Season cannot be determined.")
			else:
				my_info['season'] = show_info['seasonList'][0]
		else:
			my_info['season'] = show_info['season']
		if not 'episodeNumber' in show_info:
			if not 'seasonList' in show_info:
				raise NameError("Episode cannot be determined.")
			else:
				my_info['episode'] = show_info['episodeList'][0]
		else:
			my_info['episode'] = show_info['episodeNumber']
		return my_info

	
	def _add_show_to_directory(self, show_name):
		if not show_name in self.show_directory:
			self.show_directory[show_name] = {}


	def _add_season_to_directory(self, show_name, season_num):
		if not season_num in self.show_directory[show_name]:
			self.show_directory[show_name][season_num] = {}


	def build_tv_show_directory(self):
		self.show_directory = {}
		for i in self.tv_infos:

			# Ensure that te correct keys are available
			tv_info = self.parse_desired_info(self.tv_infos[i])
			if not tv_info == None:
				self._add_show_to_directory(tv_info['show'])
				self._add_season_to_directory(tv_info['show'], tv_info['season'])
				self._add_episode_to_directory(tv_info['show'], tv_info['season'], tv_info['episode'], i)
	

	def _add_episode_to_directory(self, show_name, season_num, episode_num, path):
		if type(episode_num) == 'list':
			episodes = list(episode_num)
		else:
			episodes = [episode_num]
		for episode in episodes:
			if not episode in self.show_directory[show_name][season_num]:
				self.show_directory[show_name][season_num][episode] = path
			else:
				print 'Episode %s already exists for Season %s of %s.' % (episode, season_num, show_name)



			


