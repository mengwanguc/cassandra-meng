#!/bin/bash
start_time="$(date -u +%s)"

echo " Resetting Keyspace"
python3 reset-keyspace.py 
echo " Temporary test data are deleted"


echo " heavy workload is started"

touch heavy_load.running
node_name=`hostname`

# Put Cass-2 in the whitelist (Limit communications to the provided nodes)
cass_1=`dig +short a.cass-5n.ucare.emulab.net | sed -n 2p`
cass_2=`dig +short b.cass-5n.ucare.emulab.net | sed -n 2p`
cass_3=`dig +short c.cass-5n.ucare.emulab.net | sed -n 2p`

host_target='a.cass-5n.ucare.emulab.net'

# Run the noise for Cass-1
tools/bin/cassandra-stress user profile=tools/cqlstress-cluster.yaml n=15000000 ops\(insert=4,simple1=2\) cl=ONE no-warmup -errors ignore -rate threads=4 -node $cass_1 whitelist  -graph file=test.html title=test 

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "elapsed $elapsed"
