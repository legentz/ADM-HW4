import pandas as pd
import os

# separators
# todo: need to assert separators
COMMA = ','
TAB = '\t'
SPACE = ' '

'''
The class below is meant to be a simple wrapper with the main purpose of making life easier to the user while working 
with big input file, obviously, through the usage of Pandas API.
Hence, the Jupyter notebook will be lighter and simpler to read (Yeah, I know, It should be improved with further code reuse).

The provided datasets are divided in multiple file (one per month), so the user could freely feed a list of file_path and start iterating 
as they were concatenated, in chunk. 

Due to a lack of time, this piece of code was not engineered too much, so, I presume is not practical to use it outside this context
outside of this homework without further modifications. But, hey, let's dive into it anyway...
'''
class Loader:

	# Constuctor
	# 	csv 	-> has to be a list of tuples (eg. [('Month_name', 'file_path') )] containing info about the file to load (for each month)
	# 	nrows 	-> has to be an int, indicating the no. of lines we want to to load for each file at max (maily used for debug purposes)
	# 	chunksize -> has to be an int, indicating the no. of lines (batch) that are going to be taken into account when reading a file line-by-line
	# 	separator -> has to be a string, containing the separator used within input files
	def __init__(self, csv=None, nrows=None, chunksize=10000, separator=COMMA):

		# check csv type
		assert type(csv) == list

		# check csv data
		# (es. (Jan, data/file.csv) <-- tuple)
		for f in csv:
			assert os.path.isfile(f)

		self.csv = csv
		self.chunksize = chunksize
		self.separator = separator
		self.nrows = nrows

		# for later use
		self.to_merge = None
		self.to_merge_direction = None
		self.to_merge_on = None

	# handle a list queue-like where all csv
	# are being contained
	def __get_csv(self):
		if len(self.csv) == 0:
			return False
		return self.csv[0]

	# get line with columns
	def get_columns(self, nline=0):
		with open(self.csv, 'r') as f:
			for i, line in enumerate(f):
				if i == nline:
					return line.rstrip('\n').split(self.separator)

	# This function is useful to merge a file to another that is being yielded in chunks. Be careful that
	# the file being merged is NOT iterable, so, it has to fit in your memory :)
	# 
	#	csv -> has to be a string, indicating the path of the file to merge
	#	on -> has to be a tuple, containing the left and right attributes to merge on
	# 	direction -> has to be a string, indicating the direction of the merge
	# 	usecols -> has to be a list, containing the no. or the names of the columns we want to load (and save memory)
	# 	separator -> has to be a string, containing the separator used within merge file
	# 	drop_on_columns -> has to be a bool, indicating whether or not to drop the columns that were used for merging
	def merge(self, csv=None, on=None, direction='left', usecols=[], separator=COMMA, drop_on_columns=False):

		# check csv path
		assert os.path.isfile(csv)
		assert type(on) == tuple and len(on) > 0

		# take precise columns only into account
		if len(usecols) > 0:
			self.to_merge = pd.read_csv(csv, usecols=usecols, sep=separator)

		# load all columns
		else:
			self.to_merge = pd.read_csv(csv)

		# set merge prefs
		self.to_merge_direction = direction
		self.to_merge_on = on
		self.drop_on_columns = drop_on_columns

	# This function "returns" a generator that's an iterator anyway. It enable the user to get the data in batches of n lines
	# without stressing the memory (or, like in my case, to avoid crashing :) )
	# 	usecols -> has to be a list, containing the no. or the names of the columns we want to load (and save memory)
	# 	parse_dates -> has to be a list, indicating whether or not to automatically parse dates identified by an attribute (or more)
	# 	date_index -> has to be a string, indicating ONE date column that has been parsed, should become index (for better manipulation) 
	def iterate(self, usecols=[], parse_dates=False, date_index=None):

		# continue to loop until any csv left in the queue
		while len(self.csv) > 0:

			# get csv to process from the queue
			csv_data = self.__get_csv()

			# assing to vars
			csv = csv_data

			# get all data from all columns
			if len(usecols) == 0:
				iterator = pd.read_csv(csv, nrows=self.nrows, chunksize=self.chunksize, sep=self.separator, iterator=True, parse_dates=parse_dates)

			# take precise columns
			else:
				iterator = pd.read_csv(csv, nrows=self.nrows, chunksize=self.chunksize, sep=self.separator, iterator=True, parse_dates=parse_dates, usecols=usecols)

			# after being processed, we remove it from the queue
			# todo: this could be improved using a pointer instead of removing from the csv list
			self.csv.pop(0)

			# create a generator
			for df in iterator:

				# if something has to be merged
				if self.to_merge is not None:
					df = pd.merge(df, self.to_merge, how=self.to_merge_direction, left_on=self.to_merge_on[0], right_on=self.to_merge_on[1])

					# remove columns that we're used to join
					if self.drop_on_columns:
						df = df.drop(columns=list(self.to_merge_on))

				# dates have to be indexed to be manipulated
				if parse_dates:

					# check date_index
					assert date_index in parse_dates and type(date_index) == str
					
					# setting datetime index
					# todo: check whether to avoid creating an index when parsing dates
					df = df.set_index(date_index)

				# yeild DataFrame and the name of the month which is related to
				yield df