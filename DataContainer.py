import gzip
import pickle

# Simple container with load and save methods.  Declare the container
# then add data to it.  Save will save any data added to the container.
# The class automatically gzips the file if it ends in .gz
#
# Notes on size and speed (using UbuntuDialog data)
#       pkl     pkl.gz
# Save  11.4s   83.7s
# Load   4.8s   45.0s
# Size  596M    205M
#
class DataContainer(object):
    @staticmethod
    def isGZIP(filename):
        if filename.split('.')[-1] == 'gz':
            return True
        return False

    # Using HIGHEST_PROTOCOL is almost 2X faster and creates a file that
    # is ~10% smaller.  Load times go down by a factor of about 3X.
    def save(self, filename='DataContainer.pkl'):
        if self.isGZIP(filename):
            f = gzip.open(filename, 'wb')
        else:
            f = open(filename, 'wb')
        pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    # Note that loading to a string with pickle.loads is about 10% faster
    # but probaly comsumes a lot more memory so we'll skip that for now.
    @classmethod
    def load(cls, filename='DataContainer.pkl'):
        if cls.isGZIP(filename):
            f = gzip.open(filename, 'rb')
        else:
            f = open(filename, 'rb')
        n = pickle.load(f)
        f.close()
        return n