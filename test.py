""" Test file for sort.py
"""
from hashlib import md5

from passwordsorter import sort


def md5Hash(unicodeStr: str):
	return md5(unicodeStr.encode("utf-8")).hexdigest()


TABLE0 = [
	["password123", "john@example.com", md5Hash("password123")],
	["password", "steve@example.com", md5Hash("password")],
	["pa55w0rd!", "bill@example.com", md5Hash("pa55w0rd")],
	["password123", "sam@example.com", md5Hash("password123")],
	["password123", "gwen@example.com", md5Hash("password123")],
	["password123", "samantha@example.com", md5Hash("password123")],
	["password123", "john@example.com", md5Hash("password123")],
	["password123", "john@example.com", md5Hash("password123")],
	["password123", "john@example.com", md5Hash("password123")],
	["password123", "john@example.com", md5Hash("password123")],
	["password123", "john@example.com", md5Hash("password123")],
	["password123", "john@example.com", md5Hash("password123")],

]


DOMAINS = [" example.com"]



FILE0 = open("TestFiles/Braydooon.txt pastebin.comSvZR2M9L.txt").readlines()


FILE0_TABLE = [
	["thesaxmaniac@hotmail.com", "neverhood"],
	["ledzepln1@aol.com", "stairway"],
	["mekim45@hotmail.com", "mullins74"],
	["jjenkins19@yahoo.com", "faster"],
	["r_m_vincent@yahoo.com", "soling12"],
	["deadally@hotmail.com", "balajaga1"],
	["Choas23@gmail.com", "8KlAs432"],
	["jefftrey@yahoo.com", "tanqueray"],
	["syntex05@mac.com", "kobela87"],
	["michaelbarbra@hotmail.com", "2177"],
	["mcginnis_98@yahoo.com", "bentley"],
	["majikcityqban82@gmail.com", "tinpen39"],
	["pekanays@yahoo.com", "warriors"],
	["g_vanmeter@yahoo.com", "torbeet"],
	["rrothn@yahoo.com", "rebsopjul3"],
	["apryle_douglas@yahoo.com", "campbell"],
	["estocanam2@gmail.com", "Firebird1@"],
	["Samirenzer@yahoo.com", "pepper0120"],
	["davebialik@gmail.com", "tr1ang1e"],
	["kellyjames@atmc.net", "ginnyanna"],
	["Kennedy123@aol.com", "Edmonia1"],
	["rcstanley@ms.metrocast.net", "jjba1304"]
]

def test_idEmailCol():
	assert sort.idEmailCol(TABLE0) == 1


def test_idHashCol():
	assert sort.idHashCol(TABLE0) == 2


def test_idPwdCol():
	assert sort.idPwdCol(TABLE0) == 0


def test_getSrc():
	assert sort.getSrc(DOMAINS[0]) == "example.com"



def test_File0_Delim():
	assert sort.returnDelim(FILE0) == ":"


def test_File0_Data():
	assert sort.returnArr(FILE0) == FILE0_TABLE

def test_File0_idEmailCol():
	assert sort.idEmailCol(FILE0_TABLE) == 0


def test_File0_idHashCol():
	assert sort.idHashCol(FILE0_TABLE) == -1


def test_File0_idPwdCol():
	# Wow using our algorithm, we can only be 15% sure that this is a password
	# col. Col0 has a score of 0.6 and Col1 has a score of 4.3
	assert sort.idPwdCol(FILE0_TABLE, 0.15) == 1


def test_File0_getSrc():
	assert sort.getSrc("Braydooon.txt pastebin.comSvZR2M9L.txt") == "pastebin.com"
