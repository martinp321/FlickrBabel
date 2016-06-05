from microsofttranslator import Translator

"""
Examples of what config settings look like:
FLICKR_CONFIG = {'photoset_id': '7245765746496198',
                 'user_id': '632007@N07',
                 'api_key': '7988vc595a6d5ce9d6b7751bf1af',
                 'api_secret': 'a733b5250863'}

MS_CLIENT_ID = 'someClientId'
MS_SECRET_KEY = 'AL16vZYCQ8ZUGHvUmaDnyx3gPbDsvd3F4hC27Y='
"""

FLICKR_CONFIG = {'photoset_id': 'FILL ME IN',
                 'user_id': 'FILL ME IN',
                 'api_key': 'FILL ME IN',
                 'api_secret': 'FILL ME IN'}

MS_CLIENT_ID = 'FILL ME IN'
MS_SECRET_KEY = 'FILL ME IN'

SUPPORTED_LANGUAGES = ['de', 'es', 'fr', 'it', 'ko', 'pt', 'zh-CHT', 'zh-CHS', 'ja']

def translate(tag, language):
    """ returns lower-case tag translated into language """
    translator = Translator(MS_CLIENT_ID, MS_SECRET_KEY)
    return translator.translate(tag, language).lower()

