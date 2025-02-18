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
7. [License](#license)

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

## Usage

1. **Update the script with your credentials**

   `sftp-parallel.py`:
    ```python
    if __name__ == "__main__":
        HOST = "YOUR_HOST_ADDRESS"             
        USERNAME = "YOUR_USERNAME"             
        KEY_FILE = "/path/to/your/private/key" 
        PORT = 22                              
    
        REMOTE_BASE_PATH = "/path/to/remote/base"
        LOCAL_BASE_PATH = "/path/to/local/base"
    
        MAX_RETRIES = 5    
        MAX_WORKERS = 4    
        TIMEOUT = 30       
    
        copy_subfolders_in_parallel(
            host=HOST,
            username=USERNAME,
            key_filename=KEY_FILE,
            remote_base_path=REMOTE_BASE_PATH,
            local_base_path=LOCAL_BASE_PATH,
            subfolders=SUBFOLDERS,
            port=PORT,
            max_retries=MAX_RETRIES,
            max_workers=MAX_WORKERS,
            timeout=TIMEOUT
        )
    ```

2. **Create the list file**

   `list.py`:
    ```python
    SUBFOLDERS = ["folder1",
    "folder2",
    "folder3"]
    ```


2. **Run the script**


    ```bash
    python3 sftp-parallel.py
    ```

## Configuration

- **Concurrent Threads (max_workers)**:
  - Increase or decrease to optimize the download process based on your system resources and network bandwidth. 
  - Too high a value may overwhelm the server or your local system.

- **Retries (max_retries)**:
  - Adjust to allow multiple attempts in case of intermittent network failures or server timeouts.

- **Timeout**:
  - Each channel has a set timeout during SFTP operations. If the remote server is slow, you might need to increase it.

- **SSH Key File**:
  - Paramiko requires a private key file (e.g., `id_rsa`). Ensure correct file permissions and that your user has the necessary SSH access privileges.


## Logging and Output

- A log file named `copy_subfolders_log.txt` (or similar) is created/appended each time the script runs.
- It records two types of events:
  - `[SUCCESS] Copied <subfolder>`
  - `[FAILURE] Could not copy <subfolder> (Attempt x/y)`

- **Progress Bar**:
  - The script uses `tqdm` to provide a real-time progress bar in the console, indicating how many subfolders have been processed.


## License

This project is licensed under the terms of the **MIT License**. See [LICENSE](LICENSE) for details, or choose another license as appropriate for your needs.

---

**Thank you for using the SFTP Recursive Copy Utility!** If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.


