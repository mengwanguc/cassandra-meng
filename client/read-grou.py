import time
import sys
from cassandra.cluster import Cluster

cluster = Cluster(['155.98.36.70'])

session = cluster.connect('mittcpu')


print(session.execute("SELECT release_version FROM system.local").one())

times = []
for i in range(0,1000):
	start = time.time()
	command = "select * from students where id <= 10 group by id ALLOW FILTERING";
	rows = session.execute(command)
	end = time.time()
	if i >= 100:
		times.append(end-start)


with open(sys.argv[1], 'w') as the_file:
	for t in times:
		the_file.write(str(t) + '\n')


