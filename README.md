# File Organizer Automation System

A professional Python automation tool that organizes files in a directory by automatically sorting them into categorized folders based on file extensions. Built with modular functions, exception handling, and a complete logging system.

## Features

### Core Features
- **Folder Selection** – Interactive prompt with path validation
- **File Scanning** – Reads all files from the target directory
- **Auto-Categorization** – Creates folders dynamically based on file extensions (e.g., `JPG_Files`, `PDF_Files`, `TXT_Files`)
- **File Organization** – Moves files into their corresponding category folders
- **Auto-Rename** – Optionally renames files sequentially (e.g., `JPG_001.jpg`, `JPG_002.jpg`)
- **Empty Folder Cleanup** – Removes empty sub-folders after organization
- **Logging System** – Every operation is logged to `logs.txt` with timestamps
- **Error Handling** – Comprehensive `try-except` blocks throughout the code

### Bonus Features
- **Menu-Driven Interface** – Interactive console menu (1-8) for easy navigation
- **Duplicate File Detection** – Scans for duplicate files using MD5 hashing
- **File Size Display** – Shows human-readable file sizes (B, KB, MB, GB)
- **Backup Creation** – Creates timestamped backup folder before making changes
- **Full Automation Mode** – Runs all operations in sequence with a single command

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python 3 | Core programming language |
| `os` module | File system operations, directory traversal |
| `shutil` module | File moving and copying |
| `hashlib` module | MD5 hashing for duplicate detection |
| `datetime` module | Timestamp generation for logs and backups |
| `pathlib` module | Cross-platform path handling |

## Project Structure

```
file_automation/
│
├── automation.py          # Main Python script
├── logs.txt               # Auto-generated log file
├── README.md              # Project documentation
│
└── sample_files/          # Sample files for testing
    ├── document.txt
    ├── sample.pdf
    ├── index.html
    ├── script.js
    ├── data.json
    ├── config.xml
    ├── script.py
    ├── readme.md
    ├── photo.jpg
    ├── image.png
    └── data.csv
```

## How to Run

### Prerequisites
- Python 3.6 or higher installed on your system

### Steps

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/yourusername/file-organizer-automation.git
   cd file_automation
   ```

2. **Run the script**
   ```bash
   python automation.py
   ```

3. **Follow the interactive menu**
   ```
   Enter your choice (1-8): 7
   ```

## Sample Output

### Terminal Output (Full Automation)

```
########################################################################
#           FILE ORGANIZER AUTOMATION SYSTEM          #
########################################################################
#  1.  Display File Statistics                        #
#  2.  Create Backup                                  #
#  3.  Organize Files                                 #
#  4.  Organize Files (with Auto-Rename)              #
#  5.  Remove Empty Folders                           #
#  6.  Detect Duplicate Files                         #
#  7.  Run Full Automation (All Steps)                #
#  8.  Exit                                           #
#==================================================================#

Enter your choice (1-8): 7


====================================================================
           RUNNING FULL AUTOMATION
====================================================================

[2026-05-24 11:30:00] Scanning folder for file statistics...

====================================================================
                   FILE STATISTICS
====================================================================
  photo.jpg                                     1.2 KB
  document.txt                                  0.5 KB
  image.png                                     0.8 KB
  script.py                                     0.3 KB
  data.json                                     0.4 KB
  config.xml                                    0.6 KB
  index.html                                    0.7 KB
  readme.md                                     0.2 KB
  sample.pdf                                    0.5 KB
  script.js                                     0.3 KB
  data.csv                                      0.4 KB
------------------------------------------------------------------
Total files found: 11
Distinct extension types: 9

Extension Summary:
  .csv           : 1 file(s)
  .html          : 1 file(s)
  .jpg           : 1 file(s)
  .json          : 1 file(s)
  .js            : 1 file(s)
  .md            : 1 file(s)
  .pdf           : 1 file(s)
  .png           : 1 file(s)
  .py            : 1 file(s)
  .txt           : 1 file(s)
====================================================================

[2026-05-24 11:30:01] Creating backup folder: 'Backup_20260524_113001'
Backup created successfully at: C:\Users\...\sample_files\Backup_20260524_113001

