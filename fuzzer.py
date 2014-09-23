#!/usr/bin/python

#Fuzzer for testing texmaker
#http://www.xm1math.net/texmaker/

import math
import random
import string
import subprocess
import time



#List of files to use as initial seed
file_list=[]

for i in range(1,11):
	file_name = "./tests/test"+ str(i) + ".tex"
	file_list.append(file_name)
	


#Application to test
app = "/Applications/texmaker.app/Contents/MacOS/texmaker"


fuzz_output = "fuzzed_input.tex"

fuzz_factor = 50
num_tests = 200
verbose = False



for i in range(num_tests):
	file_choice = random.choice(file_list)
	
	buf= bytearray(open(file_choice, 'rb').read()) #read in binary
	
	#5-line fuzzer from Charlie MIller's "Babysitting an Army of Monkeys"
	#---------------------------------------------------------
	num_writes = random.randrange(math.ceil((float(len(buf)) / fuzz_factor ))) +1
		
	for j in range(num_writes):
		rbyte = random.randrange(256)
		rn = random.randrange(len(buf))
		buf[rn] = "%c"%(rbyte)
		
	#----------------------------------------------------------
	
	#save mutated input
	open(fuzz_output, 'wb').write(buf)
	
	#open application with mutated input
	process = subprocess.Popen([app,fuzz_output])
	
	#see what happens
	time.sleep(1)
	crashed=process.poll()
	
	#process.terminate()
	if crashed:
		#renaming input file
		crashing_file = "crash_"+file_choice
		subprocess.call(['rename',file_choice,crashing_file], shell=True)
		print "process crashed with input file " + crashing_file
		exit(1)
	if not crashed:
		if verbose:
			print "Test", i, "file "+ file_choice + " OK"
		process.terminate()
		
		
print "All tests OK"		
