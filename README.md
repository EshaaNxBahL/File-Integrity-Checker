# File-Integrity-Checker
This code uses the SHA-256 hashing algorithm, implemented using the `hashlib.sha256()` function. 

Project Description:

This Python code implements a File Integrity Monitor application with a graphical user interface (GUI). It allows users to select a directory and monitor any changes to the files within that directory and its subdirectories. 

Here's a breakdown of the functionalities:

Monitoring: The application continuously monitors the selected directory at a user-defined interval (1 second by default).

Hashing: It calculates the SHA-256 hash of each file upon initial selection and stores them. 

Change Detection: During subsequent monitoring cycles, it recalculates the hashes and compares them with the stored values. Any discrepancies indicate a file modification.

Deletion Detection: It also compares the current list of files with the previously monitored ones. Missing files are identified as deletions.

Reporting: The application displays information about detected changes (file modification or deletion) in a designated text area within the GUI.

Use Cases:

*  Monitoring critical files for unauthorized modifications (e.g., configuration files, system files).
*  Verifying file integrity after transfers or downloads to ensure no corruption occurred.
*  Keeping track of file changes for version control or auditing purposes.

Limitations:

*  This application relies on file hashing, which cannot detect changes within a file if the overall hash remains the same. 
*  It monitors file system changes, not the content itself. 
*  It doesn't provide any data recovery functionalities.

Enhancements:

*  Implement real-time monitoring instead of relying on a fixed time interval.
*  Allow users to configure the monitoring interval.
*  Integrate with logging or notification systems for more robust alerting.
*  Consider incorporating additional hashing algorithms for different security needs.
