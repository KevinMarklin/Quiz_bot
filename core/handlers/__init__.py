from . import user, admins, test_friend, indiv_opros

def setup_handlers(dp):
    dp.include_router(user.router)
    dp.include_router(admins.router)
    dp.include_router(test_friend.router)
    dp.include_router(indiv_opros.router)

