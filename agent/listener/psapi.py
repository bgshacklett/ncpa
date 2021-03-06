import psutil as ps
import os
import logging
import datetime
import time
import re
import platform
import server
from nodes import ParentNode, RunnableNode, RunnableParentNode, LazyNode
from pluginnodes import PluginAgentNode
import services
import processes
import environment


importables = (
    'windowscounters',
    'windowslogs'
)

def get_uptime():
    current_time = time.time()
    epoch_boot = int(current_time)
    return ([epoch_boot - ps.BOOT_TIME], 's')


def make_disk_nodes(disk_name):
    read_time = RunnableNode('read_time', method=lambda: (ps.disk_io_counters(perdisk=True)[disk_name].read_time, 'ms'))
    write_time = RunnableNode('write_time',
                              method=lambda: (ps.disk_io_counters(perdisk=True)[disk_name].write_time, 'ms'))
    read_count = RunnableNode('read_count',
                              method=lambda: (ps.disk_io_counters(perdisk=True)[disk_name].read_count, 'c'))
    write_count = RunnableNode('write_count',
                               method=lambda: (ps.disk_io_counters(perdisk=True)[disk_name].write_count, 'c'))
    read_bytes = RunnableNode('read_bytes',
                              method=lambda: (ps.disk_io_counters(perdisk=True)[disk_name].read_bytes, 'b'))
    write_bytes = RunnableNode('write_bytes',
                               method=lambda: (ps.disk_io_counters(perdisk=True)[disk_name].write_bytes, 'b'))
    return ParentNode(disk_name, children=[read_time, write_time, read_count, write_count, read_bytes, write_bytes])


def make_mountpoint_nodes(partition_name):
    mountpoint = partition_name.mountpoint
    total_size = RunnableNode('total_size', method=lambda: (ps.disk_usage(mountpoint).total, 'b'))
    used = RunnableNode('used', method=lambda: (ps.disk_usage(mountpoint).used, 'b'))
    free = RunnableNode('free', method=lambda: (ps.disk_usage(mountpoint).free, 'b'))
    used_percent = RunnableNode('used_percent', method=lambda: (ps.disk_usage(mountpoint).percent, '%'))
    device_name = RunnableNode('device_name', method=lambda: ([partition_name.device], 'name'))
    safe_mountpoint = re.sub(r'[\\/]+', '|', mountpoint)
    return RunnableParentNode(safe_mountpoint,
                              children=[total_size, used, free, used_percent, device_name],
                              primary='used_percent',
                              include=('total_size', 'used', 'free', 'used_percent'))


def make_if_nodes(if_name):
    bytes_sent = RunnableNode('bytes_sent', method=lambda: (ps.net_io_counters(pernic=True)[if_name].bytes_sent, 'b'))
    bytes_recv = RunnableNode('bytes_recv', method=lambda: (ps.net_io_counters(pernic=True)[if_name].bytes_recv, 'b'))
    packets_sent = RunnableNode('packets_sent',
                                method=lambda: (ps.net_io_counters(pernic=True)[if_name].packets_sent, 'c'))
    packets_recv = RunnableNode('packets_recv',
                                method=lambda: (ps.net_io_counters(pernic=True)[if_name].packets_recv, 'c'))
    errin = RunnableNode('errin', method=lambda: (ps.net_io_counters(pernic=True)[if_name].errin, 'c'))
    errout = RunnableNode('errout', method=lambda: (ps.net_io_counters(pernic=True)[if_name].errout, 'c'))
    dropin = RunnableNode('dropin', method=lambda: (ps.net_io_counters(pernic=True)[if_name].dropin, 'c'))
    dropout = RunnableNode('dropout', method=lambda: (ps.net_io_counters(pernic=True)[if_name].dropout, 'c'))
    return ParentNode(if_name,
                      children=[bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout])


def get_system_node():
    sys_system = RunnableNode('system', method=lambda: ([platform.uname()[0]], 'name'))
    sys_node = RunnableNode('node', method=lambda: ([platform.uname()[1]], 'name'))
    sys_release = RunnableNode('release', method=lambda: ([platform.uname()[2]], 'name'))
    sys_version = RunnableNode('version', method=lambda: ([platform.uname()[3]], 'name'))
    sys_machine = RunnableNode('machine', method=lambda: ([platform.uname()[4]], 'name'))
    sys_processor = RunnableNode('processor', method=lambda: ([platform.uname()[5]], 'name'))
    sys_uptime = RunnableNode('uptime', method=get_uptime)
    sys_agent = RunnableNode('agent_version', method=lambda: ([server.__VERSION__], ''))
    return ParentNode('system', children=[sys_system, sys_node, sys_release, sys_version, sys_machine, sys_processor, sys_uptime, sys_agent])


