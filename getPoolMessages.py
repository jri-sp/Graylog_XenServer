#!/bin/env python

import os
import sys
from XenServer import XenServer
from GELF import GELF
import traceback
import xmlrpclib
from time import time

try:
    xs_session = XenServer().make_session()
    #last 24h messages
    messages = xs_session.xenapi.message.get_since(xmlrpclib.DateTime(time()-86400))
    #Get Pool info to match CPU with this pool
    pool = xs_session.xenapi.pool.get_all()[0]
    pool_uuid = xs_session.xenapi.pool.get_uuid(pool)

    for message in messages:
        message_record = xs_session.xenapi.message.get_record(message)

        data = {
            'short_message': os.path.basename(__file__).split('.')[0],
            '_pool_uuid': pool_uuid,
            '_body': message_record['body'],
            '_cls': message_record['cls'],
            '_name': message_record['name'],
            '_priority': message_record['priority'],
            '_obj_uuid': message_record['obj_uuid'],
            '_message_timestamp': str(message_record['timestamp'])

        }

        GELF().log_udp(data)

except:
    sys.stderr.write('ERROR: %s\n' % traceback.format_exc())


