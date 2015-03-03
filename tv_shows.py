import os

def determine_show_name_from_path(file_path):
	pass

def determine_show_name_from_file(file_name):
	if '/' in file_name:
		return determine_show_name_from_path(file_name)
	pass

def determine_show_season_from_path(file_path):
	pass

def determine_show_season_from_file(file_name):
	pass

def determine_show_episode_from_path(file_path):
	return determine_show_episode_from_file(file_path)

def determine_show_episode_from_file(file_name):
	pass
