import time
from socket import *
try:
    import simplejson
except ImportError:
    import json as simplejson
import zlib
from Config import Config

class GELF:

    def __init__(self, config=Config().read_config()):
        self.graylog_server = config.get("GrayLog", "Host")
        self.graylog_port = int(config.get("GrayLog", "Port"))

    #Send GELF data in UDP Datagram
    def log_udp(self, data):
        try:
            # GELF "Header"
            data['version'] = '1.1'
            data['timestamp'] = time.time()
            data['host'] = gethostname()
            data['level'] = 6

            udp_socket = socket(AF_INET,SOCK_DGRAM)
            compressed_data = zlib.compress(simplejson.dumps(data).encode('utf-8'))
            udp_socket.sendto(compressed_data,(self.graylog_server,self.graylog_port))
            udp_socket.close()
        except Exception, e:
            raise
