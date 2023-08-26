import os
import warnings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

##
DEBUG = os.getenv('DEBUG')
if DEBUG is None:
    warnings.warn("DEBUG is not provided; using DEBUG=True")
    DEBUG = 1
else:
    try:
        DEBUG = int(DEBUG)
        assert DEBUG in {0, 1}
    except:
        raise EnvironmentError("DEBUG: Unknown value provided; 0 or 1 expected")
