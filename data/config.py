from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')
IP = env.str('ip')
PASSWORD = env.str('PASSWORD')
SUPPORTS = env.list('SUPPORTS')

database_path = env.str('database_path')

NGROK_AUTHTOKEN = env.str('NGROK_AUTHTOKEN')
