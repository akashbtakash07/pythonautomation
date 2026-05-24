"""
File Organizer Automation System
=================================
A professional Python automation tool that organizes files in a directory
by automatically sorting them into categorized folders based on file extensions.

Author: Your Name
Version: 1.0.0
"""

import os
import shutil
import datetime
import hashlib
from pathlib import Path


# ---------------------------------------------------------------------------
# Logging System
# ---------------------------------------------------------------------------

LOG_FILE = "logs.txt"


def log_operation(message: str) -> None:
    """
    Write a timestamped log entry to the log file and print to console.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Warning: Could not write to log file. {e}")

    print(log_entry)


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------


def get_folder_path() -> str:
    """
    Prompt the user for a folder path and validate that it exists.
    Returns the absolute path as a string.
    """
    while True:
        path = input("\nEnter the folder path to organize: ").strip()

        if not path:
            print("Path cannot be empty. Please try again.")
            continue

        # Expand the tilde (~) to the user's home directory if used
        path = os.path.expanduser(path)
        abs_path = os.path.abspath(path)

        if os.path.exists(abs_path) and os.path.isdir(abs_path):
            return abs_path
        else:
            print(f"Error: The path '{abs_path}' does not exist or is not a directory.")
            print("Please enter a valid folder path.")


def get_file_category(extension: str) -> str:
    """
    Map a file extension to a human-readable category folder name.
    Returns a string like 'PDF_Files' or 'Other_Files'.
    """
    # Strip the leading dot and convert to lowercase
    ext = extension.lstrip(".").lower()

    # If the extension is empty (file has no extension), treat as "No_Extension"
    if not ext:
        return "No_Extension_Files"

    return f"{ext.upper()}_Files"


def compute_file_hash(file_path: str, chunk_size: int = 8192) -> str:
    """
    Compute the MD5 hash of a file to detect duplicates.
    Reads the file in chunks to handle large files efficiently.
    """
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
    except Exception:
        return None
    return hasher.hexdigest()


def format_size(file_path: str) -> str:
    """
    Return a human-readable file size string.
    """
    try:
        size_bytes = os.path.getsize(file_path)
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes / (1024**2):.1f} MB"
        else:
            return f"{size_bytes / (1024**3):.2f} GB"
    except Exception:
        return "Unknown"


# ---------------------------------------------------------------------------
# Core Features
# ---------------------------------------------------------------------------


def display_file_stats(folder_path: str) -> None:
    """
    Scan and display statistics for all files in the given folder.
    Shows count, extension, and size for each file.
    """
    log_operation("Scanning folder for file statistics...")
    print("\n" + "=" * 60)
    print("                   FILE STATISTICS")
    print("=" * 60)

    files_found = 0
    extension_counts = {}

    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            if os.path.isfile(item_path):
                files_found += 1
                _, ext = os.path.splitext(item)
                ext = ext.lower() if ext else "(no extension)"
                extension_counts[ext] = extension_counts.get(ext, 0) + 1
                print(f"  {item:<40s} {format_size(item_path):>8s}")

        print("-" * 60)
        print(f"Total files found: {files_found}")
        print(f"Distinct extension types: {len(extension_counts)}")

        if extension_counts:
            print("\nExtension Summary:")
            for ext, count in sorted(extension_counts.items()):
                print(f"  {ext:<20s}: {count} file(s)")

    except PermissionError:
        log_operation(f"ERROR: Permission denied while scanning '{folder_path}'")
        print("Permission denied while scanning folder.")
    except Exception as e:
        log_operation(f"ERROR: Could not scan folder. {e}")
        print(f"An unexpected error occurred: {e}")

    print("=" * 60)


def create_backup(folder_path: str) -> str | None:
    """
    Create a timestamped backup folder and copy all files into it.
    Returns the path to the backup folder, or None on failure.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(folder_path, f"Backup_{timestamp}")

    try:
        os.makedirs(backup_dir, exist_ok=True)
        log_operation(f"Creating backup folder: '{backup_dir}'")

        files_copied = 0
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                shutil.copy2(item_path, backup_dir)
                files_copied += 1

        log_operation(f"Backup completed: {files_copied} file(s) copied to '{backup_dir}'")
        print(f"Backup created successfully at: {backup_dir}")
        return backup_dir

    except Exception as e:
        log_operation(f"ERROR: Backup failed. {e}")
        print(f"Backup failed: {e}")
        return None


