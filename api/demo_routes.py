from controllers.demo_controller import get_demo_controller, post_demo_controller


def register_routes(router):
    # Route mapping:
    # URL -> Controller function
    router["/api/demo"] = get_demo_controller
    router["/api/demo/order"] = post_demo_controller
