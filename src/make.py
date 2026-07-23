#!/usr/bin/env python3
# PERFEC System Euclidian Sequencer
# make.py
# copyright 2026, Tom Hoffman
# MIT License

import argparse
from pathlib import Path
import subprocess
import shutil
import os
import urllib.request
import sys

DONT_PRECOMPILE = {"boot.py", "code.py", "config.py", "make.py"}
DONT_UPDATE = {"config.py"}
SKIP = {"make.py", "make_release.py", "__pycache__"}
PY_EXT = "py"

# Supported target versions
SUPPORTED_VERSIONS = {"10.0.3", "10.1.4", "10.2.1"}

PLATFORM_SUFFIXES = {
    "linux-aarch64": ".static",
    "linux-amd64": ".static",
    "linux-raspbian": ".static",
    "macos-11": "",
    "macos": "",
    "windows": ".exe"
}

def is_python_file(filename: str) -> bool:
    return filename.endswith(PY_EXT)

def is_directory(local_path: Path) -> bool:
    return local_path.is_dir()

def local_is_more_recent(local_path: Path, remote_path: Path) -> bool:
    return os.path.getmtime(local_path) > os.path.getmtime(remote_path)

def generateRemotePath(root_path: Path, filename: str) -> Path:
    if filename in DONT_PRECOMPILE:
        return root_path / filename
    else:
        return root_path / f"{filename[:-len(PY_EXT)]}m{PY_EXT}"

def fetch_mpy_cross(platform: str, version: str) -> Path:
    """Downloads the required mpy-cross binary dynamically if it is missing."""
    if platform not in PLATFORM_SUFFIXES:
        print(f"Error: Unknown platform '{platform}'. Choose from: {list(PLATFORM_SUFFIXES.keys())}")
        sys.exit(1)
        
    suffix = PLATFORM_SUFFIXES[platform]
    
    # EXACT PATTERN MATCH: mpy-cross-linux-amd64-10.2.1.static
    binary_name = f"mpy-cross-{platform}-{version}{suffix}"
    url = f"https://adafruit-circuit-python.s3.amazonaws.com/bin/mpy-cross/{platform}/{binary_name}"
    
    cache_dir = Path.home() / ".cache" / "mpy-cross"
    cache_dir.mkdir(parents=True, exist_ok=True)
    local_binary_path = cache_dir / binary_name
    
    if not local_binary_path.exists():
        print(f"Downloading compiler: {url}")
        try:
            urllib.request.urlretrieve(url, local_binary_path)
            local_binary_path.chmod(0o755)  # Make executable
            print("✓ Download complete.")
        except Exception as e:
            print(f"Error downloading compiler from {url}: {e}")
            sys.exit(1)
            
    return local_binary_path

def compile_and_copy(local_path: Path, remote_path: Path, mpy_cross_exe: Path) -> None:
    """Process a single file with compilation + fallback copy logic."""
    try:
        # Use the explicit output flag '-o' to make mpy-cross compile 
        # and drop the bytecode file directly into the target volume allocation-free!
        result = subprocess.run(
            [str(mpy_cross_exe), "-o", str(remote_path), str(local_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        
        # Verify if the target bytecode file path exists successfully on the target side
        if not remote_path.exists():
            raise FileNotFoundError("Target .mpy file descriptor was not successfully written to destination.")
    except Exception as e:
        print(f" ! Compilation failed ({e}), copying directly...")
        shutil.copyfile(str(local_path), str(remote_path))
        print(f" ✗ Fallback copied: {remote_path}")

def main():
    parser = argparse.ArgumentParser(description="Compile CircuitPython files dynamically.")
    parser.add_argument("platform", help="Platform name string (e.g., linux-amd64, windows, macos)")
    parser.add_argument("version", help="CircuitPython version number (e.g., 10.0.3, 10.1.4, 10.2.1)")
    parser.add_argument("target_dir", help="Base target directory path for built files.")
    parser.add_argument("count", type=int, nargs="?", default=None, 
                        help="Optional suffix count to generate matching multi-target directories (e.g., EUCLID1, EUCLID2).")
    
    args = parser.parse_args()
    
    if args.version not in SUPPORTED_VERSIONS:
        sorted_versions = sorted(list(SUPPORTED_VERSIONS))
        print(f"Error: CircuitPython version '{args.version}' is not supported.")
        print(f"Supported versions are: {', '.join(sorted_versions)}")
        sys.exit(1)
    
    # 1. Resolve Compiler Path Dynamically
    mpy_cross_exe = fetch_mpy_cross(args.platform, args.version)
    
    # 2. Determine Output Directory Targets
    target_paths = []
    if args.count is not None:
        if args.count < 1:
            print("Error: Count must be 1 or greater.")
            sys.exit(1)
        base_path = args.target_dir
        for i in range(1, args.count + 1):
            target_paths.append(Path(f"{base_path}{i}"))
    else:
        target_paths.append(Path(args.target_dir))

    # 3. Process Build for Every Target Directory
    for remote_dir in target_paths:
        remote_dir.mkdir(parents=True, exist_ok=True)
        print(f"\nProcessing build directory: {remote_dir}")
        print("Scanning directory...")
        
        for filename in os.listdir("."):
            local_path = Path(filename)
            remote_path = generateRemotePath(remote_dir, filename)

            if not is_python_file(filename):
                if is_directory(local_path):
                    try:
                        shutil.copytree(local_path, remote_dir / filename)
                        print(f" ✓ Copied {filename} directory tree.")
                    except FileExistsError:
                        pass
                else:
                    print(f" ✗ Not a Python file: {filename}")
                    
            elif filename in SKIP:
                print(f" ✗ Skipping: {filename}")
                
            elif filename in DONT_UPDATE:
                if not remote_path.exists():
                    shutil.copyfile(str(local_path), str(remote_path))
                    print(f" ✓ Copied: {remote_path.name}")
                else:
                    if local_is_more_recent(local_path, remote_path):
                        print(f" ⚠ WARNING: you may need to manually update {filename}")
                    else:
                        print(f" ✗ Remote copy up to date: {remote_path.name}")
                        
            elif filename in DONT_PRECOMPILE:
                if remote_path.exists():
                    if local_is_more_recent(local_path, remote_path):
                        shutil.copyfile(str(local_path), str(remote_path))
                        print(f" ✓ Updated: {remote_path.name}")
                    else:
                        print(f" ✗ Remote copy up to date: {remote_path.name}")
                else:
                    shutil.copyfile(str(local_path), str(remote_path))
                    print(f" ✓ Copied: {remote_path.name}")
                    
            else:
                if remote_path.exists():
                    if local_is_more_recent(local_path, remote_path):
                        compile_and_copy(local_path, remote_path, mpy_cross_exe)
                        print(f" ✓ Compiled and updated: {remote_path.name}")
                    else:
                        print(f" ✗ Remote copy up to date: {remote_path.name}")
                else:
                    compile_and_copy(local_path, remote_path, mpy_cross_exe)
                    print(f" ✓ Compiled and copied: {remote_path.name}")

if __name__ == "__main__":
    main()
