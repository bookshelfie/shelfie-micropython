# main file.
# This file is run after boot.py.
import usocket as socket
import ujson as json
import machine
import dht
import light
import time

CONTENT_JSON = b"""HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Response Status Code -> 200 OK
Access-Control-Allow-Methods: GET, POST
Content-Type application-json; charset=utf-8
Connection: Close
Response Body:

%s
"""

CONTENT_HTML = b"""HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Response Status Code -> 200 OK
Access-Control-Allow-Methods: GET, POST
Content-Type: text/html; charset=utf-8
Connection: Close
Response Body:

%s
"""


def parse_req(myrequest):
    """Function to pass the url and return the path"""
    myrequest = str(myrequest)
    items = myrequest.strip().split('\r\n')
    path = ""
    param_pairs = []
    for item in items:
        if 'GET' in item:
            adr = item.split()[1]
            if '?' in adr: 
                adr, params = adr.split('?', 1)
            else:
                params = []
            adr = adr.split('/')
            if params:
                param_pairs = [p.split('=') for p in  params.split('&')]
            else:
                param_pairs = []
    param_dict = {key.lower():value.lower() for [key, value] in param_pairs}
    return adr, param_dict

def exec_req(adr, param_dict):
    """Function to execute the request"""
    print("URL:", adr, param_dict)
    if adr[1] == 'locate':
        light.locate(param_dict["locate"])
        time.sleep(10)
        light.clear()
        return {'success': 'True'}
    elif adr[1] == "blink":
        if param_dict.get("color") is not None:
            light.blink(param_dict["color"])
        else:
            light.blink()
        return {'success': 'True', "message": "Blinked {}".format(param_dict.get("color"))}
    elif adr[1] == "clear":
        light.clear()
        return {'success': 'True'}
    elif adr[1] == "show_progress":
        light.show_progress(param_dict["value"])
        return {'success': 'True'}
    elif adr[1] == "":
        return """<html>
        <head>
            <title>Clock</title>
        </head>
        <body>
            <b>Clock</b>
        </body>
        </html>"""

    return {"Status": "No Action"}
    

def main(micropython_optimize=False):
    global CONTENT_JSON
    global CONTENT_HTML
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>")

    counter = 0
    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)

        if not micropython_optimize:
            client_stream = client_sock.makefile("rwb")
        else:
            client_stream = client_sock

        print("Request:")
        req = client_stream.readline()
        print(req)
        myrequest = req
        while True:
            h = client_stream.readline()
            if h == b"" or h == b"\r\n":
                break
            print(h)
            myrequest = myrequest + h
        print("----------------------")
        print(myrequest)
        url, param_dict = parse_req(myrequest)
        #print(url)
        out = exec_req(url, param_dict)
        #out = "URL: {}, PARAM: {}".format(str(url), str(param_dict))
        if isinstance(out, dict):
            response = CONTENT_JSON % (str(out).replace("'","\""))
        else:
            response = CONTENT_HTML % out
        client_stream.write(response)

        client_stream.close()
        if not micropython_optimize:
            client_sock.close()
        print()

main()
