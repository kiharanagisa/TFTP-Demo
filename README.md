# TFTP-Demo
Completed by using Python, with UDP, using empty data package to 
mean file has been downloaded or uploaded.

## Files
TFTP-Code.py: pack and unpack TFTP data packages.\
TFTP-Server.py: the server of TFTP.\
TFTP-Downloader.py: the downloader of TFTP.\
TFTP-Uploader.py: the uploader of TFTP.


## the code and mean of error_codes
| code | description                                       |
|------|---------------------------------------------------|
| 0    | Invalid type, type must be 1 or 2.                |
| 1    | Invalid mode, mode must be octet or netascii.     |
| 2    | Data is too large, max 512 bytes.                 |
| 3    | Invalid split id, id must be between 0 and 65535. |
| 4    | Invalid packed string.                            |
| 5    | Connection has not started.                       |
| 6    | No such file.                                     |
| 7    | file has already exist.                           | 
