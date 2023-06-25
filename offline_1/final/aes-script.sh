# take the input from plaintext.txt 
# and encrypt it using aes-128



echo -e "plain Text(in Hex)\tplain Text(in ASCII)\tkey(in Hex)\tkey(in ASCII)\tCipher Text(in Hex)\tCipher Text(in ASCII)\tDeciphered Text(in Hex)\tDeciphered Text(in ASCII)\tKey Expansion Time\tEncryption Time\tDecryption Time" > aes-128.txt

# each line in plaintext.txt and keys.txt 
# run the aes-demo.py and store the output in aes-128.txt
while read line1 && read line2 <&3; do

    # store line1 and line2 in temp.txt
    echo -e "$line1\n$line2" > temp.txt
    python3 aes-demo.py >> aes-128.txt < temp.txt
    # remove temp.txt
    rm temp.txt

    echo "--------------------------------------------------">> aes-128.txt
done < plaintext.txt 3< keys.txt