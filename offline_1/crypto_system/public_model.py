# this is the public model class of the crypto system
# this class handles the public key generation
# parameters like p, g


# import the diffie hellman from the folder diffie_hellman
from diffie_hellman.diff_hellman import generate_prime_number, generate_generator_for_prime

# import the os.path module
import os.path


class PublicModel:
    # the p parameter(Prime Number)
    prime_number = None

    # set of prime factors of p - 1
    prime_factors = None

    # the g parameter(Primitive Root)
    primitive_root = None

    # parameter file path
    parameter_file_path = None

    # __init__
    def __init__(self):
        """
        this is the constructor of the PublicModel class
        """
        self.prime_number = 0
        self.primitive_root = 0
        self.prime_factors = set()
        self.parameter_file_path = "public/parameters.txt"

    # load_parameters

    def load_parameters(self):
        """
        this method loads the parameters from the file
        """
        # open the file
        # if the file exists, read the parameters
        # else create the file
        file = None
        if not os.path.exists(self.parameter_file_path):
            # create the file
            file = open(self.parameter_file_path, "w+")
        else:
            # open the file
            file = open(self.parameter_file_path, "r")

        # read the file
        lines = file.readlines()
        print(lines)

        # if the file is empty
        if len(lines) == 0:
            # generate the parameters
            self.generate_parameters()

            # write the parameters to the file
            file.write(str(self.prime_number) + "\n")
            file.write(str(self.primitive_root) + "\n")

            # update the lines
            lines = [str(self.prime_number), str(self.primitive_root)]

        else:
            # set the parameters
            self.prime_number = int(lines[0])
            self.primitive_root = int(lines[1])

        # close the file
        file.close()

        # set the parameters
        self.prime_number = int(lines[0])
        self.primitive_root = int(lines[1])

    # get_prime_number

    def get_prime_number(self):
        """
        this method returns the prime number
        """
        return self.prime_number

    # get_primitive_root
    def get_primitive_root(self):
        """
        this method returns the primitive root
        """
        return self.primitive_root

    # generate_parameters
    def generate_parameters(self):
        """
        this method generates the parameters
        """
        # generate the prime number
        self.generate_prime_number()

        # generate the primitive root
        self.generate_primitive_root()

    # generate_prime_number

    def generate_prime_number(self):
        """
        this method generates the prime number
        """

        p, prime_factors, loop_count = generate_prime_number(128)

        # set the prime number, prime factors
        self.prime_number = p
        self.prime_factors = prime_factors

    # generate_primitive_root

    def generate_primitive_root(self):
        """
        this method generates the primitive root
        """
        # generate the primitive root
        self.primitive_root = generate_generator_for_prime(
            self.prime_number, self.prime_factors)