def organize_files(folder_path: str, rename_files: bool = False) -> None:
    """
    Scan the target folder, create sub-folders based on file extensions,
    and move files into their corresponding folders.
    Optionally renames files sequentially during the move.
    """
    log_operation("Starting file organization...")
    print("\n" + "=" * 60)
    print("              FILE ORGANIZATION IN PROGRESS")
    print("=" * 60)

    extension_map = {}  # ext -> list of file paths
    files_moved = 0

    # -----------------------------------------------------------------------
    # Phase 1: Scan and categorize files
    # -----------------------------------------------------------------------
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            # Skip directories and the script/log/backup files themselves
            if os.path.isdir(item_path):
                continue
            if item == os.path.basename(__file__) or item == LOG_FILE:
                continue
            if item.startswith("Backup_"):
                continue

            _, extension = os.path.splitext(item)
            category = get_file_category(extension)

            if category not in extension_map:
                extension_map[category] = []
            extension_map[category].append((item, item_path))

    except PermissionError:
        log_operation("ERROR: Permission denied while reading folder contents.")
        print("Permission denied. Run as administrator or choose a different folder.")
        return
    except Exception as e:
        log_operation(f"ERROR: Failed to read folder. {e}")
        print(f"Error reading folder: {e}")
        return

    if not extension_map:
        log_operation("No files found to organize.")
        print("No files to organize in this folder.")
        return

    # -----------------------------------------------------------------------
    # Phase 2: Create category folders and move files
    # -----------------------------------------------------------------------
    for category in sorted(extension_map.keys()):
        category_path = os.path.join(folder_path, category)

        try:
            os.makedirs(category_path, exist_ok=True)
            log_operation(f"Created folder: '{category}'")
        except Exception as e:
            log_operation(f"ERROR: Could not create folder '{category}'. {e}")
            print(f"Failed to create folder '{category}': {e}")
            continue

        rename_counter = 1
        for file_name, file_path in extension_map[category]:
            try:
                if rename_files:
                    # Rename file as Category_001.ext, Category_002.ext, etc.
                    base_name = category.replace("_Files", "")
                    _, ext = os.path.splitext(file_name)
                    new_name = f"{base_name}_{rename_counter:03d}{ext}"
                    rename_counter += 1
                else:
                    new_name = file_name

                destination = os.path.join(category_path, new_name)

                # Handle name collisions
                if os.path.exists(destination):
                    base, ext = os.path.splitext(new_name)
                    collision_count = 1
                    while os.path.exists(destination):
                        new_name = f"{base}_{collision_count}{ext}"
                        destination = os.path.join(category_path, new_name)
                        collision_count += 1

                shutil.move(file_path, destination)
                files_moved += 1
                log_operation(f"Moved: '{file_name}' -> '{category}/{new_name}'")

            except Exception as e:
                log_operation(f"ERROR: Failed to move '{file_name}'. {e}")
                print(f"Error moving '{file_name}': {e}")

    print("-" * 60)
    print(f"Organization complete! {files_moved} file(s) organized.")
    print("=" * 60)
    log_operation(f"Organization finished. {files_moved} file(s) moved.")


def remove_empty_folders(folder_path: str) -> None:
    """
    Scan the target folder and remove any empty sub-folders.
    Does NOT remove the root folder or folders containing organized files.
    """
    log_operation("Scanning for empty folders...")
    print("\n" + "-" * 60)
    print("              REMOVING EMPTY FOLDERS")
    print("-" * 60)

    removed_count = 0

    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            if os.path.isdir(item_path):
                # Skip backup folders
                if item.startswith("Backup_"):
                    continue

                try:
                    # Check if the directory is empty
                    if not os.listdir(item_path):
                        os.rmdir(item_path)
                        removed_count += 1
                        log_operation(f"Removed empty folder: '{item}'")
                        print(f"Removed: '{item}'")
                except PermissionError:
                    log_operation(f"WARNING: Permission denied removing folder '{item}'")
                except Exception as e:
                    log_operation(f"WARNING: Could not remove folder '{item}'. {e}")

        if removed_count == 0:
            print("No empty folders found.")
        else:
            print(f"Removed {removed_count} empty folder(s).")

    except Exception as e:
        log_operation(f"ERROR: Failed to scan for empty folders. {e}")
        print(f"Error scanning folders: {e}")


