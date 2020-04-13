import pandas as pd
import numpy as np
import time
import sys
from cassandra.cluster import Cluster

cluster = Cluster(['c.cass-5n-2.ucare.emulab.net'])

session = cluster.connect('mittcpu')


#print(session.execute("SELECT release_version FROM system.local").one())

file_name = "tokens.txt"
df = pd.read_csv(file_name, index_col=0)
row = df.index.values

times = []
for i in range(0,1000):
	start = time.time()
#	command = "select * from students where id = " + str(row[i]);
	command = "select * from students where id = 5";
	rows = session.execute(command)
	end = time.time()
	if i >= 100:
		times.append(end-start)
	print(end-start)



with open(sys.argv[1], 'w') as the_file:
	for t in times:
		the_file.write(str(t) + '\n')


