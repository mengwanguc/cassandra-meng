import uuid
import time
import pandas as pd
import io
import numpy as np
import math
import os.path
import socket
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.policies import HostFilterPolicy
from cassandra.policies import RoundRobinPolicy
from random import randrange
# This will prevent the Cass-1 from sheding the request to Cass-2
# https://docs.datastax.com/en/developer/python-driver/3.19/api/cassandra/policies/


target_ip = "c.cass-5n-2.ucare.emulab.net"

def address_is_allowed(host_name): 
	try: 
		host_ip = socket.gethostbyname(host_name) 
		print("Hostname :  ",host_name) 
		print("IP : ",host_ip) 
		return host_ip
	except: 
		print("Unable to get Hostname and IP") 

host_ip_allowed=[address_is_allowed(target_ip)]

blacklist_filter_policy = HostFilterPolicy(
    child_policy=RoundRobinPolicy(),
    predicate=lambda host: host.address in host_ip_allowed
)

# This will go to Cass-3 ONLY!
# 	check by using cassandra/ driver and search <Cass-3's IP> message :  <ExecuteMessage
cluster = Cluster(
	[target_ip], 
    load_balancing_policy=blacklist_filter_policy
    )

session = cluster.connect()
session.execute('USE mittcpu')

#fo = open("light-client.log", "w")
#fo.close()

fo = open("light-client.log", "w")

next_ = 0
global_counter = 0
total_latency = 0

def run_query(query, id):
	global total_latency
	start_time = time.time()
	try:
		rows = session.execute(query)

		finish_time = time.time()
		latency = (finish_time - start_time)*1000
		total_latency = total_latency + latency;
		log_latency(latency)
		# print_out(rows)
	except Exception as e:
		# Should never reach here!
		logging("FAILED, received exception in the client side!")

def run_query_async(query, id, key):
	start_time = time.time()
	future = session.execute_async(query)
	future.add_callbacks(
		callback=handle_success, callback_kwargs={'start_time': start_time, 'id': id, 'key': key},
		errback=handle_error, errback_args=(id, start_time, key))

def handle_success(rows, start_time, id, key):
	global total_latency
	finish_time = time.time()
	latency = (finish_time - start_time)*1000
	total_latency = total_latency + latency;
	log_latency(latency, id, key)
	# future = session.execute(query)

def handle_error(exception, id, start_time, key):
	# logging("Should failover to Cass-2")
	logging("Failed to fetch id (%s) : %s \n %s - %s - \"latency: %f ms\"\"" % (id,exception, datetime.now(), key, latency))

def print_out(rows):
	i = 0
	print ("------------------------------------------------")
	for user_row in rows:
		i=i+1
		print (i, ". ", user_row.name," | ", user_row.phone, " | ", user_row.salary)
	print ("------------------------------------------------")

def logging(str):
	global global_counter
	global_counter = global_counter + 1
	print ("%d %s" % (global_counter, str))
	fo.write(str+"\n")

def log_latency(latency, id, key):
	if (latency>200):
		logging( "%s - %d - %s - \"latency: %f ms\"\"" % (datetime.now(), id, key, latency))
	else :
		logging( "%s - %d - %s -  latency: %f ms"  % (datetime.now(), id, key, latency))

def is_heavy_load_running():
	return True
	# because the heavy-client is not running on the same node!

user_lookup_stmt = session.prepare("select * from students where id = ?")
batch_size = 1
sleep_duration = 0.005
	# 3*4ms = 12ms
# 1
# ==========================================================================================
#rand = randrange(4059)
file_name = "tokens.txt"
df = pd.read_csv(file_name, index_col=0)
row = df.index.values

total_req = 50000
#logging(file_name)
counter = 0

print(row)
for index in range(0,total_req):
#	query = "select * from students where id = 3 or id = " + str(id + 100000000)
#	query = "select * from students where id = 5"
#	query = "SELECT id FROM mittcpu.students WHERE token(id)<=-178478985399637210 AND token(id)>-183000000000000000;" #244rows
#	query = "SELECT id FROM mittcpu.students WHERE token(id)<=-178478985399637210 AND token(id)>-182160000000000000;" #200rows
	query = "SELECT id FROM mittcpu.students WHERE token(id)<=-178478985399637210 AND token(id)>-180150000000000000;" #100rows

