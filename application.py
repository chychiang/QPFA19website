# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from time import sleep
from threading import Thread, Event

# for data parsing
import csv

# dependencies for ftp to work
from ftplib import FTP  # documentation: https://docs.python.org/3/library/ftplib.html

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()

# ftp config
piHost = '192.168.43.196'  # ip of the pi
ftpServerAccount: str = 'pi'
ftpServerPassword: str = 'qp19'

def ftpGetFile():
    """
    Attempts to connect to the pi FTP server to retrieve data.
    Reads existing data, regardless of whether the retrival is successful or not.
    """
    try:
        ftp = FTP(piHost, timeout= 3)   # create the ftp object with the ip of the pi
        ftp.login(ftpServerAccount, ftpServerPassword)  # login pi 
        ftp.cwd('/files')   # change dir /pi/ftp/files - only have permission in /files
        ftp.dir()   # displays the dir on python console
        with open ('data.txt', 'wb') as fp:
            # fetches the file from pi and save it as "data.txt" locally
            ftp.retrbinary('RETR ' + 'data.txt', fp.write)
    except: 
        print("FTP error, check connection and config")
    finally: 
        # parses data from data.txt as a csv_file (formatted as a csv on pi)
        with open('data.txt') as csv_file:
            # parses the data from "data.txt"
            data = []  # refreshes array every loop
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                data.append(row)
            return data  # return the appended array

def sendDataWeb():
    """
    opens a ftp connection with the pi, downloads the data.txt file
    parses the data using csv reader and emits
    """
    while not thread_stop_event.isSet():
        # main loop
        laundryData = ftpGetFile() # retrieve data and stores the list in var
        print(laundryData)
        # converts raw data to human readable str
        # the data is passed in as str, so condition is also str
        machine1data = 'Unavailable' if int(laundryData[0][0]) == 1 else 'Available'
        machine2data = 'Unavailable' if int(laundryData[0][1]) == 1 else 'Available'
        # emits data to clients
        socketio.emit('data1', {'data': machine1data}, namespace='/test')
        socketio.emit('data2', {'data': machine2data}, namespace='/test')
        socketio.sleep(1)   # waits 1 sec


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(sendDataWeb)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
