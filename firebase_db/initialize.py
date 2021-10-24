from firebase_admin import credentials,initialize_app

# Use a service account
cred = credentials.Certificate('ServiceAccountKey.json')


def initialize_firebase():
    return initialize_app(cred)