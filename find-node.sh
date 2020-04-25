for i in {1..1000}
do
  echo $i
  nodetool getendpoints mittcpu students $i
done
