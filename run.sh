set +o posix
rm result.csv
make
echo "MEM,func,k,AAE,ARE,_sum,throughput" >> result.csv
#ruleDir='/Users/caolu/Downloads/Data/temp.dat'
chmod +r /Users/caolu/Downloads/Data/*.dat
ruleDir[40]="/Users/caolu/Downloads/Data/temp.dat"
if [ -z "${ruleDir[0]}" ]; then
    ruleDir="${ruleDir[40]}"
fi
echo "ruleDir: $ruleDir"
for ((int i = 1; i <= 1000000; i++))
do
		read -r -n 13 tmp
        tmp="${tmp%'\n'}"
        s[$i]="$tmp"
        ((B[$tmp]++))
done
#for MEM in 10 20 30 40 50 60 70 80 90 100
for MEM in 10 20 30 40 50 60 70 80 90 $(seq 100 100 1000)
do
    for K in $(seq 100 100 1000)
    do
      cmd="./cuckoo -d $ruleDir -m $MEM -k $K"
      #cmd="./cuckoo -d $ruleDir -m $MEM -k 1000" 
        echo $cmd
        eval $cmd
        pid = $!
        wait $pid
        if ps -p $pid > /dev/null; then
            kill -9 $pid
        fi
        echo "done"
        sleep 1
    done
done

