# Symbols

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `Config` | class | `fakesystemD/fakesystemd.py:71` | `class Config` |
| `Describe` | method | `fakesystemD/fakesystemd.py:228` | `def Describe(self)` |
| `DisableUnitFiles` | method | `fakesystemD/fakesystemd.py:471` | `def DisableUnitFiles(self, files, runtime)` |
| `EnableUnitFiles` | method | `fakesystemD/fakesystemd.py:463` | `def EnableUnitFiles(self, files, runtime, force)` |
| `FakeSystemd` | class | `fakesystemD/fakesystemd.py:649` | `class FakeSystemd` |
| `Freeze` | method | `fakesystemD/fakesystemd.py:244` | `def Freeze(self, mode)` |
| `Get` | method | `fakesystemD/fakesystemd.py:166` | `def Get(self, interface_name, property_name)` |
| `Get` | method | `fakesystemD/fakesystemd.py:263` | `def Get(self)` |
| `Get` | method | `fakesystemD/fakesystemd.py:321` | `def Get(self, interface_name, property_name)` |
| `GetAll` | method | `fakesystemD/fakesystemd.py:202` | `def GetAll(self, interface_name)` |
| `GetAll` | method | `fakesystemD/fakesystemd.py:346` | `def GetAll(self, interface_name)` |
| `GetArchitecture` | method | `fakesystemD/fakesystemd.py:377` | `def GetArchitecture(self)` |
| `GetEnvironment` | method | `fakesystemD/fakesystemd.py:382` | `def GetEnvironment(self)` |
| `GetFeatures` | method | `fakesystemD/fakesystemd.py:367` | `def GetFeatures(self)` |
| `GetJob` | method | `fakesystemD/fakesystemd.py:511` | `def GetJob(self, job_id)` |
| `GetUnit` | method | `fakesystemD/fakesystemd.py:414` | `def GetUnit(self, name)` |
| `GetUnitByPID` | method | `fakesystemD/fakesystemd.py:420` | `def GetUnitByPID(self, pid)` |
| `GetUnitFileInfo` | method | `fakesystemD/fakesystemd.py:518` | `def GetUnitFileInfo(self)` |
| `GetUnitFileInfoByName` | method | `fakesystemD/fakesystemd.py:526` | `def GetUnitFileInfoByName(self, name)` |
| `GetUnitFileState` | method | `fakesystemD/fakesystemd.py:223` | `def GetUnitFileState(self)` |
| `GetUnitFileState` | method | `fakesystemD/fakesystemd.py:453` | `def GetUnitFileState(self, name)` |
| `GetUnitProcesses` | method | `fakesystemD/fakesystemd.py:538` | `def GetUnitProcesses(self, name)` |
| `GetVersion` | method | `fakesystemD/fakesystemd.py:362` | `def GetVersion(self)` |
| `GetVirtualization` | method | `fakesystemD/fakesystemd.py:372` | `def GetVirtualization(self)` |
| `Job` | class | `fakesystemD/fakesystemd.py:255` | `class Job(Object)` |
| `JobConfig` | class | `fakesystemD/fakesystemd.py:64` | `class JobConfig` |
| `KillUnit` | method | `fakesystemD/fakesystemd.py:490` | `def KillUnit(self, name, signal)` |
| `ListJobs` | method | `fakesystemD/fakesystemd.py:502` | `def ListJobs(self)` |
| `ListUnitFiles` | method | `fakesystemD/fakesystemd.py:458` | `def ListUnitFiles(self)` |
| `ListUnits` | method | `fakesystemD/fakesystemd.py:430` | `def ListUnits(self)` |
| `ListUnitsFiltered` | method | `fakesystemD/fakesystemd.py:448` | `def ListUnitsFiltered(self, states)` |
| `Manager` | class | `fakesystemD/fakesystemd.py:268` | `class Manager(Object)` |
| `NotifyListener` | class | `fakesystemD/fakesystemd.py:546` | `class NotifyListener` |
| `Reexecute` | method | `fakesystemD/fakesystemd.py:485` | `def Reexecute(self)` |
| `Reload` | method | `fakesystemD/fakesystemd.py:238` | `def Reload(self, mode)` |
| `Reload` | method | `fakesystemD/fakesystemd.py:480` | `def Reload(self, mode)` |
| `ResetFailedUnit` | method | `fakesystemD/fakesystemd.py:496` | `def ResetFailedUnit(self, name)` |
| `RestartUnit` | method | `fakesystemD/fakesystemd.py:405` | `def RestartUnit(self, name, mode)` |
| `Set` | method | `fakesystemD/fakesystemd.py:196` | `def Set(self, interface_name, property_name, value)` |
| `Set` | method | `fakesystemD/fakesystemd.py:341` | `def Set(self, interface_name, property_name, value)` |
| `SetUnitProperties` | method | `fakesystemD/fakesystemd.py:533` | `def SetUnitProperties(self, name, runtime, properties)` |
| `StartUnit` | method | `fakesystemD/fakesystemd.py:387` | `def StartUnit(self, name, mode)` |
| `StopUnit` | method | `fakesystemD/fakesystemd.py:396` | `def StopUnit(self, name, mode)` |
| `Thaw` | method | `fakesystemD/fakesystemd.py:250` | `def Thaw(self)` |
| `Unit` | class | `fakesystemD/fakesystemd.py:156` | `class Unit(Object)` |
| `UnitConfig` | class | `fakesystemD/fakesystemd.py:42` | `class UnitConfig` |
| `UnitFileState` | method | `fakesystemD/fakesystemd.py:233` | `def UnitFileState(self)` |
| `__init__` | method | `fakesystemD/fakesystemd.py:72` | `def __init__(self, config_path)` |
| `__init__` | method | `fakesystemD/fakesystemd.py:158` | `def __init__(self, bus, object_path, config, manager)` |
| `__init__` | method | `fakesystemD/fakesystemd.py:256` | `def __init__(self, bus, object_path, job_config, manager)` |
| `__init__` | method | `fakesystemD/fakesystemd.py:269` | `def __init__(self, bus, object_path, config)` |
| `__init__` | method | `fakesystemD/fakesystemd.py:547` | `def __init__(self, config, callback)` |
| `__init__` | method | `fakesystemD/fakesystemd.py:650` | `def __init__(self, config_path)` |
| `_create_default_config` | method | `fakesystemD/fakesystemd.py:96` | `def _create_default_config(self)` |
| `_create_job` | method | `fakesystemD/fakesystemd.py:309` | `def _create_job(self, unit_name, job_type)` |
| `_create_units` | method | `fakesystemD/fakesystemd.py:282` | `def _create_units(self)` |
| `_emit_unit_changed` | method | `fakesystemD/fakesystemd.py:279` | `def _emit_unit_changed(self, name)` |
| `_find_usable_socket_path` | method | `fakesystemD/fakesystemd.py:555` | `def _find_usable_socket_path(self)` |
| `_get_or_create_unit` | method | `fakesystemD/fakesystemd.py:288` | `def _get_or_create_unit(self, name)` |
| `_get_unit_path` | method | `fakesystemD/fakesystemd.py:306` | `def _get_unit_path(self, name)` |
| `_notify_callback` | method | `fakesystemD/fakesystemd.py:658` | `def _notify_callback(self, message)` |
| `_parse_config` | method | `fakesystemD/fakesystemd.py:128` | `def _parse_config(self, data)` |
| `_run` | method | `fakesystemD/fakesystemd.py:604` | `def _run(self)` |
| `_signal_handler` | method | `fakesystemD/fakesystemd.py:684` | `def _signal_handler(self, sig, frame)` |
| `load` | method | `fakesystemD/fakesystemd.py:85` | `def load(self)` |
| `log_journal` | method | `fakesystemD/fakesystemd.py:634` | `def log_journal(message, journal_path)` |
| `run_tests` | method | `fakesystemD/fakesystemd.py:698` | `def run_tests()` |
| `start` | method | `fakesystemD/fakesystemd.py:578` | `def start(self)` |
| `start` | method | `fakesystemD/fakesystemd.py:662` | `def start(self)` |
| `stop` | method | `fakesystemD/fakesystemd.py:625` | `def stop(self)` |
| `stop` | method | `fakesystemD/fakesystemd.py:691` | `def stop(self)` |