#	query = "select * from students where id = " + str(row[index])
#	run_query_async(query,index)
	run_query_async(query, index, "5")
	counter = counter + 1
	if (counter == batch_size):
		counter = 0
		time.sleep(sleep_duration)
	# run_query(bound,row['id'])

# 2
# ==========================================================================================
#rand = randrange(4059)
#file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
#df = pd.read_csv(file_name, index_col=0)
#total_req = total_req + df.count()
#logging(file_name)
#for index, row in df.iterrows():
#	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
#	run_query_async(bound,row['id'])
#	counter = counter + 1
#	if (counter == batch_size):
#		counter = 0
#		time.sleep(sleep_duration)
	# run_query(bound,row['id'])

# # # 3
# # # ==========================================================================================
# rand = randrange(4059)
# file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
# df = pd.read_csv(file_name, index_col=0)
# total_req = total_req + df.count()
# logging(file_name)
# for index, row in df.iterrows():
# 	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
# 	run_query_async(bound,row['id'])
# 	counter = counter + 1
# 	if (counter == batch_size):
# 		counter = 0
# 		time.sleep(sleep_duration)
# 	# run_query(bound,row['id'])

# # # 4
# # # ==========================================================================================
# rand = randrange(4059)
# file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
# df = pd.read_csv(file_name, index_col=0)
# total_req = total_req + df.count()
# logging(file_name)
# for index, row in df.iterrows():
# 	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
# 	run_query_async(bound,row['id'])
# 	counter = counter + 1
# 	if (counter == batch_size):
# 		counter = 0
# 		time.sleep(sleep_duration)
# 	# run_query(bound,row['id'])


# # # 5
# # # ==========================================================================================
# rand = randrange(4059)
# file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
# df = pd.read_csv(file_name, index_col=0)
# total_req = total_req + df.count()
# logging(file_name)
# for index, row in df.iterrows():
# 	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
# 	run_query_async(bound,row['id'])
# 	counter = counter + 1
# 	if (counter == batch_size):
# 		counter = 0
# 		time.sleep(sleep_duration)
# 	# run_query(bound,row['id'])

# # # 6
# # # ==========================================================================================
# rand = randrange(4059)
# file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
# df = pd.read_csv(file_name, index_col=0)
# total_req = total_req + df.count()
# logging(file_name)
# for index, row in df.iterrows():
# 	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
# 	run_query_async(bound,row['id'])
# 	counter = counter + 1
# 	if (counter == batch_size):
# 		counter = 0
# 		time.sleep(sleep_duration)
# 	# run_query(bound,row['id'])

# # # 7
# # # ==========================================================================================
# rand = randrange(4059)
# file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
# df = pd.read_csv(file_name, index_col=0)
# total_req = total_req + df.count()
# logging(file_name)
# for index, row in df.iterrows():
# 	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
# 	run_query(bound,row['id'])

# # # 8
# # # ==========================================================================================
# rand = randrange(4059)
# file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
# df = pd.read_csv(file_name, index_col=0)
# total_req = total_req + df.count()
# logging(file_name)
# for index, row in df.iterrows():
# 	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
# 	run_query(bound,row['id'])

# # # 9
# # # ==========================================================================================
# rand = randrange(4059)
# file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
# df = pd.read_csv(file_name, index_col=0)
# total_req = total_req + df.count()
# logging(file_name)
# for index, row in df.iterrows():
# 	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
# 	run_query(bound,row['id'])

# # # 10
# # # ==========================================================================================
# rand = randrange(4059)
# file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
# df = pd.read_csv(file_name, index_col=0)
# total_req = total_req + df.count()
# logging(file_name)
# for index, row in df.iterrows():
# 	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
# 	run_query(bound,row['id'])

# # # 11
# # # ==========================================================================================
# rand = randrange(4059)
# file_name = '~/Project/MitMem-Cassandra/workload/random_ids/ids_'+str(rand)+'.csv'
# df = pd.read_csv(file_name, index_col=0)
# total_req = total_req + df.count()
# logging(file_name)
# for index, row in df.iterrows():
# 	bound = user_lookup_stmt.bind([uuid.UUID(str(row['id']))])
# 	run_query(bound,row['id'])
max_counter=total_req
# print (max_counter)
while (True):
	i=1
	if (global_counter == int(max_counter)):
		break

avg_latency = total_latency/total_req
logging("avg : %d ms" % (avg_latency))
fo.close()
