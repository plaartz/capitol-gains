import os

if os.getenv('CI') == 'true':
    from .settings_test import *
else:
    from .settings import *
