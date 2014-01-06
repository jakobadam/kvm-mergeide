#!/usr/bin/env python
import sys
import guestfs
import tempfile
import hivex

def create_merge_file(path):
    """Create mergeide.reg with the link to the proper controlset.

    The original file points to a CurrentControlSet key in the registry
    However, that key is not present when the guest is not running.

    This function creates a mergeide.reg file with the proper controlsetvalue.
    """
    g = mount(path)
    hive = download_system_hive(g)
    cset = get_current_control_set(hive)

    template = None
    with open('mergeide.reg.template') as f:
        template = f.read()

    with open('mergeide.reg', 'w') as f:
        f.write(template % {'cset':cset})

def mount(path):
    """Mount windows guest with the given path."""
    g = guestfs.GuestFS()
    g.add_drive_opts(path, readonly=True)
    g.launch()

    roots = g.inspect_os()
    if len(roots) == 0:
        raise Exception("%s: no operating system found in the disk image" % (path))

    root = roots[0]

    if g.inspect_get_type(root) != "windows":
        raise Exception("%s disk: not a Windows guest")

    # mount image read only
    g.mount_ro(root, "/")
    g.__root = root
    return g

def download_system_hive(g):
    system_config_path = None
    system_root = g.inspect_get_windows_systemroot(g.__root)
    system_config_path = g.case_sensitive_path("%s/system32/config" % system_root)
    if not system_config_path:
        raise Exception("Ups. Couldn't locate Windows system config dir")

    system_path = g.case_sensitive_path("%s/system" % system_config_path)
    fhandle,local_system_hive_path = tempfile.mkstemp('system_hive')
    g.download(system_path, local_system_hive_path)
    system_hive = hivex.Hivex(local_system_hive_path)
    return system_hive

def get_current_control_set(system_hive):
    # more about windows reg control sets:
    # http://support.microsoft.com/kb/100010

    # Firstly get HKLM\SYSTEM\Select so we know which
    # ControlSetNNN is in use
    h = system_hive
    h_root = h.root()
    node = h.node_get_child(h_root, "Select")
    val = h.node_get_value(node, "Current")
    cset = "ControlSet%03d" % h.value_dword(val)
    return cset

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("usage: mergeide_create_reg.py <image>")
    create_merge_file(sys.argv[1])
