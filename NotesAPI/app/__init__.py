import os
import warnings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True))
load_dotenv(find_dotenv('secrets.env', raise_error_if_not_found=True))

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
