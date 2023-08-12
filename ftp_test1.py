from ftpext import FTPExt

ftp = FTPExt('192.168.48.130', 21, 'anonymous', 'anonymous@')
# ftp.login()


def getfile():
    ftp.retrlines('LIST')
    filename = input('Name of file:')
    local_file = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, local_file.write, 1024)
    local_file.close()


getfile()