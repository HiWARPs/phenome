import os

DEBUG=True

DATABASE='phenome.db'
SECRET_KEY = os.urandom(64)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
UPLOADS_DEFAULT_DEST = 'uploads'

RECAPTCHA_PUBLIC_KEY = '6LeebhoTAAAAAMMOTao5w3Jb73EZ1Qa_qHQ3eFZZ'
RECAPTCHA_PRIVATE_KEY = '6LeebhoTAAAAAAYpfA__vsyEowCZ_8YW_mM4I9qu'
RECAPTCHA_OPTIONS = {'theme': 'white'}