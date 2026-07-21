#!/usr/bin/env python3
# fakesystemd.py – Complete systemd emulator with full D-Bus properties and FD closure.

import sys
import os
import json
import time
import threading
import socket
import logging
import signal
import grp
import pwd
import tempfile
import array
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

DEFAULT_CONFIG_PATH = "/etc/fake_systemd/config.json"
DEFAULT_NOTIFY_SOCKET = "/run/systemd/notify"
DEFAULT_BUS_NAME = "org.freedesktop.systemd1"
DEFAULT_OBJECT_PATH = "/org/freedesktop/systemd1"
DEFAULT_JOURNAL_PATH = "/var/log/fake_systemd/journal.log"

# Default units to satisfy dependency checks
DEFAULT_UNITS = {
    "sysinit.target": {"type": "target", "active_state": "active", "sub_state": "running"},
    "basic.target": {"type": "target", "active_state": "active", "sub_state": "running"},
    "network.target": {"type": "target", "active_state": "active", "sub_state": "running"},
    "time-sync.target": {"type": "target", "active_state": "active", "sub_state": "running"},
    "multi-user.target": {"type": "target", "active_state": "active", "sub_state": "running"},
    "graphical.target": {"type": "target", "active_state": "active", "sub_state": "running"},
}


@dataclass
class UnitConfig:
    name: str
    type: str
    active_state: str = "active"
    sub_state: str = "running"
    load_state: str = "loaded"
    description: str = ""
    load_error: str = ""
    job_id: int = 0
    job_type: str = ""
    job_state: str = ""
    pid: int = 0
    exec_path: str = ""
    main_pid: int = 0
    control_pid: int = 0
    memory_current: int = 0
    cpu_usage: float = 0.0
    tasks_current: int = 0
    unit_file_state: str = "enabled"


@dataclass
class JobConfig:
    id: int
    unit_name: str
    job_type: str
    state: str = "running"


class Config:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.units: Dict[str, UnitConfig] = {}
        self.jobs: Dict[int, JobConfig] = {}
        self.notify_socket_path = DEFAULT_NOTIFY_SOCKET
        self.bus_name = DEFAULT_BUS_NAME
        self.object_path = DEFAULT_OBJECT_PATH
        self.journal_path: Optional[str] = DEFAULT_JOURNAL_PATH
        self.socket_mode: int = 0o666
        self.socket_user: str = "root"
        self.socket_group: str = "root"
        self.load()

    def load(self):
        if not os.path.exists(self.config_path):
            self._create_default_config()
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
            self._parse_config(data)
        except Exception as e:
            logging.error(f"Failed to load config: {e}, using defaults")
            self._create_default_config()

    def _create_default_config(self):
        default = {
            "units": {**DEFAULT_UNITS, **{
                "test.service": {
                    "type": "service",
                    "active_state": "active",
                    "sub_state": "running",
                    "description": "Test service",
                    "pid": 1234,
                    "exec_path": "/usr/bin/test",
                    "main_pid": 1234
                },
                "test.socket": {
                    "type": "socket",
                    "active_state": "active",
                    "sub_state": "running",
                    "description": "Test socket"
                }
            }},
            "notify_socket": DEFAULT_NOTIFY_SOCKET,
            "bus_name": DEFAULT_BUS_NAME,
            "object_path": DEFAULT_OBJECT_PATH,
            "journal_path": DEFAULT_JOURNAL_PATH,
            "socket_mode": "666",
            "socket_user": "root",
            "socket_group": "root"
        }
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(default, f, indent=2)
        self._parse_config(default)

    def _parse_config(self, data):
        self.notify_socket_path = data.get("notify_socket", DEFAULT_NOTIFY_SOCKET)
        self.bus_name = data.get("bus_name", DEFAULT_BUS_NAME)
        self.object_path = data.get("object_path", DEFAULT_OBJECT_PATH)
        self.journal_path = data.get("journal_path", DEFAULT_JOURNAL_PATH)
        if "socket_mode" in data:
            self.socket_mode = int(data["socket_mode"], 8)
        self.socket_user = data.get("socket_user", "root")
        self.socket_group = data.get("socket_group", "root")
        for name, params in data.get("units", {}).items():
            u = UnitConfig(
                name=name,
                type=params.get("type", "service"),
                active_state=params.get("active_state", "active"),
                sub_state=params.get("sub_state", "running"),
                load_state=params.get("load_state", "loaded"),
                description=params.get("description", ""),
                pid=params.get("pid", 0),
                exec_path=params.get("exec_path", ""),
                main_pid=params.get("main_pid", 0),
                memory_current=params.get("memory_current", 0),
                cpu_usage=params.get("cpu_usage", 0.0),
                tasks_current=params.get("tasks_current", 0),
                unit_file_state=params.get("unit_file_state", "enabled")
            )
            self.units[name] = u


