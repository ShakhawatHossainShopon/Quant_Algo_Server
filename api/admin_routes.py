from controllers.admin_controller import (
    list_admins_controller,
    get_admin_controller,
    create_admin_controller,
    update_admin_controller,
    delete_admin_controller
)


def register_routes(router):
    router["/api/admin/list"] = list_admins_controller
    router["/api/admin/get"] = get_admin_controller
    router["/api/admin/create"] = create_admin_controller
    router["/api/admin/update"] = update_admin_controller
    router["/api/admin/delete"] = delete_admin_controller
