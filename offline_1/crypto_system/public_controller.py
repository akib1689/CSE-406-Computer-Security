# this class controls the public key generation
# model class is the PublicModel class

# import the public model
from public_model import PublicModel


class PublicController:

    # the public model
    public_model = None

    def __init__(self):
        # initialize the public model
        self.public_model = PublicModel()
        self.public_model.load_parameters()

    def get_prime_number(self):
        """
        this method returns the prime number
        """
        prime_number = self.public_model.get_prime_number()
        return prime_number

    def get_primitive_root(self):
        """
        this method returns the primitive root
        """
        primitive_root = self.public_model.get_primitive_root()
        return primitive_root

    def get_parameters(self):
        """
        this method returns the parameters in json format
        """
        # get the prime number
        prime_number = self.get_prime_number()

        # get the primitive root
        primitive_root = self.get_primitive_root()

        # return the parameters
        return {
            "p": prime_number,
            "g": primitive_root,
            "min_len": 128 // 2
        }