class Unit(dbus.service.Object):
    """Unit object implementing org.freedesktop.systemd1.Unit and DBus.Properties."""
    def __init__(self, bus, object_path, config: UnitConfig, manager):
        self.config = config
        self.manager = manager
        dbus.service.Object.__init__(self, bus, object_path)

    # ---- org.freedesktop.DBus.Properties ----
    @dbus.service.method(dbus_interface='org.freedesktop.DBus.Properties',
                         in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        if interface_name == 'org.freedesktop.systemd1.Unit':
            if property_name == 'Id':
                return dbus.String(self.config.name)
            if property_name == 'LoadState':
                return dbus.String(self.config.load_state)
            if property_name == 'ActiveState':
                return dbus.String(self.config.active_state)
            if property_name == 'SubState':
                return dbus.String(self.config.sub_state)
            if property_name == 'Description':
                return dbus.String(self.config.description)
            if property_name == 'UnitFileState':
                return dbus.String(self.config.unit_file_state)
            if property_name == 'MainPID':
                return dbus.UInt32(self.config.main_pid)
            if property_name == 'MemoryCurrent':
                return dbus.UInt64(self.config.memory_current)
            if property_name == 'CPUUsageNSec':
                return dbus.UInt64(int(self.config.cpu_usage * 1e9))
            if property_name == 'TasksCurrent':
                return dbus.UInt32(self.config.tasks_current)
            if property_name == 'Following':
                return dbus.String("")
            if property_name == 'LoadError':
                return dbus.String(self.config.load_error)
        raise dbus.DBusException(f"Unknown property {property_name}")

    @dbus.service.method(dbus_interface='org.freedesktop.DBus.Properties',
                         in_signature='ssv', out_signature='')
    def Set(self, interface_name, property_name, value):
        # Ignore sets – we are a fake
        logging.debug(f"Unit.Set({interface_name}, {property_name}) ignored")

    @dbus.service.method(dbus_interface='org.freedesktop.DBus.Properties',
                         in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        if interface_name == 'org.freedesktop.systemd1.Unit':
            return {
                'Id': dbus.String(self.config.name),
                'LoadState': dbus.String(self.config.load_state),
                'ActiveState': dbus.String(self.config.active_state),
                'SubState': dbus.String(self.config.sub_state),
                'Description': dbus.String(self.config.description),
                'UnitFileState': dbus.String(self.config.unit_file_state),
                'MainPID': dbus.UInt32(self.config.main_pid),
                'MemoryCurrent': dbus.UInt64(self.config.memory_current),
                'CPUUsageNSec': dbus.UInt64(int(self.config.cpu_usage * 1e9)),
                'TasksCurrent': dbus.UInt32(self.config.tasks_current),
                'Following': dbus.String(""),
                'LoadError': dbus.String(self.config.load_error),
            }
        return {}

    # ---- org.freedesktop.systemd1.Unit methods ----
    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Unit',
                         out_signature='s')
    def GetUnitFileState(self):
        return self.config.unit_file_state

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Unit',
                         out_signature='a{sv}')
    def Describe(self):
        return self.GetAll('org.freedesktop.systemd1.Unit')

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Unit',
                         out_signature='s')
    def UnitFileState(self):
        return self.config.unit_file_state

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Unit',
                         in_signature='s', out_signature='')
    def Reload(self, mode):
        self.config.sub_state = "reloading"
        self.manager._emit_unit_changed(self.config.name)

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Unit',
                         in_signature='s', out_signature='')
    def Freeze(self, mode):
        self.config.active_state = "frozen"
        self.manager._emit_unit_changed(self.config.name)

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Unit',
                         out_signature='')
    def Thaw(self):
        self.config.active_state = "active"
        self.manager._emit_unit_changed(self.config.name)


