#!/usr/bin/python
import os
import sys
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib.animation as animation
import re
import operator

def mean2d(v): 
	return [float(sum(l))/len(l) for l in zip(*v)]

def read_from_file(f):
	a, b, g, d, t, c, h = [], [], [], [], [], [], []
	lines = f.readlines()
	for line in lines:	
		w = line.split()
		if w[0] == 'a': 
			a.append([float(w[1]), float(w[2]), float(w[3]), float(w[4])])
		elif w[0] == 'b': 
			b.append([float(w[1]), float(w[2]), float(w[3]), float(w[4])])
		elif w[0] == 'g': 
			g.append([float(w[1]), float(w[2]), float(w[3]), float(w[4])])
		elif w[0] == 'd': 		
			d.append([float(w[1]), float(w[2]), float(w[3]), float(w[4])])
		elif w[0] == 't': 
			t.append([float(w[1]), float(w[2]), float(w[3]), float(w[4])])
		elif w[0] == 'c': 
			c.append(float(w[1]))
		elif w[0] == 'h': 
			h.append([float(w[1]), float(w[2]), float(w[3]), float(w[4])])
		
	
	return np.asarray(a).mean(axis=1), np.asarray(b).mean(axis=1),np.asarray(g).mean(axis=1),np.asarray(d).mean(axis=1),np.asarray(t).mean(axis=1), c, h

def check_status(V): 
	#print len(V), len((V == np.asarray([1,1,1,1])) == True)
	good = 0
	for v in V:
		if v == [1.0,1.0,1.0,1.0]:
			good +=1
	return good/float(len(V))


def ewma(Y, a = 0.2): 
	S = []
	for i, y in enumerate(Y): 
		if i == 0: 
			S.append(y)
		else: 
			S.append(a*Y[i-1] + (1-a)*S[i-1])
	return S	


D = [3,5,7,9]
dirname = "../data/"
users = os.listdir(dirname)
 
for user in users:
	sessions = os.listdir(dirname + '/' + user)
	for session in sessions:
		ts = 0 
		ENG = {}
		EE = []
		points = []
		annotation = []

		file_name = dirname + '/' + user + '/' + session
		logfile = open(file_name + '/state_EEG', 'r')
		lines = logfile.readlines()
		logfile.close()
		efile = open(file_name + '/engagement','w')
		T = []
		
		if not os.path.exists('EEG/engagement/' + user + '/' + session):
   			os.makedirs('EEG/engagement/'+ user + '/' + session)
		ff = open('EEG/engagement/' + user + '/' + session + '/status', 'w')
		print "opening: " + file_name
		for line in lines: 
			A = re.split('\s+', line)
			eeg_filename = A[3]
			f = open(file_name + '/' + eeg_filename, 'r')

			a, b, g, d, t, c, h = read_from_file(f)

			status = check_status(h)
			#print status
			#if status < 0.85:
			#	print user, session, 

			ff.write(str(status) + '\n')
			
			c_smoothed = ewma(c)
			a_smoothed = ewma(a)
			b_smoothed = ewma(b)
			t_smoothed = ewma(t)

			e = [x+y for x, y in zip(a_smoothed, t_smoothed)]
			engagement = [x/y for x, y in zip(b_smoothed, e)]

			points.append(len(engagement)-1)
			efile.write(str(A[0]) + ' ' + str(A[1]) + ' ' + str(A[2]))
	
			for E in engagement: 
				efile.write(' ' + str(E))
				EE.append(E)
		
			annotation.append(A[0])
			if ENG.has_key(A[0]):
				ENG[A[0]] = np.append(ENG[A[0]], np.asarray(engagement))	
			else:
				ENG[A[0]] = np.asarray(engagement)

			efile.write('\n')

		ff.close()
		efile.close()
	
		#efile = open(file_name + '/engagement','w')
		#lines = efile.readlines()
		#efile.close()
		
		if not os.path.exists('EEG/engagement/' + user + '/' + session):
   			os.makedirs('EEG/engagement/'+ user + '/' + session)

		#efile = open('EEG/engagement/' + user + '/' + session + '/normed_mean_engagement','w')
		#for line in lines: 
		#	A = re.split('\s+', line)
		#	st1 = A[]


		plt.plot(EE)
		plt.hold(True)
		pr = 0 
	
		for pp, ann in zip(points, annotation):
			plt.axvline(int(pp + pr), color = 'r')
			plt.text(int(pr) + 1, max(EE), ann)
			pr += pp 

			
		plt.savefig('EEG/engagement/' + user + '/' + session + '/engagement.png')
		plt.hold(False)


		# plot normalized
		x = np.asarray(EE)
		minx = min(x)
		maxx = max(x)
		normed = (x-min(x))/(max(x)-min(x))
		plt.plot(normed)
		plt.ylim([-0.1, 1.1])
		plt.hold(True)

		pr = 0 
		for pp, ann in zip(points, annotation):
			plt.axvline(int(pp + pr), color = 'r')
			plt.text(int(pr) + 1, max(EE), ann)
			pr += pp
		plt.savefig('EEG/engagement/' + user + '/' + session + '/engagement_normed.png')
		plt.hold(False)	

		flatten = lambda l: [item for sublist in l for item in sublist]
		Means = [0,0,0,0]
		Vars = [0,0,0,0]
		for level in ENG: 
			a = ENG[level]
			normed_a = (a-minx)/(maxx-minx)
			weights = 100*np.ones_like(normed_a)/len(normed_a)
			plt.hist(a, weights = weights, label = 'Level = ' + str(level))
			plt.legend()
			plt.title("M = " + str(np.asarray(a).mean()) + ' var = ' + str(np.asarray(a).var()))
			plt.savefig('EEG/engagement/' + user + '/' + session + '/L_' + str(level) + '.png')
			Means[D.index(int(level))] = np.asarray(a).mean()
			Vars[D.index(int(level))] = np.asarray(a).var()

		plt.plot(Means)
		plt.savefig('EEG/engagement/' + user + '/' + session + '/means.png')
		
			

			
		
		