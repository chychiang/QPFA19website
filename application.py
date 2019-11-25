# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event

# for data parsing
import csv

# dependencies for ftp to work
from ftplib import FTP  # documentation: https://docs.python.org/3/library/ftplib.html


__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

# ftp config
piHost = '192.168.43.196'  # ip of the pi
ftpServerAccount: str = 'pi'
ftpServerPassword: str = 'raspberry'


def sendDataWeb():
    """
    opens a ftp connection with the pi, downloads the data.txt file
    parses the data using csv reader and emits
    """
    while not thread_stop_event.isSet():
        # opens the connection
        # all upload/download should be made within this with statement
        ftp = FTP(piHost)   # create the ftp object with the ip of the pi
        ftp.login(ftpServerAccount, ftpServerPassword)  # login pi 
        ftp.cwd('/files')   # change dir /pi/ftp/files - only have permission in /files
        ftp.dir()   # displays the dir on python console
        with open ('data.txt', 'wb') as fp:
            # fetches the file from pi and save it as "data.txt" locally
            ftp.retrbinary('RETR ' + 'data.txt', fp.write)
        with open('data.txt') as csv_file:
            # parses the data from "data.txt"
            temp = []   # generates a new array every loop
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                for item in row:
                    temp.append(item)   # stores item in data.txt into array temp
            number1 = temp[0]   # temporary
            number2 = temp[1]
            # TODO: reorginize data as nested arrays
            # print(temp)

        # TODO: send multiply "strands" of data with different keys 
        socketio.emit('newnumber', {'number': "Machine1: "+ number1 + " Machine2:"+ number2}, namespace='/test')
        socketio.sleep(1)   # wait 1 sec


#ben - these we didn't touch
@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(sendDataWeb)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
