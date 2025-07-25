import os
from dotenv import load_dotenv

def pytest_configure():
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env.test"))