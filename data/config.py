from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = list(map(int, env.list("ADMINS")))
DB_PATH = 'sqlite+aiosqlite:///' + env.str('DB_NAME')

# TODO это вынести в доп таблу
RULES_URL = env.str('RULES_URL')
