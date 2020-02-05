First build:
	build-cassandra.sh
	or
	build-cassandra-myjdk.sh #using my own jdk


Rebuild:
	recompile-cassandra.sh
	or
	recompile-cassandra-myjdk.sh #using my own jdk


We should add our new jdk bin folder to the system PATH.
Otherwise it will use the jdk in /usr/lib/jvm/java-8-openjdk-amd64/bin/.
