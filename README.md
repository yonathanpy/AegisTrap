# AegisTrap

AegisTrap is a modular SSH honeypot that operates by intercepting and emulating SSH sessions at the transport layer, capturing authentication attempts and interactive command input while maintaining a controlled execution environment.

---
## Execution Flow

```text
Incoming connection hits port 2222
→ accepted by the listening socket

socket.accept()
→ returns (client, address)

client socket passed into Paramiko Transport
→ SSH handshake starts
→ host key presented

authentication phase
→ username/password received
→ values stored (no validation)

channel request
→ session channel opened

transport.accept()
→ interactive channel ready

loop starts
→ chan.recv()
→ raw input read from client
→ input cleaned and parsed

command handler
→ compared against known commands
→ static response generated

logger call
→ (ip, username, password, command, timestamp)

database write
→ INSERT into SQLite

loop continues until disconnect
→ channel closed
→ session ends
```

---

## Core Runtime Behavior

### 1. Socket Binding

```python
sock = socket.socket()
sock.bind(("0.0.0.0", 2222))
sock.listen(100)
```

* Opens a TCP listener on all interfaces
* Accepts inbound SSH connections
* Queues up to 100 concurrent connection attempts

---

### 2. SSH Transport Initialization

```python
transport = paramiko.Transport(client)
transport.add_server_key(HOST_KEY)
transport.start_server(server=server)
```

* Wraps raw TCP socket with SSH protocol handler
* Injects generated RSA host key
* Initiates SSH handshake sequence

---

### 3. Authentication Interception

```python
def check_auth_password(self, username, password):
    self.username = username
    self.password = password
    return paramiko.AUTH_SUCCESSFUL
```

* Captures credentials before validation
* Accepts all login attempts (no rejection path)
* Enables full session continuation for interaction logging

---

### 4. Channel Establishment

```python
chan = transport.accept(10)
```

* Allocates interactive session channel
* Timeout-based acceptance (10 seconds)
* Required for shell emulation

---

### 5. Interactive Command Loop

```python
cmd = chan.recv(1024).decode().strip()
```

* Reads attacker input from SSH channel
* Buffers up to 1024 bytes per read
* Normalizes command string for processing

---

### 6. Command Emulation Engine

```python
def emulate_command(cmd):
    if cmd == "whoami":
        return "root\n"
    elif cmd == "uname -a":
        return "Linux aegis 5.15.0 x86_64\n"
    elif cmd.startswith("ls"):
        return "bin etc home var\n"
    return "command not found\n"
```

* Pattern-based command matching
* Returns static or simulated outputs
* Prevents execution on host system

---

### 7. Logging Pipeline

```python
logger.log(ip, username, password, cmd)
```

```python
self.db.insert(ip, username, password, command, timestamp)
```

* Captures session metadata
* Persists to SQLite backend
* Ensures chronological traceability

---

## Data Model

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    username TEXT,
    password TEXT,
    command TEXT,
    timestamp TEXT
);
```

---

## Threading Model

```python
threading.Thread(target=self.handle, args=(client, addr)).start()
```

* Each connection handled in isolated thread
* Enables concurrent attacker sessions
* Avoids blocking on I/O operations

---

## Security Model

* No real command execution
* No system shell access
* Full isolation at application layer
* Controlled response generation

---

## Network Behavior Summary

```text
[CONNECT] → TCP ACCEPT
        → SSH HANDSHAKE
        → AUTH CAPTURE
        → SESSION OPEN
        → COMMAND LOOP
        → LOG WRITE
        → SESSION CLOSE
```

---

## Extensibility Points

### Command Engine Hook

```python
def emulate_command(cmd):
    # extend with regex / behavior modeling
```

### Logging Extension

```python
logger.log(...)
# forward to external SIEM or file stream
```

### Detection Layer

```python
if "wget" in cmd or "curl" in cmd:
    flag_high_risk(ip)
```

---

## Deployment Context

* Isolated lab environments
* Controlled exposure networks
* Sandboxed research systems

---

## Disclaimer

This system is designed strictly for authorized security testing and controlled research environments. Unauthorized deployment is not permitted.
