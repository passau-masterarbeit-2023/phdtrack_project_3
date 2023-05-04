import os
from dotenv import load_dotenv



if __name__ == '__main__':
    # Load environment variables from .env file
    env_path = os.path.join(os.path.dirname(__file__), 'src', '.env')
    load_dotenv(dotenv_path=env_path)

    # Access environment variables
    variable_name = os.getenv('VARIABLE_NAME')
