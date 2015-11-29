#!/bin/env python

import os
import sys
from XenServer import XenServer
from GELF import GELF
import traceback

try:
    xs_session = XenServer().make_session()

    #Get all Tasks in the pool
    tasks = xs_session.xenapi.task.get_all()
    #Get Pool info to match CPU with this pool
    pool = xs_session.xenapi.pool.get_all()[0]
    pool_uuid = xs_session.xenapi.pool.get_uuid(pool)

    for task in tasks:
        task_record = xs_session.xenapi.task.get_record(task)
        data = {
            'short_message': os.path.basename(__file__).split('.')[0],
            '_pool_uuid': pool_uuid,
            '_task_uuid': task_record["uuid"],
            '_name_description': task_record["name_description"],
            '_name_label': task_record["name_label"],
            '_allowed_operations': task_record["allowed_operations"],
            '_created': str(task_record["created"]),
            '_current_operations': task_record["current_operations"],
            '_error_info': task_record["error_info"],
            '_finished': str(task_record["finished"]),
            '_progress': task_record["progress"],
            '_result': task_record["result"],
            '_status': task_record["status"],
            '_type': task_record["type"]

        }

        GELF().log_udp(data)

except:
    sys.stderr.write('ERROR: %s\n' % traceback.format_exc())


