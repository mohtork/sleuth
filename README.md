# Sleuth
AWS Tools 

# Installation
1. git clone https://github.com/mohtork/sleuth.git
2. pip install -r requirements.txt

# S3
Get reports about S3 buckets to easily identify 
1. Infected files (download and scan bucket files with clamAV)
2. Which buckets have public access 
3. Buckets size in MB
4. Number of files in each backet
5. Check & fix public policy
6. Download bucket files to your machine


# Requirements
- ClamAV (https://goo.gl/fR81Mz)

# Commands
- List Buckets
python sleuth.py s3 list-buckets
- List Buckets permissions
python sleuth.py s3  list-permissions
- List Buckets Size
python sleuth.py s3 bucket-size
- List number of files for your buckets
python sleuth.py s3 count-files
- Fix Public ACL permissions
python sleuth.py s3 fix-acl-permissions
- Download bucket files to you machine or a server
python sleuth.py s3 download bucket_name download_dir_path
example: python sleuth.py s3 download linuxdirection /backup
linuxdirection: bucketname
/backup: the directory path on your machine
- Scan Bucket files
python sleuth.py s3 scan bucket_name download_dir_path
example: python sleuth.py s3 scan linuxdirection /tmp

