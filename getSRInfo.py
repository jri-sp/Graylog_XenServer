#!/bin/env python

import os
import sys
from XenServer import XenServer
from GELF import GELF
import traceback


try:
    xs_session = XenServer().make_session()

    #Get all Storage Repo in the pool
    storage_repositories = xs_session.xenapi.SR.get_all()
    #Get Pool info to match CPU with this pool
    pool = xs_session.xenapi.pool.get_all()[0]
    pool_uuid = xs_session.xenapi.pool.get_uuid(pool)


    for sr in storage_repositories:
        sr_record = xs_session.xenapi.SR.get_record(sr)

        data = {
            'short_message': os.path.basename(__file__).split('.')[0],
            '_pool_uuid': pool_uuid,
            '_content_type': sr_record["content_type"],
            '_name_description': sr_record["name_description"],
            '_name_label': sr_record["name_label"],
            '_physical_size': int(sr_record["physical_size"]),
            '_physical_utilisation': int(sr_record["physical_utilisation"]),
            '_shared': str(sr_record["shared"]),
            '_sr_uuid': sr_record["uuid"],
            '_virtual_allocation': int(sr_record["virtual_allocation"]),
            '_local_cache_enabled': str(sr_record["local_cache_enabled"]),
            '_type': sr_record["type"]

        }

        GELF().log_udp(data)

except:
    sys.stderr.write('ERROR: %s\n' % traceback.format_exc())


