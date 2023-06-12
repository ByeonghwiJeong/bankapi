import os
from dotenv import load_dotenv

load_dotenv()

"""
.env file

db_protocol=mysql+aiomysql
db_user=root
db_password=6008
db_host=127.0.01
db_port=3306
db_name=bering
SECRET_KEY=333809dfe79d55fc49216952965632e7cc0b46b1d27ce34792581014a6cef1b1
ALGORITHM=HS256
"""

def get_db_uri():
    return "{}://{}:{}@{}:{}/{}".format(
        os.getenv("db_protocol", ""),
        os.getenv("db_user", ""),
        os.getenv("db_password", ""),
        os.getenv("db_host", ""),
        os.getenv("db_port", ""),
        os.getenv("db_name", ""),
    )
