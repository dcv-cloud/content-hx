servers="198.18.134.200 198.18.134.201 198.18.134.202 198.18.134.203 198.18.134.204 192.168.0.100 192.168.0.51 192.168.0.52 192.168.0.53 192.168.0.54"



while :
do
echo $(date) >> /tmp/output.txt
for i in `echo $servers`
do
ping -c 1 $i > dev/null && echo "$i is up" >> /tmp/output.txt || echo "$i is down" >> /tmp/output.txt
done
sleep 60
done


