import sys
from XenServer import XenServer
import traceback

try:
    xs_session = XenServer().make_session()

    pool = xs_session.xenapi.pool.get_all()[0]
    pool_record = xs_session.xenapi.pool.get_record(pool)

    sys.stdout.write("Successfully connected to pool: " + pool_record["name_label"]+'\n')


except Exception, e:
    sys.stderr.write('ERROR: %s\n' % traceback.format_exc())