[2026-05-24 11:30:02] Starting file organization...
[2026-05-24 11:30:02] Created folder: 'CSV_Files'
[2026-05-24 11:30:02] Moved: 'data.csv' -> 'CSV_Files/CSV_001.csv'
[2026-05-24 11:30:02] Created folder: 'HTML_Files'
[2026-05-24 11:30:02] Moved: 'index.html' -> 'HTML_Files/HTML_001.html'
...
[2026-05-24 11:30:05] Organization finished. 11 file(s) moved.

[2026-05-24 11:30:06] Scanning for empty folders...
No empty folders found.

====================================================================
           FULL AUTOMATION COMPLETE!
====================================================================
```

### Sample logs.txt

```
File Organizer Automation System - Log File
Started: 2026-05-24 11:30:00
============================================================
[2026-05-24 11:30:00] Application started.
[2026-05-24 11:30:00] Target folder set to: 'C:\Users\...\sample_files'
[2026-05-24 11:30:00] Scanning folder for file statistics...
[2026-05-24 11:30:01] Creating backup folder: 'C:\Users\...\Backup_20260524_113001'
[2026-05-24 11:30:01] Backup completed: 11 file(s) copied to 'C:\Users\...\Backup_20260524_113001'
[2026-05-24 11:30:02] Starting file organization...
[2026-05-24 11:30:02] Created folder: 'CSV_Files'
[2026-05-24 11:30:02] Moved: 'data.csv' -> 'CSV_Files/CSV_001.csv'
[2026-05-24 11:30:02] Moved: 'data.json' -> 'JSON_Files/JSON_001.json'
[2026-05-24 11:30:02] Moved: 'config.xml' -> 'XML_Files/XML_001.xml'
[2026-05-24 11:30:02] Moved: 'document.txt' -> 'TXT_Files/TXT_001.txt'
[2026-05-24 11:30:02] Moved: 'index.html' -> 'HTML_Files/HTML_001.html'
[2026-05-24 11:30:02] Moved: 'script.js' -> 'JS_Files/JS_001.js'
[2026-05-24 11:30:02] Moved: 'script.py' -> 'PY_Files/PY_001.py'
[2026-05-24 11:30:02] Moved: 'readme.md' -> 'MD_Files/MD_001.md'
[2026-05-24 11:30:02] Moved: 'photo.jpg' -> 'JPG_Files/JPG_001.jpg'
[2026-05-24 11:30:02] Moved: 'image.png' -> 'PNG_Files/PNG_001.png'
[2026-05-24 11:30:02] Moved: 'sample.pdf' -> 'PDF_Files/PDF_001.pdf'
[2026-05-24 11:30:05] Organization finished. 11 file(s) moved.
[2026-05-24 11:30:06] Scanning for empty folders...
[2026-05-24 11:30:07] Duplicate scan completed.
[2026-05-24 11:30:07] Full automation completed successfully.
```

## Requirements Explained

| Requirement | Implementation |
|-------------|---------------|
| Python | Written in Python 3 with standard library only |
| OS module | `os.listdir()`, `os.path.join()`, `os.makedirs()`, `os.rmdir()`, `os.walk()` |
| Exception handling | `try-except` blocks around all file operations, permission checks |
| Logging | `logs.txt` with `[YYYY-MM-DD HH:MM:SS]` timestamps for every operation |
| User input | Interactive menu and folder path prompt with validation |
| File sorting | Dynamic folder creation based on file extension category mapping |
| File renaming | Sequential renaming with padding: `Category_001.ext`, `Category_002.ext` |
| Empty folder cleanup | `os.rmdir()` after verifying directory is empty |
| Menu interface | Console-based numbered menu with input validation |
| Duplicate detection | MD5 hashing with chunked reading for large files |
| File size display | Human-readable format (B, KB, MB, GB) |
| Backup creation | Timestamped backup folder with `shutil.copy2()` |

## Future Improvements

- **GUI Interface** – Build a desktop app using Tkinter or PyQt
- **Configurable Rules** – Allow users to define custom extension-to-folder mappings via JSON
- **Real-Time Monitoring** – Watchdog-based folder monitoring for auto-organization
- **Compression Support** – Archive older files into ZIP archives
- **Cloud Backup** – Push backups to Google Drive or Dropbox
- **Filter by Date** – Organize files by creation/modification date as well as extension
- **Undo Feature** – Roll back the last organization operation
- **Multi-threading** – Process large folders faster with concurrent operations

## License

This project is open-source and available for educational and professional use.

---

**Made with Python** – Internship-ready project for GitHub submission.
#   p y t h o n a u t o m a t i o n  
 