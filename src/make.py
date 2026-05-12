#!/usr/bin/env python3

"""Build script for PERFEC System applicaitons for the Circuit Playground."""

# This processes the files in the same directory as make.py and 
# recursivesly copies any subdirectories (without precompiling).

# Copyright 2026
# Tom Hoffman


import argparse
from pathlib import Path
import subprocess
import shutil
import os

DONT_PRECOMPILE = {"boot.py", "code.py", "config.py", "make.py"}
DONT_UPDATE = {"config.py"}
SKIP = {"make.py"}
PY_EXT = "py"

def is_python_file(filename: str) -> bool:
    return filename.endswith(PY_EXT)

def is_directory(local_path: Path) -> bool:
    return local_path.is_dir()

def local_is_more_recent(local_path: Path, remote_path: Path):
    return (os.path.getmtime(local_path) > os.path.getmtime(remote_path))

def generateRemotePath(root_path: Path, filename: str) -> Path:
    if filename in DONT_PRECOMPILE:
        return root_path / filename
    else:
        return root_path / f"{filename[:-len(PY_EXT)]}m{PY_EXT}" 

def compile_and_copy(local_path: Path, remote_path: Path, mpy_cross_exe: Path, ) -> None:
    """Process a single file with compilation + fallback copy logic."""    
    try:
        # Try compiling first (only if compilation is feasible)
        subprocess.run(
            [str(mpy_cross_exe), str(local_path)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False  # Never crash on compile errors
        )
        shutil.move(str(remote_path.name), str(remote_path))  # Move compiled output to final location
    
    except FileNotFoundError as e:
        # Compilation failed silently or file doesn't exist → fallback copy
        print(f"  ! Compilation failed ({e}), copying directly...")
        shutil.copyfile(str(remote_path.name), str(remote_path))
        print(f"  ✗ Fallback copied: {remote_path}")
    
    except Exception as e:
        # Catch all other errors (e.g., permission issues) → fallback copy
        print(f"  ? Unexpected error ({e}), copying directly...")
        shutil.copyfile(str(remote_path.name), str(remote_path))

def main():
    parser = argparse.ArgumentParser(description="Compile Python files with mpy-cross.")
    parser.add_argument("mpy_cross_path", help="Path to mpy-cross compiler executable.")
    parser.add_argument("remote_root_path", help="Root directory for output files.")
    
    args = parser.parse_args()
    remote_dir = Path(args.remote_root_path)
    mpy_cross_exe = Path(args.mpy_cross_path).resolve()  # Resolve symlinks
    
    if not remote_dir.is_dir():
        raise FileNotFoundError(f"Output root does not exist: {remote_path}")
    if not mpy_cross_exe.is_file():
        raise FileNotFoundError(f"Compiler missing: {mpy_cross_exe}")

    print("Scanning directory...")

    for filename in os.listdir("."):  # Only process files in current dir (not subdirs)
        # generate paths
        d = os.getcwd()
        local_path = Path(filename)
        remote_path = generateRemotePath(remote_dir, filename)
        '''
        cases:
        * isn't a Python file: 
            * is a directory:
                recursively copy
            * else: skip
        * is in SKIP: 
            * skip
        * is in DONT_UPDATE:
            * if it does not exist, send a copy
            * else:
                * if local is newer, print a warning ⚠
                * else: skip
        * is in DONT_PRECOMPILE:
            * if local is newer, send a copy
        * else:
            if local is newer, complile and send a copy
        '''
        if not(is_python_file(filename)):
            if is_directory(local_path):
                try:
                    shutil.copytree(local_path, remote_dir / filename)
                except FileExistsError:
                    pass
                print(f"  ✓ Copied {filename} directory tree.")
            else:
                print(f"    ✗ Not a Python file: {filename}") 
        elif filename in SKIP:
            print(f"    ✗ Skipping: {filename}")
        elif filename in DONT_UPDATE:
            if not(remote_path.exists()):
                shutil.copyfile(str(remote_path.name), str(remote_path))
                print(f"  ✓ Copied: {remote_path.name}")
            else:
                if local_is_more_recent(local_path, remote_path):
                    print(f" ⚠ WARNING: you may need to manually update {filename}")
                else:
                    print(f"    ✗ Remote copy up to date: {remote_path.name}")        
        elif filename in DONT_PRECOMPILE:
            if remote_path.exists():
                if local_is_more_recent(local_path, remote_path):
                    shutil.copyfile(str(remote_path.name), str(remote_path))
                    print(f"  ✓ Updated: {remote_path.name}")
                else:
                    print(f"    ✗ Remote copy up to date: {remote_path.name}")
            else:
                shutil.copyfile(str(remote_path.name), str(remote_path))
                print(f"  ✓ Copied: {remote_path.name}")
        else:
            if remote_path.exists():
                if local_is_more_recent(local_path, remote_path):
                    compile_and_copy(local_path, remote_path, mpy_cross_exe)
                    print(f"  ✓ Compiled and updated: {remote_path.name}")
                else:
                    print(f"    ✗ Remote copy up to date: {remote_path.name}")
            else:
                compile_and_copy(local_path, remote_path, mpy_cross_exe)
                print(f"  ✓ Compiled and copied: {remote_path.name}")
    
    shutil.make_archive(os.getcwd(), 'zip', remote_dir)
    print(f" ✓ ZIP file saved to: {Path(__file__).resolve().parents[1]}")
    ### Add fsck code.

if __name__ == "__main__":
    main()