# AegisTrap

AegisTrap is an adaptive SSH honeypot designed for security researchers and organizations to monitor, log, and analyze unauthorized access attempts in real time.

## Architecture

AegisTrap uses a modular architecture:

- core/server.py → SSH emulation engine
- core/logger.py → structured logging system
- db/database.py → persistent storage layer
- main.py → execution entry point

## Features

- Credential harvesting
- Command emulation
- Session tracking
- SQLite logging backend
- Multi-threaded connection handling

## Usage

```bash
python main.py
```
Data Collected
Source IP
Username and password attempts
Executed commands
Timestamp
Use Cases
Red Team labs
SOC simulation
Threat intelligence collection
Disclaimer

This tool is intended for authorized environments only.
