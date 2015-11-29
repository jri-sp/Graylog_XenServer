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
        host_record = xs_session.xenapi.host.get_record(host)
        data = {
            'short_message': os.path.basename(__file__).split('.')[0],
            '_pool_uuid': pool_uuid,
            '_host_uuid': host_record["uuid"],
            '_address': host_record["address"],
            '_software_edition': host_record["edition"],
            '_enabled': str(host_record["enabled"]),
            '_hostname': host_record["hostname"],
            '_memory_overhead': host_record["memory_overhead"],
            '_name_description': host_record["name_description"],
            '_name_label': host_record["name_label"],
            '_software_brand': host_record["software_version"]["product_brand"],
            '_software_version': host_record["software_version"]["product_version_text"],
        }

        if(host_record["metrics"] != "OpaqueRef:NULL"):
            data['_metrics_uuid:'] = xs_session.xenapi.host_metrics.get_uuid(host_record["metrics"])
            data['_memory_total'] = xs_session.xenapi.host_metrics.get_memory_total(host_record["metrics"])

        if(host_record["PIFs"] != "OpaqueRef:NULL"):
            for pif in host_record["PIFs"]:
                pif_record = xs_session.xenapi.PIF.get_record(pif)
                device = 'dvc%s' % (pif_record["device"].lstrip("eth"))
                data['_'+device+'_ip'] = pif_record["IP"]
                data['_'+device+'_ip_gateway]'] = pif_record["gateway"]
                data['_'+device+'_ip_netmask'] = pif_record["netmask"]
                data['_'+device+'_ip_mode'] = pif_record["ip_configuration_mode"]
                data['_'+device+'_mac'] = pif_record["MAC"];

        GELF().log_udp(data)

except Exception, e:
    sys.stderr.write('ERROR: %s\n' % traceback.format_exc())


