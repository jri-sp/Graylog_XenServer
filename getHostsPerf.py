#!/bin/env python

import os
import sys
from XenServer import XenServer
from GELF import GELF
import traceback

try:
    xs_session = XenServer().make_session()

    pool = xs_session.xenapi.pool.get_all()[0]
    pool_uuid = xs_session.xenapi.pool.get_uuid(pool)

    hosts = xs_session.xenapi.host.get_all()

    for host in hosts:
        hostname = xs_session.xenapi.host.get_address(host)
        try:
            perf_data = XenServer().get_rrd_data(hostname)
            host_uuid = perf_data.get_host_uuid()
            data = {
                'short_message': os.path.basename(__file__).split('.')[0],
                '_pool_uuid': pool_uuid,
                '_host_uuid': host_uuid,
                '_hostname': hostname,
            }

            for param in perf_data.get_host_param_list():
                if param != "":
                    for row in range(perf_data.get_nrows()):
                         param_data = perf_data.get_host_data(param,row)

                    if param.startswith("cpu"):
                        # CPU usage, convert to percentage
                        data['_'+param] = param_data*100

                    if param.startswith("memory"):
                        # Memory usage, already in Kilobyte
                        data['_'+param] = param_data

                    if param.startswith("pif"):
                        # Network I/O, raw data in Byte/s, convert to Kilobyte/s
                        data['_'+param+'_kib'] = param_data/1024

                    if param == "loadavg":
                        # Load average UNIX indicator
                        data['_'+param] = param_data

            GELF().log_udp(data)
        except:
            sys.stderr.write('ERROR: Can get Data from host: %s \n' % hostname)

except Exception, e:
    sys.stderr.write('ERROR: %s\n' % traceback.format_exc())


