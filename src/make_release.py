#!/usr/bin/env python3
# PERFEC System Release Automation
# make_release.py
# copyright 2026, Tom Hoffman
# MIT License
# Generates isolated zipped packages inside the release folder directory.

import argparse
import subprocess
import shutil
import sys
from pathlib import Path

try:
    import make
except ImportError:
    print("Error: Could not import 'make.py'. Ensure it exists in the current directory.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate individual version compiled .mpy zip packages inside the release folder.")
    parser.add_argument("platform", help="Platform name string (e.g., linux-amd64, windows, macos)")
    parser.add_argument("release_name", help="Name of this release tag (e.g., v1.0.0-beta, final-release)")
    
    args = parser.parse_args()
    
    current_dir = Path(".").resolve()
    make_script = current_dir / "make.py"
    
    bin_base_dir = current_dir.parent / "bin"
    release_dir = bin_base_dir / args.release_name
    
    versions_to_build = make.SUPPORTED_VERSIONS
    
    print("==================================================")
    print(f"Starting Per-Version Release Process: {args.release_name}")
    print(f"Output Release Directory: {release_dir}")
    print("==================================================\n")

    # Build and bundle each version independently
    for cp_version in versions_to_build:
        version_target_dir = release_dir / cp_version
        print(f"📦 Compiling files for CircuitPython {cp_version}...")
        
        build_process = subprocess.run(
            [sys.executable, str(make_script), args.platform, cp_version, str(version_target_dir)],
            capture_output=True,
            text=True
        )
        
        if build_process.returncode != 0:
            print(f" ✗ Error building version {cp_version}:")
            print(build_process.stderr)
            sys.exit(1)
        
        # --- FIXED ZIP PATH EXTENSION ---
        # Directs the archival engine to drop the zip file STRAIGHT inside the release directory
        # Target format path: ../bin/<release_name>/<release_name>-<cp_version>.zip
        zip_base_filename = release_dir / f"{args.release_name}-{cp_version}"
        print(f" -> Compressing {cp_version} release archive...")
        
        try:
            actual_zip_path = shutil.make_archive(
                base_name=str(zip_base_filename),
                format="zip",
                root_dir=str(release_dir),
                base_dir=cp_version
            )
            print(f" ✓ Generated zip inside release folder: {Path(actual_zip_path).name}")
        except Exception as e:
            print(f" ✗ Compression failed for version {cp_version}: {e}")
            sys.exit(1)
            
        print("") # Formatting gap

    print("==================================================")
    print(" 🎉 ALL PER-VERSION RELEASES PACKAGED IN RELEASE FOLDER! 🎉")
    print("==================================================")

if __name__ == "__main__":
    main()
