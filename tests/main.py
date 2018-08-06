from unittest import TextTestRunner
from test_auth import suite

if __name__ == "__main__":
    suite = suite()
    ttr = TextTestRunner()
    ttr.run(suite)
