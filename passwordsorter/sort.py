"""PASSWORD SORTER

Sort dumps into Email, hash, password, source
"""
from __future__ import annotations

import typing
import csv
from re import match, search as regexSearch
import time
from pathlib import Path

from email_validator import validate_email, EmailNotValidError
from hashid import HashID

THISDIR = str(Path(__file__).resolve().parent)

# We want to limit the file chunks to 1gb
BUF_SIZE = 10**9

TLDS = "|".join([line.strip()
for line in open(THISDIR + "/tlds.txt").readlines()]).lower()


# Find the delimeter and split, if delim is a space then shlex.split
def returnDelim(lines: list[str]):
	"""Return the most likely delimeter from some input data

	Args:
		lines (list[str]): array of plaintext lines (raw data)
	"""
	delims = [" ", "\t", ",", ":", ";"]
	maxCount = 0
	delimIdx = -1
	for index, delim in enumerate(delims):
		delimCount = "".join(lines).count(delim)
		if delimCount > maxCount:
			maxCount = delimCount
			delimIdx = index
	return delims[delimIdx]


def returnArr(lines: list[str], delim: typing.Optional[str] = None) -> list[
list[str]]:
	"""Convert the array of raw data (lines) to a 2d array representing a table

	Args:
		lines (string[]): array of plaintext lines (raw data)
	"""
	delim = returnDelim(lines) if delim is None else delim
	if delim != " ":
		return list(csv.reader(lines, delimiter=delim))
	return [line.split() for line in lines]


# Identify the email column from a table of data
def idEmailCol(data: list[list[str]], threshhold: float = 0.85) -> int:
	"""Do some heuristics on the data and return the column index that is
	likely to be the email column

	Args:
		data (list[list[str]]): the 2d array of data to analyse
		threshhold (float, optional): The confidence that the column actually
		contains email addresses. Defaults to 0.85.

	Returns:
		int: the column index for emails
	"""
	rowThreshold = int(len(data) * threshhold)
	emailIdx = -1
	maxScore = 0
	for colIdx in range(len(data[0])):
		score = 0
		for row in data:
			try:
				validate_email(row[colIdx], check_deliverability=False)
				score += 1
			except EmailNotValidError:
				pass
		if score > maxScore and score > rowThreshold:
			maxScore = score
			emailIdx = colIdx
	return emailIdx


# Identify the hash column from a table of data
def idHashCol(data: list[list[str]], threshhold: float = 0.85) -> int:
	"""Do some heuristics on the data and return the column index that is
	likely to be the hash column

	Args:
		data (list[list[str]]): the 2d array of data to analyse
		threshhold (float, optional): The confidence that the column actually
		contains hashes. Defaults to 0.85.

	Returns:
		int: the column index for the hashes
	"""
	rowThreshold = int(len(data) * threshhold)
	hashIdx = -1
	maxScore = 0
	for colIdx in range(len(data[0])):
		score = 0
		for row in data:
			if len(list(HashID().identifyHash(row[colIdx]))) > 0:
				score += 1
		if score > maxScore and score > rowThreshold:
			maxScore = score
			hashIdx = colIdx
	return hashIdx


def isKnownPwd(password: str) -> bool:
	"""Is the password known? As in does it show up in the top 10,000 list?

	Args:
		password (str): password to check

	Returns:
		bool: true if known
	"""
	with open(THISDIR + '/top10000.txt') as pwdFile:
		return password in pwdFile.read()


def hasPwdComplexity(password: str) -> bool:
	"""Does the password have sufficient complexity?

	Args:
		password (string): password to check

	Returns:
		bool: true if the string looks like a complex password
	"""
	minPwdLen = 8
	regexValidPwd = (
	## Don't allow any spaces, e.g. '\t', '\n' or whitespace etc.
	r'^(?!.*[\s])'
	## Check for a digit
	r'((?=.*[\d])'
	## Check for an uppercase letter
	r'(?=.*[A-Z])'
	## check for special characters. Something which is not word, digit or
	## space will be treated as special character
	r'(?=.*[^\w\d\s])).'
	## Minimum 8 characters
	'{' + str(minPwdLen) + ',}$')
	return match(regexValidPwd, password) is not None


