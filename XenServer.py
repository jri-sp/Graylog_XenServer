import sys
from Config import Config
import XenAPI

class XenServer:

    def __init__(self, config = Config().read_config() ):
        # Getting config vars
        self.xs_host = config.get("XenServer", "Host")
        self.xs_url = "http://"+self.xs_host
        self.xs_username = config.get("XenServer", "Username")
        self.xs_password = config.get("XenServer", "Password")

    def make_session(self):
        try:
            # Making XenServer API Session
            session = XenAPI.Session(self.xs_url)
            session.xenapi.login_with_password(self.xs_username, self.xs_password)
        except XenAPI.Failure, e:
            if e.details[0] == 'HOST_IS_SLAVE':
                session = XenAPI.Session('http://' + e.details[1])
                session.login_with_password(self.xs_username, self.xs_password)
                sys.stdout.write(self.xs_host+" is a slave host. Trying with: "+ e.details[1]+"\n")
        except Exception, e:
            raise
        return session