def get_cpu_node():
    cpu_count = RunnableNode('count', method=lambda: ([len(ps.cpu_percent(percpu=True))], 'c'))
    cpu_percent = LazyNode('percent', method=lambda: (ps.cpu_percent(interval=1, percpu=True), '%'))
    cpu_user = RunnableNode('user', method=lambda: ([x.user for x in ps.cpu_times(percpu=True)], 'ms'))
    cpu_system = RunnableNode('system', method=lambda: ([x.system for x in ps.cpu_times(percpu=True)], 'ms'))
    cpu_idle = RunnableNode('idle', method=lambda: ([x.idle for x in ps.cpu_times(percpu=True)], 'ms'))
    return ParentNode('cpu', children=[cpu_count, cpu_system, cpu_percent, cpu_user, cpu_idle])


def get_memory_node():
    mem_virt_total = RunnableNode('total', method=lambda: (ps.virtual_memory().total, 'b'))
    mem_virt_available = RunnableNode('available', method=lambda: (ps.virtual_memory().available, 'b'))
    mem_virt_percent = RunnableNode('percent', method=lambda: (ps.virtual_memory().percent, '%'))
    mem_virt_used = RunnableNode('used', method=lambda: (ps.virtual_memory().used, 'B'))
    mem_virt_free = RunnableNode('free', method=lambda: (ps.virtual_memory().free, 'B'))
    mem_virt = RunnableParentNode('virtual',
                          primary='percent',
                          children=(mem_virt_total, mem_virt_available, mem_virt_free, mem_virt_percent, mem_virt_used))
    mem_swap_total = RunnableNode('total', method=lambda: (ps.swap_memory().total, 'b'))
    mem_swap_percent = RunnableNode('percent', method=lambda: (ps.swap_memory().percent, '%'))
    mem_swap_used = RunnableNode('used', method=lambda: (ps.swap_memory().used, 'B'))
    mem_swap_free = RunnableNode('free', method=lambda: (ps.swap_memory().free, 'B'))
    mem_swap = RunnableParentNode('swap', primary='percent', children=[mem_swap_total, mem_swap_free, mem_swap_percent, mem_swap_used])
    return ParentNode('memory', children=[mem_virt, mem_swap])


def get_disk_node():
    disk_counters = [make_disk_nodes(x) for x in list(ps.disk_io_counters(perdisk=True).keys())]

    disk_mountpoints = []
    for x in ps.disk_partitions():
        if os.path.isdir(x.mountpoint):
            tmp = make_mountpoint_nodes(x)
            disk_mountpoints.append(tmp)

    disk_logical = ParentNode('logical', children=disk_mountpoints)
    disk_physical = ParentNode('physical', children=disk_counters)

    return ParentNode('disk', children=[disk_physical, disk_logical])


def get_interface_node():
    if_children = [make_if_nodes(x) for x in list(ps.net_io_counters(pernic=True).keys())]
    return ParentNode('interface', children=if_children)


def get_agent_node():
    plugin = PluginAgentNode('plugin')
    return ParentNode('agent', children=(plugin,))


def get_user_node():
    user_count = RunnableNode('count', method=lambda: (len([x.name for x in ps.get_users()]), 'c'))
    user_list = RunnableNode('list', method=lambda: ([x.name for x in ps.get_users()], 'name'))
    return ParentNode('user', children=[user_count, user_list])


def get_root_node():
    cpu = get_cpu_node()
    memory = get_memory_node()
    disk = get_disk_node()
    interface = get_interface_node()
    agent = get_agent_node()
    user = get_user_node()
    system = get_system_node()
    service = services.get_node()
    process = processes.get_node()

    children = [cpu, memory, disk, interface, agent, user, system, service, process]

    if environment.SYSTEM == "Windows":
        for importable in importables:
            try:
                relative_name = 'listener.' + importable
                tmp = __import__(relative_name, fromlist=['get_node'])
                get_node = getattr(tmp, 'get_node')

                node = get_node()
                children.append(node)
                logging.info("Imported %s into the API tree.", importable)
            except ImportError:
                logging.info("Could not import %s, skipping.", importable)
            except AttributeError:
                logging.warning("Trying to import %s but does not get_node() function, skipping.", importable)

    return ParentNode('root', children=children)

root = get_root_node()


def getter(accessor, config):
    # Sanity check. If accessor is None, we can do nothing meaningfully, and
    # we need to stop.
    if accessor is None:
        return
    path = [re.sub('%2f', '/', x, flags=re.I) for x in accessor.split('/') if x]
    if len(path) > 0 and path[0] == 'api':
        path = path[1:]
    return root.accessor(path, config)
