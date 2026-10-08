# API

## fakesystemD/fakesystemd.py

### log_journal (method) `def log_journal(message, journal_path)`
- Defined: `fakesystemD/fakesystemd.py:634`

### run_tests (method) `def run_tests()`
- Defined: `fakesystemD/fakesystemd.py:698`

### __init__ (method) `def __init__(self, config_path)`
- Defined: `fakesystemD/fakesystemd.py:72`

### load (method) `def load(self)`
- Defined: `fakesystemD/fakesystemd.py:85`

### _create_default_config (method) `def _create_default_config(self)`
- Defined: `fakesystemD/fakesystemd.py:96`

### _parse_config (method) `def _parse_config(self, data)`
- Defined: `fakesystemD/fakesystemd.py:128`

### __init__ (method) `def __init__(self, bus, object_path, config, manager)`
- Defined: `fakesystemD/fakesystemd.py:158`

### Get (method) `def Get(self, interface_name, property_name)`
- Defined: `fakesystemD/fakesystemd.py:166`

### Set (method) `def Set(self, interface_name, property_name, value)`
- Defined: `fakesystemD/fakesystemd.py:196`

### GetAll (method) `def GetAll(self, interface_name)`
- Defined: `fakesystemD/fakesystemd.py:202`

### GetUnitFileState (method) `def GetUnitFileState(self)`
- Defined: `fakesystemD/fakesystemd.py:223`

### Describe (method) `def Describe(self)`
- Defined: `fakesystemD/fakesystemd.py:228`

### UnitFileState (method) `def UnitFileState(self)`
- Defined: `fakesystemD/fakesystemd.py:233`

### Reload (method) `def Reload(self, mode)`
- Defined: `fakesystemD/fakesystemd.py:238`

### Freeze (method) `def Freeze(self, mode)`
- Defined: `fakesystemD/fakesystemd.py:244`

### Thaw (method) `def Thaw(self)`
- Defined: `fakesystemD/fakesystemd.py:250`

### __init__ (method) `def __init__(self, bus, object_path, job_config, manager)`
- Defined: `fakesystemD/fakesystemd.py:256`

### Get (method) `def Get(self)`
- Defined: `fakesystemD/fakesystemd.py:263`

### __init__ (method) `def __init__(self, bus, object_path, config)`
- Defined: `fakesystemD/fakesystemd.py:269`

### _emit_unit_changed (method) `def _emit_unit_changed(self, name)`
- Defined: `fakesystemD/fakesystemd.py:279`

### _create_units (method) `def _create_units(self)`
- Defined: `fakesystemD/fakesystemd.py:282`

### _get_or_create_unit (method) `def _get_or_create_unit(self, name)`
- Defined: `fakesystemD/fakesystemd.py:288`

### _get_unit_path (method) `def _get_unit_path(self, name)`
- Defined: `fakesystemD/fakesystemd.py:306`

### _create_job (method) `def _create_job(self, unit_name, job_type)`
- Defined: `fakesystemD/fakesystemd.py:309`

### Get (method) `def Get(self, interface_name, property_name)`
- Defined: `fakesystemD/fakesystemd.py:321`

### Set (method) `def Set(self, interface_name, property_name, value)`
- Defined: `fakesystemD/fakesystemd.py:341`

### GetAll (method) `def GetAll(self, interface_name)`
- Defined: `fakesystemD/fakesystemd.py:346`

### GetVersion (method) `def GetVersion(self)`
- Defined: `fakesystemD/fakesystemd.py:362`

### GetFeatures (method) `def GetFeatures(self)`
- Defined: `fakesystemD/fakesystemd.py:367`

### GetVirtualization (method) `def GetVirtualization(self)`
- Defined: `fakesystemD/fakesystemd.py:372`

### GetArchitecture (method) `def GetArchitecture(self)`
- Defined: `fakesystemD/fakesystemd.py:377`

### GetEnvironment (method) `def GetEnvironment(self)`
- Defined: `fakesystemD/fakesystemd.py:382`