def detect_duplicates(folder_path: str) -> None:
    """
    Scan the folder for duplicate files using MD5 hashing.
    Displays a report of all duplicate files found.
    """
    log_operation("Scanning for duplicate files...")
    print("\n" + "=" * 60)
    print("              DUPLICATE FILE DETECTION")
    print("=" * 60)

    hash_map = {}  # md5_hash -> list of file paths
    duplicates_found = False

    try:
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Skip log file
                if file_name == LOG_FILE:
                    continue

                file_hash = compute_file_hash(file_path)

                if file_hash is None:
                    continue

                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(file_path)

        # Report duplicates
        for file_hash, file_list in hash_map.items():
            if len(file_list) > 1:
                duplicates_found = True
                print(f"\nDuplicate group ({len(file_list)} files):")
                for path in file_list:
                    display_name = os.path.relpath(path, folder_path)
                    print(f"  - {display_name}")

        if not duplicates_found:
            print("No duplicate files found.")

    except Exception as e:
        log_operation(f"ERROR: Duplicate detection failed. {e}")
        print(f"Error detecting duplicates: {e}")

    print("=" * 60)
    log_operation("Duplicate scan completed.")


# ---------------------------------------------------------------------------
# Menu System
# ---------------------------------------------------------------------------


def display_menu() -> None:
    """
    Display the interactive menu and return the user's choice.
    """
    print("\n" + "#" * 60)
    print("#           FILE ORGANIZER AUTOMATION SYSTEM          #")
    print("#" * 60)
    print("#  1.  Display File Statistics                        #")
    print("#  2.  Create Backup                                  #")
    print("#  3.  Organize Files                                 #")
    print("#  4.  Organize Files (with Auto-Rename)              #")
    print("#  5.  Remove Empty Folders                           #")
    print("#  6.  Detect Duplicate Files                         #")
    print("#  7.  Run Full Automation (All Steps)                #")
    print("#  8.  Exit                                           #")
    print("#" + "=" * 58 + "#")

    while True:
        try:
            choice = input("\nEnter your choice (1-8): ").strip()
            if choice in ("1", "2", "3", "4", "5", "6", "7", "8"):
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
        except (KeyboardInterrupt, EOFError):
            return "8"


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------


def main() -> None:
    """
    Main entry point for the File Organizer Automation System.
    Displays the menu and orchestrates feature execution.
    """
    # Initialize log file
    try:
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write("File Organizer Automation System - Log File\n")
                f.write(f"Started: {datetime.datetime.now()}\n")
                f.write("=" * 60 + "\n")
    except Exception as e:
        print(f"Warning: Could not initialize log file. {e}")

    log_operation("Application started.")
    print("Welcome to the File Organizer Automation System!")

    folder_path = None

    while True:
        choice = display_menu()

        if choice == "8":
            log_operation("Application closed by user.")
            print("\nThank you for using File Organizer Automation System!")
            break

        # Ask for folder path if not already set
        if folder_path is None:
            folder_path = get_folder_path()
            log_operation(f"Target folder set to: '{folder_path}'")

        if choice == "1":
            display_file_stats(folder_path)

        elif choice == "2":
            create_backup(folder_path)

        elif choice == "3":
            organize_files(folder_path, rename_files=False)

        elif choice == "4":
            organize_files(folder_path, rename_files=True)

        elif choice == "5":
            remove_empty_folders(folder_path)

        elif choice == "6":
            detect_duplicates(folder_path)

        elif choice == "7":
            print("\n" + "=" * 60)
            print("           RUNNING FULL AUTOMATION")
            print("=" * 60)

            # Step 1: Display stats
            display_file_stats(folder_path)

            # Step 2: Create backup
            backup_path = create_backup(folder_path)

            # Step 3: Organize files (with rename)
            organize_files(folder_path, rename_files=True)

            # Step 4: Remove empty folders
            remove_empty_folders(folder_path)

            # Step 5: Detect duplicates (in organized folder)
            detect_duplicates(folder_path)

            print("\n" + "=" * 60)
            print("           FULL AUTOMATION COMPLETE!")
            print("=" * 60)
            log_operation("Full automation completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user. Exiting...")
        log_operation("Application interrupted by user (Ctrl+C).")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        log_operation(f"Unexpected error: {e}")
    finally:
        print("\nGoodbye!")