class Job(dbus.service.Object):
    def __init__(self, bus, object_path, job_config: JobConfig, manager):
        self.config = job_config
        self.manager = manager
        dbus.service.Object.__init__(self, bus, object_path)

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Job',
                         out_signature='ssso')
    def Get(self):
        return (self.config.unit_name, self.config.job_type, self.config.state,
                dbus.ObjectPath(f"{self.manager.object_path}/unit/{self.config.unit_name.replace('.', '_')}"))


class Manager(dbus.service.Object):
    def __init__(self, bus, object_path, config: Config):
        self.config = config
        self.object_path = object_path
        self.units: Dict[str, Unit] = {}
        self.jobs: Dict[int, Job] = {}
        self.next_job_id = 1
        self.bus = bus
        dbus.service.Object.__init__(self, bus, object_path)
        self._create_units()

    def _emit_unit_changed(self, name):
        pass

    def _create_units(self):
        for name, ucfg in self.config.units.items():
            path = f"{self.object_path}/unit/{name.replace('.', '_')}"
            unit = Unit(self.bus, path, ucfg, self)
            self.units[name] = unit

    def _get_or_create_unit(self, name):
        if name not in self.units:
            ucfg = UnitConfig(
                name=name,
                type="service",
                active_state="active",
                sub_state="running",
                load_state="loaded",
                description=f"Auto-created unit {name}",
                unit_file_state="enabled"
            )
            self.config.units[name] = ucfg
            path = f"{self.object_path}/unit/{name.replace('.', '_')}"
            unit = Unit(self.bus, path, ucfg, self)
            self.units[name] = unit
            logging.debug(f"Auto-created unit {name}")
        return self.units[name]

    def _get_unit_path(self, name):
        return f"{self.object_path}/unit/{name.replace('.', '_')}"

    def _create_job(self, unit_name, job_type):
        job_id = self.next_job_id
        self.next_job_id += 1
        job_config = JobConfig(id=job_id, unit_name=unit_name, job_type=job_type, state="running")
        job_path = f"{self.object_path}/job/{job_id}"
        job = Job(self.bus, job_path, job_config, self)
        self.jobs[job_id] = job
        return job_path

    # ---- Manager Properties via DBus.Properties ----
    @dbus.service.method(dbus_interface='org.freedesktop.DBus.Properties',
                         in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        if interface_name == 'org.freedesktop.systemd1.Manager':
            if property_name == 'Version':
                return dbus.String(self.GetVersion())
            if property_name == 'Features':
                return dbus.String(self.GetFeatures())
            if property_name == 'Virtualization':
                return dbus.String(self.GetVirtualization())
            if property_name == 'Architecture':
                return dbus.String(self.GetArchitecture())
            if property_name == 'Environment':
                return dbus.String(self.GetEnvironment())
            if property_name == 'ControlGroup':
                return dbus.String("")
            if property_name == 'DefaultControlGroup':
                return dbus.String("")
        raise dbus.DBusException(f"Unknown property {property_name}")

    @dbus.service.method(dbus_interface='org.freedesktop.DBus.Properties',
                         in_signature='ssv', out_signature='')
    def Set(self, interface_name, property_name, value):
        logging.debug(f"Manager.Set({interface_name}, {property_name}) ignored")

    @dbus.service.method(dbus_interface='org.freedesktop.DBus.Properties',
                         in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        if interface_name == 'org.freedesktop.systemd1.Manager':
            return {
                'Version': dbus.String(self.GetVersion()),
                'Features': dbus.String(self.GetFeatures()),
                'Virtualization': dbus.String(self.GetVirtualization()),
                'Architecture': dbus.String(self.GetArchitecture()),
                'Environment': dbus.String(self.GetEnvironment()),
                'ControlGroup': dbus.String(""),
                'DefaultControlGroup': dbus.String(""),
            }
        return {}

    # ---- Manager methods ----
    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='s')
    def GetVersion(self):
        return "247"

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='s')
    def GetFeatures(self):
        return "+PAM +AUDIT +SELINUX +IMA -APPARMOR +SMACK +SECCOMP +GCRYPT +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN +IPTC +KMOD +LIBCRYPTSETUP +LIBFDISK +PCRE2 +PWQUALITY +P11KIT +QRENCODE +BZIP2 +LZ4 +XZ +ZLIB +ZSTD +XKBCOMMON +UTMP +SYSVINIT +LIBARCHIVE"

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='s')
    def GetVirtualization(self):
        return "none"

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='s')
    def GetArchitecture(self):
        return "x86-64"

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='s')
    def GetEnvironment(self):
        return "LANG=en_US.UTF-8"

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='ss', out_signature='o')
    def StartUnit(self, name, mode):
        unit = self._get_or_create_unit(name)
        unit.config.active_state = "active"
        unit.config.sub_state = "running"
        job_path = self._create_job(name, "start")
        return dbus.ObjectPath(job_path)

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='ss', out_signature='o')
    def StopUnit(self, name, mode):
        unit = self._get_or_create_unit(name)
        unit.config.active_state = "inactive"
        unit.config.sub_state = "stopped"
        job_path = self._create_job(name, "stop")
        return dbus.ObjectPath(job_path)

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='ss', out_signature='o')
    def RestartUnit(self, name, mode):
        unit = self._get_or_create_unit(name)
        unit.config.active_state = "active"
        unit.config.sub_state = "running"
        job_path = self._create_job(name, "restart")
        return dbus.ObjectPath(job_path)

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='s', out_signature='o')
    def GetUnit(self, name):
        unit = self._get_or_create_unit(name)
        return dbus.ObjectPath(self._get_unit_path(name))

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='u', out_signature='o')
    def GetUnitByPID(self, pid):
        for name, unit in self.units.items():
            if unit.config.main_pid == int(pid):
                return dbus.ObjectPath(self._get_unit_path(name))
        dummy = f"pid-{pid}.service"
        self._get_or_create_unit(dummy)
        return dbus.ObjectPath(self._get_unit_path(dummy))

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='a(sssssssso)')
    def ListUnits(self):
        result = []
        for name, unit in self.units.items():
            result.append((
                name,
                unit.config.description or name,
                unit.config.load_state,
                unit.config.active_state,
                unit.config.sub_state,
                "",
                self._get_unit_path(name),
                str(unit.config.job_id) if unit.config.job_id else "",
                dbus.ObjectPath(self._get_unit_path(name))
            ))
        return result

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='as', out_signature='a(sssssssso)')
    def ListUnitsFiltered(self, states):
        return self.ListUnits()

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='s', out_signature='s')
    def GetUnitFileState(self, name):
        return "enabled"

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='as')
    def ListUnitFiles(self):
        return [name for name in self.units.keys()]

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='asbb', out_signature='b')
    def EnableUnitFiles(self, files, runtime, force):
        for f in files:
            name = os.path.basename(f)
            self._get_or_create_unit(name)
        return True

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='asb', out_signature='b')
    def DisableUnitFiles(self, files, runtime):
        for f in files:
            name = os.path.basename(f)
            if name in self.units:
                self.units[name].config.unit_file_state = "disabled"
        return True

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='s', out_signature='')
    def Reload(self, mode):
        pass

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='')
    def Reexecute(self):
        pass

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='si', out_signature='')
    def KillUnit(self, name, signal):
        if name in self.units:
            pass

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='s', out_signature='')
    def ResetFailedUnit(self, name):
        if name in self.units:
            self.units[name].config.active_state = "active"

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='a(ussso)')
    def ListJobs(self):
        result = []
        for job_id, job in self.jobs.items():
            result.append((job_id, job.config.unit_name, job.config.job_type, job.config.state,
                           dbus.ObjectPath(self._get_unit_path(job.config.unit_name))))
        return result

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='u', out_signature='o')
    def GetJob(self, job_id):
        if job_id not in self.jobs:
            raise dbus.DBusException("Job not found")
        return dbus.ObjectPath(f"{self.object_path}/job/{job_id}")

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         out_signature='a(sbssss)')
    def GetUnitFileInfo(self):
        result = []
        for name, unit in self.units.items():
            result.append((name, True, "enabled", "enabled", "", ""))
        return result

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='s', out_signature='a(sbssss)')
    def GetUnitFileInfoByName(self, name):
        if name in self.units:
            return [(name, True, "enabled", "enabled", "", "")]
        return []

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='sba(sv)', out_signature='')
    def SetUnitProperties(self, name, runtime, properties):
        logging.debug(f"SetUnitProperties({name}, {runtime}, {properties}) ignored")

    @dbus.service.method(dbus_interface='org.freedesktop.systemd1.Manager',
                         in_signature='s', out_signature='a(sus)')
    def GetUnitProcesses(self, name):
        if name in self.units:
            pid = self.units[name].config.main_pid
            if pid:
                return [(pid, self.units[name].config.exec_path, 0)]
        return []


