from Simple_Flask import app
import sys
debug=False
local=False

if "--debug" in sys.argv[1:]:
    debug=True
    print ("### ENSURE THAT DEBUG IS NOT ENABLED ON PRODUCTION ###")

if "--local" in sys.argv[1:]:
    local=True

if debug:
    app.config["DEBUG"] = True

if local:
    app.run()
else:
    context = ('cert.crt', 'key.key') # edit file to point at actual certs
    app.run("0.0.0.0",443, ssl_context=context) # listen on any IP address

