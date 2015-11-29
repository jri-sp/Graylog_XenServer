#!/bin/env python

import os
import sys
from XenServer import XenServer
from GELF import GELF
import traceback


try:
    xs_session = XenServer().make_session()

    #Get all CPUs info in the pool
    host_CPUs = xs_session.xenapi.host_cpu.get_all()
    #Get Pool info to match CPU with this pool
    pool = xs_session.xenapi.pool.get_all()[0]
    pool_uuid = xs_session.xenapi.pool.get_uuid(pool)

    for cpu in host_CPUs:
        cpu_record = xs_session.xenapi.host_cpu.get_record(cpu)
        if(cpu_record["host"] != "OpaqueRef:NULL"):
            host_uuid = xs_session.xenapi.host.get_uuid(cpu_record["host"])
            host_hostname = xs_session.xenapi.host.get_hostname(cpu_record["host"])

        data = {
            'short_message': os.path.basename(__file__).split('.')[0],
            '_pool_uuid': pool_uuid,
            '_host_uuid': host_uuid,
            '_host_hostname': host_hostname,
            '_cpu_uuid': cpu_record["uuid"],
            '_cpu_family': cpu_record["family"],
            '_cpu_features': cpu_record["features"],
            '_cpu_flags': cpu_record["flags"],
            '_cpu_model': cpu_record["model"],
            '_cpu_modelname': cpu_record["modelname"],
            '_cpu_number': cpu_record["number"],
            '_cpu_other_config': cpu_record["other_config"],
            '_cpu_speed': cpu_record["speed"],
            '_cpu_stepping': cpu_record["stepping"],
            '_cpu_utilisation': cpu_record["utilisation"],
            '_cpu_vendor': cpu_record["vendor"],
        }

        GELF().log_udp(data)

except Exception, e:
    sys.stderr.write('ERROR: %s\n' % traceback.format_exc())


