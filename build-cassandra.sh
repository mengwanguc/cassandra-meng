export SOURCE_ROOT=/home/sda_mount

sudo apt-get update
sudo apt-get install -y git tar g++ make automake autoconf libtool  wget patch libx11-dev libxt-dev pkg-config texinfo locales-all unzip python
sudo apt-get install -y openjdk-8-jre openjdk-8-jdk

cd $SOURCE_ROOT/
wget http://archive.apache.org/dist/ant/binaries/apache-ant-1.10.4-bin.tar.gz
tar -xvf apache-ant-1.10.4-bin.tar.gz

export LANG="en_US.UTF-8"
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF8"
export JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk-amd64/"
export ANT_OPTS="-Xms4G -Xmx4G"
export ANT_HOME=$SOURCE_ROOT/apache-ant-1.10.4
export PATH=$JAVA_HOME/bin:$ANT_HOME/bin:$PATH


cd $SOURCE_ROOT/
cd cassandra-meng
sed  -i 's/Xss256k/Xss32m/g' build.xml conf/jvm.options
cd $SOURCE_ROOT/cassandra
ant

