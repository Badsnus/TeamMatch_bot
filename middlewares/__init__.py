from loader import dp
from middlewares.throttling import ThrottlingMiddleware
from middlewares.register import RegisterMiddleware
from middlewares.update_user_data import UpdateUserDataMiddleware
from middlewares.set_user import SetUserMiddleware

if __name__ == 'middlewares':
    # НЕ ТРОГАЙ ПОРЯДОК!!!
    middlewares = [
        SetUserMiddleware,
        ThrottlingMiddleware,
        RegisterMiddleware,
        UpdateUserDataMiddleware
    ]
    for middleware in middlewares:
        dp.middleware.setup(middleware())
