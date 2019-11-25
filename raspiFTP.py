import ftplib  # documentation: https://docs.python.org/3/library/ftplib.html
import time


def getfile(filename, repeat_time=None):
    if repeat_time is None:
        with open(filename, 'wb') as fp:  # opens up target file in write binary (wb) mode
            ftp.retrbinary('RETR ' + filename, fp.write)
    elif repeat_time > 0:
        new_file = time.asctime() + filename
        # TODO add in a timer feature and how to exit
        with open(filename, 'wb') as new_file:
            ftp.retrbinary('RETR ' + filename, new_file.write)
    else:
        # throw an exception
        print('Check parameters of function getfile')


def login():
    try:
        ftp.login(ftpServerAccount, ftpServerPassword)  # login account and password
        print(ftp.getwelcome())
        ftp.cwd('/files')  # change dir into /files (no permission in /home/pi/ftp
        print('In your current working directory: ' + ftp.pwd())  # displays the current working directory
        ftp.dir()  # lists the content of the working directory

    except ftplib.all_errors as e:
        print(e)


# config
piHost = '192.168.43.196'  # ip of the pi
ftpServerAccount: str = 'pi'
ftpServerPassword: str = 'raspberry'

# opens the connection
# all upload/download should be made within this with statement
with ftplib.FTP(piHost) as ftp:
    ftp.set_debuglevel(0)  # showing more debug msg, 0 = none, 1 = some, 2 = all
    login()
    getfile('data.txt', repeat_time=1)
