# API

## fakesystemD/fakesystemd.py

### log_journal `def log_journal(message, journal_path)`
- Defined: `fakesystemD/fakesystemd.py:634`

### run_tests `def run_tests()`
- Defined: `fakesystemD/fakesystemd.py:698`

### __init__ `def __init__(self, config_path)`
- Defined: `fakesystemD/fakesystemd.py:72`

### load `def load(self)`
- Defined: `fakesystemD/fakesystemd.py:85`

### _create_default_config `def _create_default_config(self)`
- Defined: `fakesystemD/fakesystemd.py:96`

### _parse_config `def _parse_config(self, data)`
- Defined: `fakesystemD/fakesystemd.py:128`

### __init__ `def __init__(self, bus, object_path, config, manager)`
- Defined: `fakesystemD/fakesystemd.py:158`

### Get `def Get(self, interface_name, property_name)`
- Defined: `fakesystemD/fakesystemd.py:166`

### Set `def Set(self, interface_name, property_name, value)`
- Defined: `fakesystemD/fakesystemd.py:196`

### GetAll `def GetAll(self, interface_name)`
- Defined: `fakesystemD/fakesystemd.py:202`

### GetUnitFileState `def GetUnitFileState(self)`
- Defined: `fakesystemD/fakesystemd.py:223`

### Describe `def Describe(self)`
- Defined: `fakesystemD/fakesystemd.py:228`

### UnitFileState `def UnitFileState(self)`
- Defined: `fakesystemD/fakesystemd.py:233`

### Reload `def Reload(self, mode)`
- Defined: `fakesystemD/fakesystemd.py:238`

### Freeze `def Freeze(self, mode)`
- Defined: `fakesystemD/fakesystemd.py:244`

### Thaw `def Thaw(self)`
- Defined: `fakesystemD/fakesystemd.py:250`

### __init__ `def __init__(self, bus, object_path, job_config, manager)`
- Defined: `fakesystemD/fakesystemd.py:256`

### Get `def Get(self)`
- Defined: `fakesystemD/fakesystemd.py:263`

### __init__ `def __init__(self, bus, object_path, config)`
- Defined: `fakesystemD/fakesystemd.py:269`

### _emit_unit_changed `def _emit_unit_changed(self, name)`
- Defined: `fakesystemD/fakesystemd.py:279`

### _create_units `def _create_units(self)`
- Defined: `fakesystemD/fakesystemd.py:282`

### _get_or_create_unit `def _get_or_create_unit(self, name)`
- Defined: `fakesystemD/fakesystemd.py:288`

### _get_unit_path `def _get_unit_path(self, name)`
- Defined: `fakesystemD/fakesystemd.py:306`

### _create_job `def _create_job(self, unit_name, job_type)`
- Defined: `fakesystemD/fakesystemd.py:309`

### Get `def Get(self, interface_name, property_name)`
- Defined: `fakesystemD/fakesystemd.py:321`

### Set `def Set(self, interface_name, property_name, value)`
- Defined: `fakesystemD/fakesystemd.py:341`

### GetAll `def GetAll(self, interface_name)`
- Defined: `fakesystemD/fakesystemd.py:346`

### GetVersion `def GetVersion(self)`
- Defined: `fakesystemD/fakesystemd.py:362`

### GetFeatures `def GetFeatures(self)`
- Defined: `fakesystemD/fakesystemd.py:367`

### GetVirtualization `def GetVirtualization(self)`
- Defined: `fakesystemD/fakesystemd.py:372`

### GetArchitecture `def GetArchitecture(self)`
- Defined: `fakesystemD/fakesystemd.py:377`

### GetEnvironment `def GetEnvironment(self)`
- Defined: `fakesystemD/fakesystemd.py:382`

### StartUnit `def StartUnit(self, name, mode)`
- Defined: `fakesystemD/fakesystemd.py:387`

### StopUnit `def StopUnit(self, name, mode)`
- Defined: `fakesystemD/fakesystemd.py:396`

### RestartUnit `def RestartUnit(self, name, mode)`
- Defined: `fakesystemD/fakesystemd.py:405`

### GetUnit `def GetUnit(self, name)`
- Defined: `fakesystemD/fakesystemd.py:414`

### GetUnitByPID `def GetUnitByPID(self, pid)`
- Defined: `fakesystemD/fakesystemd.py:420`

### ListUnits `def ListUnits(self)`
- Defined: `fakesystemD/fakesystemd.py:430`

### ListUnitsFiltered `def ListUnitsFiltered(self, states)`
- Defined: `fakesystemD/fakesystemd.py:448`

### GetUnitFileState `def GetUnitFileState(self, name)`
- Defined: `fakesystemD/fakesystemd.py:453`

### ListUnitFiles `def ListUnitFiles(self)`
- Defined: `fakesystemD/fakesystemd.py:458`

### EnableUnitFiles `def EnableUnitFiles(self, files, runtime, force)`
- Defined: `fakesystemD/fakesystemd.py:463`

### DisableUnitFiles `def DisableUnitFiles(self, files, runtime)`
- Defined: `fakesystemD/fakesystemd.py:471`

### Reload `def Reload(self, mode)`
- Defined: `fakesystemD/fakesystemd.py:480`

### Reexecute `def Reexecute(self)`
- Defined: `fakesystemD/fakesystemd.py:485`

### KillUnit `def KillUnit(self, name, signal)`
- Defined: `fakesystemD/fakesystemd.py:490`

### ResetFailedUnit `def ResetFailedUnit(self, name)`
- Defined: `fakesystemD/fakesystemd.py:496`

### ListJobs `def ListJobs(self)`
- Defined: `fakesystemD/fakesystemd.py:502`

### GetJob `def GetJob(self, job_id)`
- Defined: `fakesystemD/fakesystemd.py:511`

### GetUnitFileInfo `def GetUnitFileInfo(self)`
- Defined: `fakesystemD/fakesystemd.py:518`

### GetUnitFileInfoByName `def GetUnitFileInfoByName(self, name)`
- Defined: `fakesystemD/fakesystemd.py:526`

### SetUnitProperties `def SetUnitProperties(self, name, runtime, properties)`
- Defined: `fakesystemD/fakesystemd.py:533`

### GetUnitProcesses `def GetUnitProcesses(self, name)`
- Defined: `fakesystemD/fakesystemd.py:538`

### __init__ `def __init__(self, config, callback)`
- Defined: `fakesystemD/fakesystemd.py:547`

### _find_usable_socket_path `def _find_usable_socket_path(self)`
- Defined: `fakesystemD/fakesystemd.py:555`

### start `def start(self)`
- Defined: `fakesystemD/fakesystemd.py:578`

### _run `def _run(self)`
- Defined: `fakesystemD/fakesystemd.py:604`

### stop `def stop(self)`
- Defined: `fakesystemD/fakesystemd.py:625`

### __init__ `def __init__(self, config_path)`
- Defined: `fakesystemD/fakesystemd.py:650`

### _notify_callback `def _notify_callback(self, message)`
- Defined: `fakesystemD/fakesystemd.py:658`

### start `def start(self)`
- Defined: `fakesystemD/fakesystemd.py:662`

### _signal_handler `def _signal_handler(self, sig, frame)`
- Defined: `fakesystemD/fakesystemd.py:684`

### stop `def stop(self)`
- Defined: `fakesystemD/fakesystemd.py:691`