class NotifyListener:
    def __init__(self, config: Config, callback):
        self.config = config
        self.callback = callback
        self.socket_path = config.notify_socket_path
        self.running = False
        self.thread = None
        self.server = None

    def _find_usable_socket_path(self):
        paths_to_try = [self.socket_path]
        if os.geteuid() != 0:
            runtime_dir = os.environ.get('XDG_RUNTIME_DIR')
            if runtime_dir:
                user_socket = os.path.join(runtime_dir, 'systemd', 'notify')
                paths_to_try.append(user_socket)
            uid = os.geteuid()
            user_run = f"/run/user/{uid}/systemd/notify"
            paths_to_try.append(user_run)
        for p in paths_to_try:
            try:
                test_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                if os.path.exists(p):
                    os.unlink(p)
                test_sock.bind(p)
                test_sock.close()
                os.unlink(p)
                return p
            except Exception:
                continue
        return None

    def start(self):
        actual_path = self._find_usable_socket_path()
        if not actual_path:
            logging.warning("Could not find writable socket path for sd_notify. Notify disabled.")
            self.socket_path = None
            return

        if os.path.exists(actual_path):
            os.unlink(actual_path)
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server.bind(actual_path)
        try:
            os.chmod(actual_path, self.config.socket_mode)
            uid = pwd.getpwnam(self.config.socket_user).pw_uid
            gid = grp.getgrnam(self.config.socket_group).gr_gid
            os.chown(actual_path, uid, gid)
        except Exception:
            pass
        self.socket_path = actual_path
        os.environ['NOTIFY_SOCKET'] = actual_path
        logging.info(f"sd_notify socket at {actual_path}")
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        while self.running and self.server:
            try:
                data, ancdata, flags, addr = self.server.recvmsg(4096, 1024)
                if data:
                    self.callback(data.decode('utf-8', errors='ignore'))
                if ancdata:
                    for cmsg_level, cmsg_type, cmsg_data in ancdata:
                        if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
                            fds = array.array('i')
                            fds.frombytes(cmsg_data[:len(cmsg_data) - (len(cmsg_data) % fds.itemsize)])
                            for fd in fds:
                                try:
                                    os.close(fd)
                                    logging.debug(f"Closed FD {fd}")
                                except OSError:
                                    pass
            except Exception as e:
                if self.running:
                    logging.error(f"Notify error: {e}")

    def stop(self):
        self.running = False
        if self.server:
            self.server.close()
            self.server = None
        if self.thread:
            self.thread.join(timeout=1)


