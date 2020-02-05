export SOURCE_ROOT=/home/sda_mount

export LANG="en_US.UTF-8"
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF8"
export JAVA_HOME="/home/sda_mount/MitMem-OpenJDK8/java8-mitmem"
export ANT_OPTS="-Xms4G -Xmx4G"
export ANT_HOME=$SOURCE_ROOT/apache-ant-1.10.4
export PATH=$JAVA_HOME/bin:$ANT_HOME/bin:$PATH


cd $SOURCE_ROOT/
cd cassandra-meng
sed  -i 's/Xss256k/Xss32m/g' build.xml conf/jvm.options
cd $SOURCE_ROOT/cassandra-meng
ant

cd $SOURCE_ROOT/cassandra-meng
sed -i "s/\<http\>/https/g" build.properties.default
sed -i "89s/\<http:\/\/repo2\>/https:\/\/repo1/" build.xml


cd $SOURCE_ROOT/
cd jna
ant
rm $SOURCE_ROOT/cassandra-meng/lib/jna-4.2.2.jar
cp build/jna.jar $SOURCE_ROOT/cassandra-meng/lib/jna-4.2.2.jar

export PATH=/home/sda_mount/cassandra-meng/bin:$PATH
echo $PATH
