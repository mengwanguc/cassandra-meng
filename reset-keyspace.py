import uuid
import time
import io
	
from cassandra.cluster import Cluster

cluster = Cluster(["a.cass-5n.ucare.emulab.net"])
session = cluster.connect()

def run_query(query):
	rows = session.execute(query)
	# print_out(rows)

def run_query_async(query):
	# future = session.execute(query)
	future = session.execute_async(query)
	future.add_callbacks(handle_success, handle_error)

def handle_success(rows):
	global next_
	try:
		next_ = 1
		# print_out(rows)
	except Exception:
		print("Failed to process the query ")
		# don't re-raise errors in the callback

def handle_error(exception):
	global next_
	next_ = 1
	print("Failed to fetch user info: ", exception)

def print_out(rows):
	print ("------------------------------------------------")
	print (rows)
	print ("------------------------------------------------")


run_query_async('DROP KEYSPACE stresscql')
run_query_async('DROP KEYSPACE keyspace1')
print ("--- Dropping keyspace1 and stresscql")
for x in range(1,1000):
	# wait until the keyspace1 is dropped (the number of keyspaces should be 6)
	if (len(cluster.metadata.keyspaces) > 6):
		print('.', end='', flush = True)
		time.sleep(1)
print ("\n--- keyspaces are dropped")

