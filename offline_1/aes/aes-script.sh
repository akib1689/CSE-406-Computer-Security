# take the input from plaintext.txt 
# and encrypt it using aes-128



echo -e "plain Text(in Hex)\tplain Text(in ASCII)\tkey(in Hex)\tkey(in ASCII)\tCipher Text(in Hex)\tCipher Text(in ASCII)\tDeciphered Text(in Hex)\tDeciphered Text(in ASCII)\tKey Expansion Time\tEncryption Time\tDecryption Time" > aes-128.txt

# for each 2 lines in plaintext.txt
for i in $(seq 1 2 $(wc -l < plaintext.txt))
do
    # take the first line
    line1=$(sed -n ${i}p plaintext.txt)
    # take the next line
    line2=$(sed -n $((${i}+1))p plaintext.txt)
    
    # create a temp file
    echo -e "$line1\n$line2" > temp.txt

    # run the aes-demo program with the temp file as input
    python3 aes-demo.py < temp.txt >> aes-128.txt

    echo -e "\n-----------------------------------\n" >> aes-128.txt

    # remove the temp file
    rm temp.txt
done