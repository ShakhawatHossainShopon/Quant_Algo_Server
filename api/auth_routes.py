from controllers.auth_controller import (
    login_controller,
    me_controller,
    logout_controller
)


def register_routes(router):
    router["/api/auth/login"] = login_controller
    router["/api/auth/me"] = me_controller
    router["/api/auth/logout"] = logout_controller
