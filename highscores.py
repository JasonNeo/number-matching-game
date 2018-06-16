import json
import time



class Highscores():
	"""Creates a highscore board"""
	def __init__(self, filename):
		self.filename = filename


	def del_highscores(self):
		"""Deletes the highscore board and replace with EMPTY & 0"""
		try:
			with open(self.filename) as f_obj:
				contents = f_obj.read()
		except FileNotFoundError:
			print('File for highscores not found! Call 016 733 7043 for assistance.')
		else:
			json_contents = json.loads(contents)
			for item in json_contents:
				item['player_name'] = 'EMPTY'
				item['player_score'] = 0
			self.save_highscores(json_contents)


	def extract_score(self, json):
		"""Extracts player's score from json"""
		try:
			return int(json['player_score'])
		except KeyError:
			return 0


	def format_time(self, secs):
		"""Returns time in mm:ss format"""
		return time.strftime("%M:%S", time.gmtime(secs))


	def get_highscores(self):
		"""File handler, reads and returns contents in JSON"""
		try:
			with open(self.filename) as f_obj:
				contents = f_obj.read()
		except FileNotFoundError:
			print('File for highscores not found! Call 016 733 7043 for assistance.')
		else:
			json_contents = json.loads(contents)
			return sorted(json_contents, key=self.extract_score)


	def print_highscores(self):
		"""Prints highscores to interface"""
		try:
			with open(self.filename) as f_obj:
				contents = f_obj.read()
		except FileNotFoundError:
			print('File for highscores not found! Call 016 733 7043 for assistance.')
		else:
			json_contents = json.loads(contents) #read as json
			print('\n{0:4s}\t{1:20s}\t{2:8s}'.format('Rank', 'Name', 'Score(mm:ss)'))
			print()
			for item in json_contents:
				player_rank = json_contents.index(item) + 1
				player_name = item['player_name']
				player_score = self.format_time(item['player_score'])
				print('{0:4d}\t{1:20s}\t{2:8s}'.format(player_rank, player_name, player_score))


	def save_highscores(self, contents):
		"""Saves the newest highscores"""
		try:
			with open(self.filename, 'w') as f_obj:
				f_obj.write(json.dumps(contents)) #save as json
		except FileNotFoundError:
			print('File for highscores not found! Call 016 741 6243 for assistance.')