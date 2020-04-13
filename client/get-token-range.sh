#!/bin/bash 
echo "PAGING OFF; SELECT tokens FROM system.local;" > query.cql

# Generate token-range.txt to be run on python at Local
echo "# Run with python (after fix the array initialization below) arr = ['a','b','c'] " > token-range.txt

echo "from pandas import *" >> token-range.txt
echo "import pandas as pd" >> token-range.txt

ip=$(dig +short `dig +short a.cass-5n.ucare.emulab.net | awk '{ print ; exit }' ` | awk '{ print; exit }' )
echo "# cass-1: $ip" >> token-range.txt
echo "arr1 = " >> token-range.txt
cqlsh $ip  -f query.cql | grep "{"  >> token-range.txt

ip=$(dig +short `dig +short b.cass-5n-2.ucare.emulab.net | awk '{ print ; exit }' ` | awk '{ print; exit }' )
echo "# cass-2: $ip" >> token-range.txt
echo "arr2 = " >> token-range.txt
cqlsh $ip  -f query.cql | grep "{"  >> token-range.txt

ip=$(dig +short `dig +short c.cass-5n-2.ucare.emulab.net | awk '{ print ; exit }' ` | awk '{ print; exit }' )
echo "# cass-3: $ip" >> token-range.txt
echo "arr3 = " >> token-range.txt
cqlsh $ip  -f query.cql | grep "{"  >> token-range.txt

echo "df1 = DataFrame({'key': arr1, 'node': 'cass-1'})" >> token-range.txt
echo "df2 = DataFrame({'key': arr2, 'node': 'cass-2'})" >> token-range.txt
echo "df3 = DataFrame({'key': arr3, 'node': 'CASS-3---'})" >> token-range.txt

echo "df = pd.concat([df1, df2], axis=0)" >> token-range.txt
echo "df = pd.concat([df, df3], axis=0)" >> token-range.txt
echo "df=df.sort_values('key', ascending=True)" >> token-range.txt
echo "df.to_csv('all-range.csv', sep='\t')" >> token-range.txt
echo "exit()" >> token-range.txt

echo "# then open: subl ~/Documents/Github/MitMem-Cassandra/important_result/current/all-range.csv" >> token-range.txt

