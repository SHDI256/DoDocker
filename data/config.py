from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')
IP = env.str('ip')
PASSWORD = env.str('PASSWORD')

database = env.str("database")

if database == "postgresql":
    postgresql = {'pguser': env.str("pguser"),
              'pgpasswd': env.str("pgpasswd"),
              'pghost': env.str("pghost"),
              'pgport': env.int("pgport"),
              'pgdb': env.str("pgdb")
              }

elif database == "sqlite":
    database_path = env.str("bdname")