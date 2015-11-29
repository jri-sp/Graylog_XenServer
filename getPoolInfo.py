#!/bin/env python

import os
import sys
from XenServer import XenServer
from GELF import GELF
import traceback

try:
    xs_session = XenServer().make_session()

    pool = xs_session.xenapi.pool.get_all()[0]
    pool_record = xs_session.xenapi.pool.get_record(pool)
    master_uuid = xs_session.xenapi.host.get_uuid(pool_record["master"])
    master_hostname = xs_session.xenapi.host.get_hostname(pool_record["master"])

    data = {
        'short_message': os.path.basename(__file__).split('.')[0],
        '_master_hostname': master_hostname,
        '_master_uuid': master_uuid,
        '_name_label': pool_record["name_label"],
        '_name_description': pool_record["name_description"],
        '_pool_uuid': pool_record["uuid"],
        '_ha_enabled': str(pool_record["ha_enabled"]),
        '_ha_host_failures_to_tolerate': pool_record["ha_host_failures_to_tolerate"],
        '_ha_allow_overcommit': str(pool_record["ha_allow_overcommit"])
    }

    GELF().log_udp(data)

except Exception, e:
    sys.stderr.write('ERROR: %s\n' % traceback.format_exc())


