# create a set of 128, 192, 256 

# for each time in 128, 192, 256
# run the diff-hellman-demo program with the time as input
# take the output and append it to diff-hellman.csv

# file creation
echo "p,g,a,b,A,B,S1,S2" > diff-hellman.csv


# for each time in 128, 192, 256
for i in 128 192 256
do
    # run the diff-hellman-demo program with the time as input
    # 5 times for each time
    for j in 1 2 3 4 5
    do
        echo $i > temp.txt
        python3 diff-hellman-demo.py < temp.txt >> diff-hellman.csv
    done

    # add a new line
    echo "---,---,---,---,---,---,---,---" >> diff-hellman.csv

done