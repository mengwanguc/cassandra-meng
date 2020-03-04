from cassandra.cluster import Cluster

cluster = Cluster(['c.cass-5n.ucare.emulab.net'])

session = cluster.connect('mittcpu')


print(session.execute("SELECT release_version FROM system.local").one())


for i in range(2,1000000):
	command = 'INSERT INTO students (id, name, city,salary, phone) VALUES('
	command += str(i)
	command += ',\''
	command += str(i)
	command += '\',\''
	command += str(i)
	command += '\','
	command += str(i)
	command += ','
	command += str(i)
	command += ');'
	session.execute(command)
	if i % 1000 == 0:
		print(i)
