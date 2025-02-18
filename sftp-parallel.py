import os
import paramiko
import stat
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Import the list of subfolders from a separate file
# (Ensure 'list_usprp.py' has the variable SUBFOLDERS defined)
from list_usprp import SUBFOLDERS

def sftp_copy_folder(
    host,
    username,
    key_filename,
    remote_folder,
    local_folder,
    port=22,
    timeout=30
):
    """
    Recursively copy the contents of `remote_folder` from an SFTP server
    to the local filesystem at `local_folder`. Returns True if successful,
    False otherwise.
    """
    try:
        # Load private key
        private_key = paramiko.RSAKey.from_private_key_file(key_filename)

        # Create and connect transport
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, pkey=private_key)

        # Create SFTP client
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get_channel().settimeout(timeout)

        # Make local_folder if it doesn't exist
        if not os.path.exists(local_folder):
            os.makedirs(local_folder, exist_ok=True)

        def _recursive_sftp_copy(remote_path, local_path):
            """
            Recursively copies a directory from the remote server to the local machine.
            """
            if not os.path.exists(local_path):
                os.makedirs(local_path, exist_ok=True)

            for item in sftp.listdir_attr(remote_path):
                remote_item_path = os.path.join(remote_path, item.filename)
                local_item_path = os.path.join(local_path, item.filename)

                mode = item.st_mode
                # Check if the item is a directory; if so, recurse
                if stat.S_ISDIR(mode):
                    _recursive_sftp_copy(remote_item_path, local_item_path)
                else:
                    # Otherwise, copy the file
                    sftp.get(remote_item_path, local_item_path)

        # Perform the recursive copy
        _recursive_sftp_copy(remote_folder, local_folder)

        # Close connections
        sftp.close()
        transport.close()

        return True
    except Exception:
        traceback.print_exc()
        return False


def copy_subfolders_in_parallel(
    host,
    username,
    key_filename,
    remote_base_path,
    local_base_path,
    subfolders,
    port=22,
    max_retries=5,
    max_workers=4,
    timeout=30
):
    """
    Copy each subfolder in `subfolders` from `remote_base_path` to
    `local_base_path` in parallel. Retries failed copies up to `max_retries`.
    """

    # Track the number of attempts and successful copies
    attempts = {sf: 0 for sf in subfolders}
    successful = set()

    # Log file to track successes/failures
    log_filename = "copy_subfolders_log_usprp.txt"

    with tqdm(total=len(subfolders), desc="Copying subfolders") as pbar, \
         open(log_filename, "a") as log_file:

        # Keep trying until all are successful or max_retries is reached
        while len(successful) < len(subfolders):
            # Subfolders that still need to be tried
            to_try = [
                sf for sf in subfolders
                if sf not in successful and attempts[sf] < max_retries
            ]
            if not to_try:
                # No subfolders left to try, but not all were successful
                break

            futures = {}
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for sf in to_try:
                    attempts[sf] += 1
                    remote_folder = os.path.join(remote_base_path, sf)
                    local_folder = os.path.join(local_base_path, sf)

                    future = executor.submit(
                        sftp_copy_folder,
                        host,
                        username,
                        key_filename,
                        remote_folder,
                        local_folder,
                        port,
                        timeout
                    )
                    futures[future] = sf

                # Process the results as they complete
                for future in as_completed(futures):
                    sf = futures[future]
                    success = future.result()

                    # Update progress bar
                    pbar.update(1)

                    # Log results
                    if success:
                        log_file.write(f"[SUCCESS] Copied {sf}\n")
                        successful.add(sf)
                    else:
                        log_file.write(
                            f"[FAILURE] Could not copy {sf} "
                            f"(Attempt {attempts[sf]}/{max_retries})\n"
                        )

                    # Optional flush for immediate log writes
                    log_file.flush()

    # Check final status of all subfolders
    not_copied = [sf for sf in subfolders if sf not in successful]
    if not_copied:
        print("Some subfolders could not be copied after max retries:", not_copied)
    else:
        print("All subfolders copied successfully!")


if __name__ == "__main__":
    # ------------------------------------------------------------------------
    # Below variables have been replaced with placeholders.
    # Replace them with the actual values for your setup.
    # ------------------------------------------------------------------------
    HOST = "YOUR_HOST_ADDRESS"             # e.g., "example.com"
    USERNAME = "YOUR_USERNAME"             # e.g., "myuser"
    KEY_FILE = "/path/to/your/private/key" # e.g., "/home/user/.ssh/id_rsa"
    PORT = 22                              # Default SSH port; adjust if needed

    REMOTE_BASE_PATH = "/path/to/remote/base"
    LOCAL_BASE_PATH = "/path/to/local/base"

    MAX_RETRIES = 100   # Adjust based on your connection reliability
    MAX_WORKERS = 9   # Adjust for parallelism (depends on system resources)
    TIMEOUT = 30      # SFTP operation timeout in seconds

    # Initiate the parallel copy
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
