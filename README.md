# SFTP Recursive Copy Utility

This repository provides a Python script to recursively copy a list of remote subfolders from an SFTP server to a local directory in parallel. It uses:

- **Paramiko** for establishing an SFTP connection and handling file transfers,
- **concurrent.futures** for parallel operations,
- **tqdm** for a progress bar,
- and a user-provided list of remote subfolders to download.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Logging and Output](#logging-and-output)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)

---

## Features

- **Parallel folder copying**: Uses Python's `ThreadPoolExecutor` to download multiple subfolders concurrently.
- **Recursive SFTP**: Automatically traverses directory structures on the remote server.
- **Configurable retries**: Retries any failed folder copy operations up to a specified maximum number of attempts.
- **Timeout handling**: Each file transfer can be given a timeout to prevent hanging processes.
- **Progress monitoring**: Provides a command-line progress bar using `tqdm`.
- **Logging**: Writes success and failure messages to a log file for auditing.

---

## Requirements

- **Python 3.6+** (Recommended; tested on 3.8+)
- **Paramiko** for SSH/SFTP operations
- **tqdm** for progress indication
- **concurrent.futures** (part of the Python standard library)

You can install the required packages using:
```bash
pip install -r requirements.txt
```

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/sftp-copy-utility.git
    cd sftp-copy-utility
    ```

2. **Optional: Create a venv**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # or
    venv\Scripts\activate     # Windows
    ```
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
