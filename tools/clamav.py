import pyclamd

pyclamd.init_unix_socket('/var/run/clamd.scan/clamd.sock')

print pyclamd.version()
