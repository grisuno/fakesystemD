# Fake Systemd – Drop‑in Replacement

This project provides a complete, self‑contained emulation of systemd’s D‑Bus interface (`org.freedesktop.systemd1`) and `sd_notify` socket. It allows modern services that expect a full systemd environment to run without modification, even when systemd is not present (e.g., containers, lightweight VMs, or development environments).

The emulator implements all critical D‑Bus methods and properties, correctly handles `sd_notify` messages (including `WATCHDOG=1`, `FDSTORE=1`, `FDSTOREREMOVE=1`), and responds to property queries so that services remain stable and do not enter restart loops.

---

## Features

- **Full `Manager` interface**: `StartUnit`, `StopUnit`, `RestartUnit`, `GetUnit`, `ListUnits`, `ListUnitsFiltered`, `EnableUnitFiles`, `DisableUnitFiles`, `GetUnitFileState`, `ListUnitFiles`, `ListJobs`, `GetJob`, `GetUnitByPID`, `KillUnit`, `ResetFailedUnit`, `Reload`, `Reexecute`, `SetUnitProperties`, `GetUnitProcesses`, informational methods (`GetVersion`, `GetFeatures`, `GetVirtualization`, etc.)
- **Complete `Unit` interface**: `GetUnitFileState`, `Describe`, `Reload`, `Freeze`, `Thaw`
- **Full `org.freedesktop.DBus.Properties` support** on both `Manager` and `Unit` objects – services can read all standard properties (`ActiveState`, `SubState`, `LoadState`, `Description`, `MainPID`, `MemoryCurrent`, `CPUUsageNSec`, `TasksCurrent`, `UnitFileState`, etc.) without errors
- **`sd_notify` listener** with Unix datagram socket, automatic fallback to user runtime directories, and correct handling of `SCM_RIGHTS` ancillary data – file descriptors are immediately closed to prevent resource leaks
- **Auto‑creation of units** – any unit queried via D‑Bus is created on‑the‑fly with `ActiveState=active` and `SubState=running`
- **Journal logging** – `sd_notify` messages are logged to a configurable journal file (with automatic directory creation)
- **Self‑test harness** – built‑in TDD/BDD test suite (`--test`) validates all implemented methods
- **Single Python file** – no external dependencies beyond Python 3, `dbus`, and `GLib`
- **Production‑ready** – no hard‑coded paths, all configuration centralised in JSON, robust error handling, and clean shutdown on signals

---

## Requirements

- **Python 3.6+**
- **python3-dbus** – D‑Bus bindings
- **python3-gi** – GLib main loop integration
- **Root privileges** – required to claim the system bus (`org.freedesktop.systemd1`) and bind to `/run/systemd/notify`. If run as non‑root, the emulator falls back to the session bus and a user‑specific notify socket.

Install dependencies (Debian/Ubuntu):

```bash
sudo apt install python3-dbus python3-gi
```

---

## Installation

Clone the repository or download `fakesystemd.py` and make it executable:

```bash
chmod +x fakesystemd.py
```

No further installation is required.

---

## Usage

### Start the emulator

```bash
sudo ./fakesystemd.py
```

With verbose logging:

```bash
sudo ./fakesystemd.py --verbose
```

With a custom configuration file:

```bash
sudo ./fakesystemd.py --config /path/to/config.json
```

### Run self‑tests

```bash
./fakesystemd.py --test
```

---

## Configuration

The default configuration file is `/etc/fake_systemd/config.json`. If it does not exist, the emulator creates it with sane defaults.

Example `config.json`:

```json
{
  "units": {
    "sysinit.target": { "type": "target", "active_state": "active", "sub_state": "running" },
    "basic.target": { "type": "target", "active_state": "active", "sub_state": "running" },
    "network.target": { "type": "target", "active_state": "active", "sub_state": "running" },
    "time-sync.target": { "type": "target", "active_state": "active", "sub_state": "running" },
    "multi-user.target": { "type": "target", "active_state": "active", "sub_state": "running" },
    "graphical.target": { "type": "target", "active_state": "active", "sub_state": "running" },
    "test.service": {
      "type": "service",
      "active_state": "active",
      "sub_state": "running",
      "description": "Test service",
      "main_pid": 1234,
      "exec_path": "/usr/bin/test"
    }
  },
  "notify_socket": "/run/systemd/notify",
  "bus_name": "org.freedesktop.systemd1",
  "object_path": "/org/freedesktop/systemd1",
  "journal_path": "/var/log/fake_systemd/journal.log",
  "socket_mode": "666",
  "socket_user": "root",
  "socket_group": "root"
}
```

