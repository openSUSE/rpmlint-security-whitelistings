#!/usr/bin/python3

import os, sys
import subprocess
import glob

def checkJSONFile(path):

	with open(path, 'rb') as json_fd:
		try:

			print("Checking", path, "... ", end = '')
			sys.stdout.flush()

			res = subprocess.call(
				["json_verify"],
				close_fds = True,
				shell = False,
				stdin = json_fd
			)

			if res == 0:
				return True
			else:
				print(path, "is not valid JSON!")
				return False

		except FileNotFoundError:

			print("Couldn't find json_verify. You need to install yajl (yet-another-json-lib).", file = sys.stderr)
			sys.exit(2)

our_dir = os.path.dirname(os.path.realpath(__file__))
pathspec = os.path.join( our_dir, "*.json" )
res = 0

for json_file in glob.glob(pathspec):

	if not checkJSONFile(json_file):
		res = 1

sys.exit(res)