### StartUnit (method) `def StartUnit(self, name, mode)`
- Defined: `fakesystemD/fakesystemd.py:387`

### StopUnit (method) `def StopUnit(self, name, mode)`
- Defined: `fakesystemD/fakesystemd.py:396`

### RestartUnit (method) `def RestartUnit(self, name, mode)`
- Defined: `fakesystemD/fakesystemd.py:405`

### GetUnit (method) `def GetUnit(self, name)`
- Defined: `fakesystemD/fakesystemd.py:414`

### GetUnitByPID (method) `def GetUnitByPID(self, pid)`
- Defined: `fakesystemD/fakesystemd.py:420`

### ListUnits (method) `def ListUnits(self)`
- Defined: `fakesystemD/fakesystemd.py:430`

### ListUnitsFiltered (method) `def ListUnitsFiltered(self, states)`
- Defined: `fakesystemD/fakesystemd.py:448`

### GetUnitFileState (method) `def GetUnitFileState(self, name)`
- Defined: `fakesystemD/fakesystemd.py:453`

### ListUnitFiles (method) `def ListUnitFiles(self)`
- Defined: `fakesystemD/fakesystemd.py:458`

### EnableUnitFiles (method) `def EnableUnitFiles(self, files, runtime, force)`
- Defined: `fakesystemD/fakesystemd.py:463`

### DisableUnitFiles (method) `def DisableUnitFiles(self, files, runtime)`
- Defined: `fakesystemD/fakesystemd.py:471`

### Reload (method) `def Reload(self, mode)`
- Defined: `fakesystemD/fakesystemd.py:480`

### Reexecute (method) `def Reexecute(self)`
- Defined: `fakesystemD/fakesystemd.py:485`

### KillUnit (method) `def KillUnit(self, name, signal)`
- Defined: `fakesystemD/fakesystemd.py:490`

### ResetFailedUnit (method) `def ResetFailedUnit(self, name)`
- Defined: `fakesystemD/fakesystemd.py:496`

### ListJobs (method) `def ListJobs(self)`
- Defined: `fakesystemD/fakesystemd.py:502`

### GetJob (method) `def GetJob(self, job_id)`
- Defined: `fakesystemD/fakesystemd.py:511`

### GetUnitFileInfo (method) `def GetUnitFileInfo(self)`
- Defined: `fakesystemD/fakesystemd.py:518`

### GetUnitFileInfoByName (method) `def GetUnitFileInfoByName(self, name)`
- Defined: `fakesystemD/fakesystemd.py:526`

### SetUnitProperties (method) `def SetUnitProperties(self, name, runtime, properties)`
- Defined: `fakesystemD/fakesystemd.py:533`

### GetUnitProcesses (method) `def GetUnitProcesses(self, name)`
- Defined: `fakesystemD/fakesystemd.py:538`

### __init__ (method) `def __init__(self, config, callback)`
- Defined: `fakesystemD/fakesystemd.py:547`

### _find_usable_socket_path (method) `def _find_usable_socket_path(self)`
- Defined: `fakesystemD/fakesystemd.py:555`

### start (method) `def start(self)`
- Defined: `fakesystemD/fakesystemd.py:578`

### _run (method) `def _run(self)`
- Defined: `fakesystemD/fakesystemd.py:604`

### stop (method) `def stop(self)`
- Defined: `fakesystemD/fakesystemd.py:625`

### __init__ (method) `def __init__(self, config_path)`
- Defined: `fakesystemD/fakesystemd.py:650`

### _notify_callback (method) `def _notify_callback(self, message)`
- Defined: `fakesystemD/fakesystemd.py:658`

### start (method) `def start(self)`
- Defined: `fakesystemD/fakesystemd.py:662`

### _signal_handler (method) `def _signal_handler(self, sig, frame)`
- Defined: `fakesystemD/fakesystemd.py:684`

### stop (method) `def stop(self)`
- Defined: `fakesystemD/fakesystemd.py:691`
