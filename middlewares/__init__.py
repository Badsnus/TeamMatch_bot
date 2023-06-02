from loader import dp
from middlewares.register import RegisterMiddleware
from middlewares.set_user import SetUserMiddleware
from middlewares.throttling import ThrottlingMiddleware
from middlewares.update_user_data import UpdateUserDataMiddleware

if __name__ == 'middlewares':
    # НЕ ТРОГАЙ ПОРЯДОК!!!
    middlewares = [
        SetUserMiddleware,
        ThrottlingMiddleware,
        RegisterMiddleware,
        UpdateUserDataMiddleware,
    ]
    for middleware in middlewares:
        dp.middleware.setup(middleware())
