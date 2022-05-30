from environs import Env

env = Env()
env.read_env()

S_KEY = env.str('SECRET_KEY')
