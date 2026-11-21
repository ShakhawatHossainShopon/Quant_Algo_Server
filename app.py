from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import traceback
import inspect

from core.router import register_all_routes

HOST = "127.0.0.1"
PORT = 5000

routes = register_all_routes()


class APIHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def _execute_controller(self, controller, payload=None):
        sig = inspect.signature(controller)
        if len(sig.parameters) > 0:
            raw = controller(payload)
        else:
            raw = controller()

        if isinstance(raw, tuple) and len(raw) == 2:
            data, status = raw
        else:
            data, status = raw, 200

        return status, data

    def do_GET(self):
        if self.path == "/":
            self.send_json(200, {
                "success": True,
                "message": "Quant Algo API Server is running",
                "endpoints": list(routes.keys())
            })
            return

        path = self.path.split("?", 1)[0]
        controller = routes.get(path)

        if controller is None:
            self.send_json(404, {
                "success": False,
                "error": "Route not found",
                "requested_path": path,
                "available_routes": list(routes.keys())
            })
            return

        try:
            status, result = self._execute_controller(controller)
            self.send_json(status, result)

        except Exception as error:
            print(f"\nAPI GET ERROR: {path}")
            traceback.print_exc()
            self.send_json(500, {
                "success": False,
                "error": str(error),
                "route": path
            })

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        controller = routes.get(path)

        if controller is None:
            self.send_json(404, {
                "success": False,
                "error": "Route not found",
                "requested_path": path,
                "available_routes": list(routes.keys())
            })
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}

        try:
            status, result = self._execute_controller(controller, payload)
            self.send_json(status, result)

        except Exception as error:
            print(f"\nAPI POST ERROR: {path}")
            traceback.print_exc()
            self.send_json(500, {
                "success": False,
                "error": str(error),
                "route": path
            })

    def send_json(self, status, data):
        body = json.dumps(
            data,
            indent=4,
            default=str
        ).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format_string, *args):
        print(f"[API] {self.address_string()} - {format_string % args}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), APIHandler)

    print("=" * 45)
    print("QUANT ALGO API SERVER")
    print("=" * 45)
    print(f"Server URL: http://{HOST}:{PORT}")
    print(f"Loaded routes: {len(routes)}")

    for route in routes:
        print(f"  GET/POST {route}")

    print("=" * 45)
    print("Press CTRL+C to stop")

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nAPI server stopped.")

    finally:
        server.server_close()
