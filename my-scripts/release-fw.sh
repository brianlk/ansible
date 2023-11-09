
ports="1500 1501 1505 1506 6325 6326"

for p in $ports
do
	firewall-cmd --add-port=$p/tcp --permanent
	firewall-cmd --add-port=$p/udp --permanent
done
firewall-cmd --reload
