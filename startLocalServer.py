import http.server
import re
import random

HOST_NAME = "127.00.0.1"
PORT_NUMBER = 9000


#returns most recent thrust sensor data
def latestThrustSensorData():
	return str(random.randrange(100))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        print("GET Request for: " + s.path)
        thrustSensorRegex = re.compile("thrustSensor")
        #if we found  a thrustSensor update request
        if(re.search(thrustSensorRegex, s.path) != None):
            s.wfile.write(bytes(latestThrustSensorData(), "UTF-8"))
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(s)

if __name__ == "__main__":
    server_class = http.server.HTTPServer
    defaultHandler = http.server.SimpleHTTPRequestHandler
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
