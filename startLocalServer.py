import http.server
import re
import random
import requests

HOST_NAME = "10.10.10.1"
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

    #incoming routes
    vcb1_handle = "/vcb1-server"
    heartbeat_handle = "/heartbeat"
    valve_handle = "/valves"

    #outgoing routes
    outgoing_handle = "/outgoing"

    def do_GET(s):
        print(s.client_address[0], end="")
        print(":", end="")
        print(s.client_address[1], end="")
        print(" > ")

        if(s.vcb1_handle in s.path):
            if(s.valve_handle in s.path):
                print("valve update")
            #handle
            pass
        elif(s.heartbeat_handle in s.path):
            print("heartbeat update")
        else:
            print("GET req for", end="")
            print(s.path)
            http.server.SimpleHTTPRequestHandler.do_GET(s)
            return
        s.send_response(200)


    def do_POST(s):
        print(s.client_address[0], end="")
        print(":", end="")
        print(s.client_address[1], end="")
        print(" > ")
        print("POST req with ", end="")
        s.data_string = s.rfile.read(int(s.headers['Content-Length']))

        print(s.data_string)
        if(s.valve_handle in s.path):
            requests.post("10.10.10.3:8000", s.data_string)
            print("POST sent to 10.10.10.3")
        s.send_response(200)
        #http.server.SimpleHTTPRequestHandler.do_POST(s)
        return


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