# Identify the password column from a table of data
def idPwdCol(data: list[list[str]], threshhold: float = 0.7) -> int:
	"""Do some heuristics on the data and return the column index that is
	likely to be the password column

	Args:
		data (list[list[str]]): the 2d array of data to analyse
		threshhold (float, optional): The confidence that the column actually
		contains passwords. Defaults to 0.7.

	Returns:
		int: the column index for the passwords
	"""
	rowThreshold = int(len(data) * threshhold * 1.3)
	hashIdx = -1
	maxScore = 0
	for colIdx in range(len(data[0])):
		score = 0
		for row in data:
			if isKnownPwd(row[colIdx]):
				score += 1
			if hasPwdComplexity(row[colIdx]):
				score += 0.3 # This has a smaller bearing than a definite pwd as
				# some email addresses would meet this
		if score > maxScore and score > rowThreshold:
			maxScore = score
			hashIdx = colIdx
	return hashIdx


# Grab the suspected source from the filename
def getSrc(filename: str) -> typing.Optional[str]:
	"""Grab the source/ domain from the filename

	Args:
		filename (str): the relative file path/ filename

	Returns:
		string|None: return the domain name or None
	"""
	groups = regexSearch(r"[ :;](.*?\.(" + TLDS + r"))", filename)
	if groups is not None:
		return groups.group(0).strip()
	groups = regexSearch(r"[/\\](.*?\.(" + TLDS + r"))", filename)
	if groups is not None:
		return groups.group(0).strip()
	groups = regexSearch(r"(.*?\.(" + TLDS + r"))", filename)
	return groups.group(0) if groups is not None else None


# Process a file...
def process(lines: list[str], filename: str):
	"""Process a file

	Args:
		lines (list[str]): list of lines from the file
		filename (str): path to the file
	"""
	# We want to take a sample of lines to identify each column and otherwise
	# parse the raw data
	head = lines[:70] if len(lines) > 70 else lines
	head = head[20:] if len(head) > 60 else head
	# Using this sample, lets work out what's what (c)
	delim = returnDelim(head)
	head2d = returnArr(head, delim)
	# Which col is emails??
	emlCol = idEmailCol(head2d)
	# Which col is the hash??
	hashCol = idHashCol(head2d)
	# Which col is the password??
	pwdCol = idPwdCol(head2d)
	# Lets try and work out the domain from the filename
	domain = getSrc(filename)

	if -1 in [emlCol, hashCol, pwdCol]:
		print("Unfortunately, it wasn't possible to determine all of the elements" +
		"\nTake a look at some of the data below and answer the following questions. Enter '-1' if NA"
							)
		for row in head2d:
			print("\t".join(row))
	if emlCol < 0:
		emlCol = int(input("Enter the column for emails (zero indexed) \n>"))
	if hashCol < 0:
		hashCol = int(input("Enter the column for hashes (zero indexed) \n>"))
	if pwdCol < 0:
		pwdCol = int(input("Enter the column for passwords (zero indexed) \n>"))
	if domain is None:
		domain = input("Enter the domain \n>")

	# Lets write to some output
	data = returnArr(lines, delim)
	with open(f"output{time.time()}.csv", "w", newline="") as csvfile:
		writer = csv.writer(csvfile)
		for row in data:
			writer.writerow([row[emlCol] if emlCol >= 0 else "",
			row[hashCol] if hashCol >= 0 else "",
			row[pwdCol] if pwdCol >= 0 else "",
			domain]) # yapf: disable


# Open Massive files
def processFile(filename: str):
	"""Open a massive file and call process() for each 1gb chunk

	Args:
		filename (str): relative file path of dump
	"""
	bigfile = open(filename, 'r')
	bufLines = bigfile.readlines(BUF_SIZE)
	while bufLines:
		process(bufLines, filename)
		bufLines = bigfile.readlines(BUF_SIZE)
