from wsgiref import simple_server
import shlex, subprocess , urllib

SERVER_PORT = 8081
CMD_LINE = "powerwake 192.168.1."
QUERY_WORD = "pcwake"
INDEX_NAME = "wake"

def query_parse(environ, start_response):
    
    query_string = environ['QUERY_STRING']
    start_response("200 OK", [('Content-Type', 'text/plain; charset=utf-8')])

#    print (query_string)
    if not query_string:
        return [b"Hi"]

    params = urllib.parse.parse_qs(query_string)

    address = params.get(QUERY_WORD, ['NONE'])[0]

    if address == "NONE":
        return [b"Hi"]
    
    if int(address) > 0 and int(address) < 255 :
        call_powerwake(address)
        return [b'success to wake']

    return [b"fail to wake"]


def call_powerwake(octed):
    
    args = shlex.split(CMD_LINE + octed)
    # print (args)
    subprocess.call(args)
    return

def run():
    server = simple_server.make_server('', SERVER_PORT , app)
    server.serve_forever()
    return

from webdispatch import URLDispatcher
app = URLDispatcher()

app.add_url(INDEX_NAME, '/'+ INDEX_NAME, query_parse)

run()
