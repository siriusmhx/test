from wsgiref import simple_server
import shlex, subprocess , urllib

command_line = "powerwake 192.168.1."
query_word = 'pcwake'

CMD_SHUTDOWN = "shutdown -h now"

def query_parse(environ, start_response):
    
    query_string = environ['QUERY_STRING']
    start_response("200 OK", [('Content-Type', 'text/plain; charset=utf-8')])

    print("test ", query_string)
    if not query_string:
        return [b"Hi"]

    params = urllib.parse.parse_qs(query_string)
    print("test2")
#    print ("param:",params)

#    address = params.get('wake', ['NONE'])[0]
    address = params.get(query_word, ['NONE'])[0]

    if address == "NONE":
        return [b"Hi"]
    
    if int(address) > 0 and int(address) < 255 :
        call_powerwake(address)
        return [b'hello']

    return [b"Hi"]


def call_powerwake(octed):
    
    args = shlex.split(command_line+octed)
    # print (args)
    subprocess.call(args)

def call_shutdown(environ, start_response):
    start_response("200 OK", [('Content-Type', 'text/plain; charset=utf-8')])

    args = shlex.split(CMD_SHUTDOWN)
    subprocess.call(args)
    return [b"shutdown"]



from webdispatch import URLDispatcher
app = URLDispatcher()

#arg1:pattern name arg2:path arg3: function
#http://localhost:8080/hh 
app.add_url('wake', '/wake', query_parse)
app.add_url('shutdown', '/shutdown', call_shutdown)


def run():
    server = simple_server.make_server('', 8081, app)
    server.serve_forever()


run()
