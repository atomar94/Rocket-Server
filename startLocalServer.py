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

    #routes
    vcb1_handle = "/vcb1-server"
    heartbeat_handle = "/heartbeat"
    valve_handle = "/valves"

    def do_GET(s):
        print(s.client_address[0], end="")
        print(":", end"")
        print(s.client_address[1], end="")
        print(" > ")

       if(vcb1_handle in s.path):
            if(valve_handle in s.path):
                print("valve update")
            #handle
            pass
        elif(heartbeat_handle in s.path):
            print("heartbeat update")
        else:
            print("GET req for", end="")
            print(s.path)
            http.server.SimpleHTTPRequestHandler.do_GET(s)
            return
        s.send_response(200)


    def do_POST(self):
        pass

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
