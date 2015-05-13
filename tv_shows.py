# Module to Manage the TV Show info
# Uses Guessit, looks at the file name and parses info
# https://github.com/wackou/guessit

import os
from guessit import guess_file_info
from keith.file_mngr import My_Files
import copy

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
		self.get_all_show_info()
		self.build_tv_show_directory()

	def get_all_show_info(self):
		self.tv_infos = {}
		for tv_file in self.tv_files:
			self.tv_infos[tv_file] = guess_file_info(tv_file)

	def parse_desired_info(self, show_info):
		my_info = {}
		gtg = True
		if show_info['type'] != 'episode':
			my_info['show'] = '??'
			gtg = False
		if not 'series' in show_info:
			my_info['show'] = '??'
			gtg = False
		else:
			my_info['show'] = show_info['series']
		if not 'season' in show_info:
			if not 'seasonList' in show_info:
				my_info['season'] = '??'
				gtg = False
			else:
				my_info['season'] = show_info['seasonList'][0]
		else:
			my_info['season'] = show_info['season']
		if not 'episodeNumber' in show_info:
			if not 'seasonList' in show_info:
				my_info['episode'] = '??'
				gtg = False
			else:
				my_info['episode'] = show_info['episodeList'][0]
		else:
			my_info['episode'] = show_info['episodeNumber']
		return my_info, gtg


	def build_tv_show_directory(self):
		self.show_directory = {}
		for i in self.tv_infos:

			# Ensure that te correct keys are available
			tv_info, parsed = self.parse_desired_info(self.tv_infos[i])
			if parsed == None:
				self._add_show_to_directory(tv_info['show'])
				self._add_season_to_directory(tv_info['show'], tv_info['season'])
				self._add_episode_to_directory(tv_info['show'], tv_info['season'], tv_info['episode'], i)
			else:
				print "TV01: Unable to parse %s, skipping! (%s, %s, %s)" % (i, tv_info['show'], tv_info['season'], tv_info['episode'])
	
	def determine_copy(self, slave_directory):
		my_show_directory = copy.deepcopy(self.show_directory)
		my_slave_directory = copy.deepcopy(slave_directory)
		for show in my_show_directory:
			if show in my_slave_directory:
				for season in my_show_directory[show]:
					if season in my_slave_directory[show]:
						for episode in my_show_directory[show][season]:
							if episode in my_slave_directory[show][season]:
								del self.show_directory[show][season][episode]


	def _add_show_to_directory(self, show_name):
		if not show_name in self.show_directory:
			self.show_directory[show_name] = {}


	def _add_season_to_directory(self, show_name, season_num):
		if not season_num in self.show_directory[show_name]:
			self.show_directory[show_name][season_num] = {}


	def _add_episode_to_directory(self, show_name, season_num, episode_num, path):
		if type(episode_num) == 'list':
			episodes = list(episode_num)
		else:
			episodes = [episode_num]
		for episode in episodes:
			if not episode in self.show_directory[show_name][season_num]:
				self.show_directory[show_name][season_num][episode] = path
			else:
				print 'TV02: Episode %s already exists for Season %s of %s.' % (episode, season_num, show_name)



			


