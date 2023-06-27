# this file will convert any file type to the
# binary and convert the original file from the binary


# from file to binary data
def file_to_binary(file_path):
    # open the file in read mode
    with open(file_path, 'rb') as f:
        # read the file
        data = f.read()

    # convert the data to binary
    data = int(data.hex(), 16)

    # return the data
    return data


# from binary to file
def binary_to_file(data, file_path):
    # convert the data to hex
    data = hex(data)[2:]

    # convert the data to bytes
    data = bytes.fromhex(data)

    # open the file in write mode
    with open(file_path, 'wb') as f:
        # write the data
        f.write(data)


# test the file_to_binary and binary_to_file
# file_path = 'test.jpg'
# data = file_to_binary(file_path)

# # print the data
# print(data)
# binary_to_file(data, 'test2.jpg')


# * conclusion: it works
