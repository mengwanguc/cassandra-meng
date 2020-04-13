echo "PAGING OFF; SELECT id FROM mittcpu.students WHERE token(id)>-1726525886406345424 AND token(id)<=-1584256327744874821 ;" > query.cql


cqlsh c.cass-5n-2.ucare.emulab.net  -f query.cql > tokens.txt
