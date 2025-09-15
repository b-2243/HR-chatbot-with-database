import os
import django
import pyodbc
from chatbotmodule.logger_function import logger_function

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrchatbot.settings')  # replace with your actual settings module path
django.setup()

from django.conf import settings

filename = os.path.basename(__file__)[:-3]

def getConnection():
    try:
        db_settings = settings.DATABASES['default']
        driver = db_settings['OPTIONS']['driver']
        server = db_settings['HOST']
        database = db_settings['NAME']
        trusted = 'yes' if db_settings['USER'] == '' else 'no'  # adjust this based on your auth style

        connection_string = (
            f"Driver={{{driver}}};"
            f"Server={server};"
            f"Database={database};"
        )

        if db_settings['USER']:
            connection_string += (
                f"UID={db_settings['USER']};"
                f"PWD={db_settings['PASSWORD']};"
            )
        else:
            connection_string += "Trusted_Connection=yes;"

        # Add any extra params like TrustServerCertificate
        if 'extra_params' in db_settings['OPTIONS']:
            connection_string += db_settings['OPTIONS']['extra_params'] + ';'

        connection = pyodbc.connect(connection_string)
        return connection

    except Exception as e:
        logger_function(filename, e, 2)
