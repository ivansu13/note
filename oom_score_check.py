#!/usr/bin/env /usr/bin/python
import getopt;
import os
import sys
from os import listdir
VER = '1.00'
DIR = '/proc/'
PNAME = {'apache_proxy':-900, 'sshd':-1000, 
	'telnetd':-900, 'systemd-udevd':-1000}
SKIP_P = {'dbus-daemon':-900}

try:  
	opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "version"]);
	for opt,arg in opts:
		if opt in ("-h", "--help"):
			print sys.argv[0], 'v%s' % VER, \
				'\nHow to use:', \
				'\n\tchmod and run oom_value_tool', \
				'\n\tOr python oom_value_tool\n', \
				'\nOption:', \
				'\n\t-h | --help\tShow help info', \
				'\n\t-v | --version\tShow version'
			sys.exit()
		elif opt in("-v", "--version"):
			print sys.argv[0], 'Version :', VER
			sys.exit()
except getopt.GetoptError:
	sys.exit()

pid_dir = [ name for name in os.listdir(DIR)
		if os.path.isdir(os.path.join(DIR, name)) ]
all_proc = unmatch_proc = miss_proc = skip_proc = 0

for m in pid_dir:
	if m.isdigit() == True:
		all_proc += 1
		value_path = DIR + str(m) + '/oom_score_adj'
		comm_path = DIR + str(m) + '/comm'
		try:
			fd_value = open(value_path)
			fd_comm = open(comm_path)
			value = int(fd_value.read())
			comm = fd_comm.read().strip('\n')
			out = ('Pid:%s, Comm: %s, Value: %s' %(m, comm, value))
			if comm in SKIP_P:
				if value != SKIP_P[comm]:
					skip_proc += 1
					#print out, '(Expect: %s)' % SKIP_P[comm]
			elif comm in PNAME:
				if value != PNAME[comm]:
					unmatch_proc += 1
					print out, '(Expect: %s)' % PNAME[comm]
			else:
				if not (value == 0 or value == 200):
					unmatch_proc += 1
					print out, '(Expect: 0 | 200)'
		except:
			miss_proc += 1
			print 'open file error. pid: ', m
		finally:
			fd_value.close()
			fd_comm.close()

match_proc = all_proc - unmatch_proc - miss_proc
print '-------------------------------v%s' %VER, \
	'\n\tScanned proc:\t%d' % all_proc, \
	'\n\tMatched proc:\t%d' % match_proc, \
	'\n\tUnmatched proc:\t%d' % unmatch_proc, \
	'\n\tMissed proc:\t%d' % miss_proc, \
     	'\n\tSkiped proc:\t%d' % skip_proc
