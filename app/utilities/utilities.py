import os
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

def Verify_credentials(TOKEN):
    return TOKEN==ACCESS_TOKEN
