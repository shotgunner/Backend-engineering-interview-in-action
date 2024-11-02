#!/usr/bin/env python3
"""
Demonstration of Linux namespace isolation similar to Docker's approach
Requires root privileges to run
"""

import os
import sys
import subprocess
from pathlib import Path
import ctypes.util
import shutil

def create_container():
    """Creates an isolated environment using Linux namespaces"""
    
    # Need to run as root
    if os.geteuid() != 0:
        print("This script requires root privileges")
        sys.exit(1)

    # Load libc for namespace constants
    libc = ctypes.CDLL(ctypes.util.find_library('c'))
    
    # Define namespace constants if not available in os module
    CLONE_NEWPID = 0x20000000
    CLONE_NEWUTS = 0x04000000
    CLONE_NEWNS = 0x00020000
    CLONE_NEWNET = 0x40000000

    # Create new namespaces
    flags = (
        CLONE_NEWPID |  # New PID namespace
        CLONE_NEWUTS |  # New UTS namespace (hostname)
        CLONE_NEWNS  |  # New mount namespace
        CLONE_NEWNET   # New network namespace
    )

    # Fork the process
    pid = os.fork()

    if pid == 0:  # Child process
        # Set up the container environment
        libc.sethostname(b'container', len(b'container'))  # Set container hostname using libc
        
        # Create a new root filesystem
        new_root = Path('/private/tmp/container_root')
        new_root.mkdir(exist_ok=True)
        
        # Mount proc filesystem
        proc = new_root / 'proc'
        proc.mkdir(exist_ok=True)
        
        # Ensure mount_proc exists and is executable
        mount_proc = Path('/Library/Filesystems/proc.fs/Contents/Resources/mount_proc')
        if not mount_proc.exists():
            print(f"Error: {mount_proc} not found")
            sys.exit(1)
            
        try:
            subprocess.run(['mount', '-t', 'proc', 'proc', str(proc)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to mount proc: {e}")
            sys.exit(1)
        
        # Change root directory
        os.chroot(str(new_root))
        os.chdir('/')
        
        # Execute a shell in the container
        if not Path('/bin/bash').exists():
            print("Error: /bin/bash not found")
            sys.exit(1)
            
        os.execv('/bin/bash', ['/bin/bash'])
    else:
        # Parent process waits for child
        _, status = os.waitpid(pid, 0)
        print(f"Container exited with status {status}")
        
        # Cleanup
        try:
            subprocess.run(['umount', '/private/tmp/container_root/proc'], check=False)
            shutil.rmtree('/private/tmp/container_root')
        except Exception as e:
            print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    create_container()

"""
Alternatively, using unshare command in bash:

#!/bin/bash

# Create new namespaces
sudo unshare --fork --pid --mount-proc --uts --net --mount /bin/bash

# This creates a new process with isolated namespaces:
# --fork: Create a new process
# --pid: New PID namespace
# --mount-proc: Mount a new proc filesystem
# --uts: New UTS namespace (hostname)
# --net: New network namespace
# --mount: New mount namespace

# Inside the new namespace, you can:
hostname container  # Set container hostname
ps aux  # See isolated process list
ip addr  # See isolated network interfaces
"""