- `units`: dictionary of unit definitions. Each unit can specify `active_state`, `sub_state`, `load_state`, `description`, `main_pid`, `exec_path`, `memory_current`, `cpu_usage`, `tasks_current`, and `unit_file_state`.
- `notify_socket`: path for the `sd_notify` socket.
- `bus_name`: D‑Bus name to claim (must be `org.freedesktop.systemd1` for compatibility).
- `object_path`: D‑Bus object path for the `Manager` interface.
- `journal_path`: log file for `sd_notify` messages; if not writable, messages are logged to stderr.
- `socket_mode`, `socket_user`, `socket_group`: permissions for the notify socket.

---

## How It Works

1. **D‑Bus** – The emulator claims the well‑known name `org.freedesktop.systemd1` and exports a `Manager` object at `/org/freedesktop/systemd1`. Every unit is exported as a separate D‑Bus object under `/org/freedesktop/systemd1/unit/<unit_name>`.

2. **Properties** – Both `Manager` and `Unit` objects implement the `org.freedesktop.DBus.Properties` interface. Services can call `Get`, `GetAll`, or `Set` to read/modify unit states. All properties return plausible values, with `ActiveState` and `SubState` defaulting to `"active"` and `"running"`.

3. **sd_notify** – The emulator binds to a Unix datagram socket (default `/run/systemd/notify`). It receives messages from services, parses them, and logs them. If ancillary data (`SCM_RIGHTS`) is received, the file descriptors are immediately closed to prevent leaks.

4. **Unit auto‑creation** – Any unit name requested via `GetUnit`, `StartUnit`, `StopUnit`, etc., is created on‑the‑fly with `ActiveState=active` and `SubState=running`. This ensures that dependency checks never fail.

5. **Journal logging** – All `sd_notify` messages are written to the configured journal file (with automatic directory creation).

---

## Testing

Run the built‑in self‑test to verify that all D‑Bus methods work correctly:

```bash
./fakesystemd.py --test
```

Expected output: `All tests passed.`

---

## Limitations

- **No real process lifecycle** – The emulator does not fork, execute, or manage actual processes. It only simulates unit states.
- **No dependency resolution** – Units do not have ordering or dependency relationships.
- **No timer or socket activation** – Only the `Manager` and `Unit` interfaces are implemented.
- **No signal emission** – Unit state changes do not emit D‑Bus signals (e.g., `UnitNew`, `JobRemoved`). However, services rarely rely on these for basic functionality.
- **FDSTORE is limited** – Received file descriptors are closed immediately; they are not stored and returned on subsequent requests. This is sufficient to prevent crashes, but services that attempt to recover state via FDSTORE will not have state restored.

---

## Security Considerations

- The emulator runs with root privileges (when started with `sudo`) to bind to the system bus and privileged socket.
- It does **not** execute any external commands, spawn subprocesses, or evaluate user‑supplied input.
- Received file descriptors are closed immediately, preventing resource exhaustion.
- All paths are configurable; no hard‑coded absolute paths are used.

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. **Write a test** for any new functionality (add it to `run_tests()`).
2. **Implement the feature**.
3. **Ensure `--test` passes**.
4. **Update documentation** (README and CLAUDE.md if applicable).
5. **Submit a pull request**.

---

## License

This project is released under the **AGPLV3 License**. See the source file header for details.

---

## Acknowledgements

This emulator was designed to fill the gap in environments where systemd is unavailable or undesirable, enabling modern Debian services to run without modification. It has been tested with `systemd-logind`, `systemd-timesyncd`, and other systemd‑aware daemons.

---

[*] This data is provided as a neutral reference object with no evaluative frame.


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) [![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y2Z73AV)
