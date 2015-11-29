#!/bin/env python

import os
import sys
from XenServer import XenServer
from GELF import GELF
import traceback


try:
    xs_session = XenServer().make_session()

    #Get all VMs in the pool
    pool_vms = xs_session.xenapi.VM.get_all()
    #Get Pool info to match CPU with this pool
    pool = xs_session.xenapi.pool.get_all()[0]
    pool_uuid = xs_session.xenapi.pool.get_uuid(pool)


    for vm in pool_vms:
        vm_record = xs_session.xenapi.VM.get_record(vm)
        #Check if it's really a VM (not the dom0, template or snapshot)
        if not(vm_record["is_control_domain"]) and not(vm_record["is_a_snapshot"]) and not (vm_record["is_a_template"]):
            # Format data
            data = {
                'short_message': os.path.basename(__file__).split('.')[0],
                '_pool_uuid': pool_uuid,
                '_name_description': vm_record["name_description"],
                '_name_label': vm_record["name_label"],
                '_power_state': vm_record["power_state"],
                '_vm_uuid': vm_record["uuid"],
                '_VCPUs_at_startup': vm_record["VCPUs_at_startup"],
                '_VCPUs_max': vm_record["VCPUs_max"],
                '_memory_dynamic_max': vm_record["memory_dynamic_max"],
                '_memory_dynamic_min': vm_record["memory_dynamic_min"],
                '_memory_static_max': vm_record["memory_static_max"],
                '_dom_arch': vm_record["domarch"],
                '_tags': vm_record["tags"]
            }
            if vm_record["other_config"]:
                for key, value in vm_record["other_config"].iteritems():
                    data['_other_config_'+key] = value

            if vm_record["platform"]:
                for key, value in vm_record["platform"].iteritems():
                    data['_platform_'+key] = value

            #Get supplemental data
            if vm_record["guest_metrics"] != "OpaqueRef:NULL":
                os_data = xs_session.xenapi.VM_guest_metrics.get_os_version(vm_record["guest_metrics"])
                for key, value in os_data.iteritems():
                    data['_os_version_'+key] = value

                pv_drivers_version = xs_session.xenapi.VM_guest_metrics.get_PV_drivers_version(vm_record["guest_metrics"])
                f_pv_drv_version = pv_drivers_version['major'] + "." + pv_drivers_version['minor'] + "." + pv_drivers_version['build']
                data['_pv_drv_version'] = f_pv_drv_version

            if vm_record["resident_on"] != "OpaqueRef:NULL":
                data['_host_uuid'] = xs_session.xenapi.host.get_uuid(vm_record["resident_on"])
                data['_host_hostname'] = xs_session.xenapi.host.get_hostname(vm_record["resident_on"])
            GELF().log_udp(data)

except:
    sys.stderr.write('ERROR: %s\n' % traceback.format_exc())


