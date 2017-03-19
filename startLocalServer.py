import http.server
import re
import random

HOST_NAME = "127.00.0.1"
PORT_NUMBER = 8000


#returns most recent thrust sensor data
def latestThrustSensorData():
    return str(random.randrange(100))


class CommandServer(http.server.SimpleHTTPRequestHandler):

   
    #in the future this should delete stale values after a set amount of time
    #and devices should be in charge of heartbeating
    address_table = {} #servername -> IP addr.
    vcb1_pattern = re.compile("vcb1-server")
    tcb1_pattern = re.compile("tcb1-server")
    def do_HEAD(s):
        s.send_response(200)
        s.end_headers()

    def do_GET(s):
        print("Fields:")
        print("Client addr, port", end="")
        print(s.client_address)
        print("Path: " + s.path)
        print("Server: ", end="")
        print(s.server)
        thrustSensorRegex = re.compile("thrustSensor")
        #if we found  a thrustSensor update request
        if(re.search(thrustSensorRegex, s.path) != None):
            s.wfile.write(bytes(latestThrustSensorData(), "UTF-8"))
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(s)

if __name__ == "__main__":
    server_class = http.server.HTTPServer
    defaultHandler = http.server.SimpleHTTPRequestHandler
    httpd = server_class((HOST_NAME, PORT_NUMBER), CommandServer)
    while True:
        httpd.handle_request()

    httpd.server_close()
    #in the future this could have a command line? that would be cool
    #try:
    #    httpd.serve_forever()
    #except KeyboardInterrupt:
    #    pass
    #httpd.server_close()