def log_journal(message, journal_path):
    if not journal_path:
        logging.info(f"Journal: {message}")
        return
    try:
        dirname = os.path.dirname(journal_path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        with open(journal_path, 'a') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
    except Exception as e:
        logging.error(f"Failed to write journal: {e}")
        logging.info(f"Journal entry: {message}")


class FakeSystemd:
    def __init__(self, config_path=None):
        self.config = Config(config_path)
        self.bus_name = self.config.bus_name
        self.object_path = self.config.object_path
        self.loop = None
        self.manager = None
        self.notify_listener = None

    def _notify_callback(self, message):
        logging.info(f"sd_notify: {message}")
        log_journal(f"sd_notify: {message}", self.config.journal_path)

    def start(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SystemBus() if os.geteuid() == 0 else dbus.SessionBus()
        try:
            session_bus.request_name(self.bus_name, dbus.bus.NAME_FLAG_REPLACE_EXISTING)
        except dbus.DBusException as e:
            logging.error(f"Failed to acquire bus name: {e}")
            return False

        self.manager = Manager(session_bus, self.object_path, self.config)
        self.loop = GLib.MainLoop()

        self.notify_listener = NotifyListener(self.config, self._notify_callback)
        self.notify_listener.start()

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logging.info(f"Fake systemd running with bus name {self.bus_name}")
        self.loop.run()
        return True

    def _signal_handler(self, sig, frame):
        logging.info("Received signal, stopping...")
        if self.loop:
            self.loop.quit()
        if self.notify_listener:
            self.notify_listener.stop()

    def stop(self):
        if self.notify_listener:
            self.notify_listener.stop()
        if self.loop:
            self.loop.quit()


def run_tests():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.json")
        config = Config(config_path)
        assert config.units, "No units loaded"

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus() if os.geteuid() == 0 else dbus.SessionBus()
        manager = Manager(bus, DEFAULT_OBJECT_PATH, config)

        units = manager.ListUnits()
        assert len(units) > 0, "ListUnits empty"

        unit_name = list(config.units.keys())[0]
        job_path = manager.StartUnit(unit_name, "replace")
        assert job_path.startswith('/'), "Invalid job path"

        unit_path = manager.GetUnit(unit_name)
        assert unit_path == f"{DEFAULT_OBJECT_PATH}/unit/{unit_name.replace('.', '_')}"

        state = manager.GetUnitFileState(unit_name)
        assert state in ["enabled", "disabled", "not-found"], "Invalid state"

        unit_obj = manager.units[unit_name]
        state2 = unit_obj.GetUnitFileState()
        assert state2 == state, "Unit state mismatch"

        assert manager.GetVersion(), "Missing version"

        jobs = manager.ListJobs()
        assert isinstance(jobs, list), "ListJobs failed"

        pid = unit_obj.config.main_pid
        if pid:
            path = manager.GetUnitByPID(pid)
            assert path == unit_path, "PID lookup failed"

        result = manager.EnableUnitFiles(["new.service"], False, False)
        assert result is True, "EnableUnitFiles failed"
        assert "new.service" in manager.units, "Unit not created"

        print("All tests passed.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fake systemd emulator")
    parser.add_argument("--config", help="Path to config JSON", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--test", action="store_true", help="Run self-tests and exit")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.test:
        run_tests()
        sys.exit(0)

    fd = FakeSystemd(args.config)
    try:
        fd.start()
    except KeyboardInterrupt:
        fd.stop()
        print("Exited.")