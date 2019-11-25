# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event

import csv

from ftplib import FTP  # documentation: https://docs.python.org/3/library/ftplib.html
import time


__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

# config
piHost = '192.168.43.196'  # ip of the pi
ftpServerAccount: str = 'pi'
ftpServerPassword: str = 'raspberry'


def randomNumberGenerator():
    """
    every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    number = 0
    temp = [0]
    #infinite loop of magical random numbers
    #print("Making random numbers")
    while not thread_stop_event.isSet():
        # opens the connection
    # all upload/download should be made within this with statement
        ftp = FTP(piHost)
        ftp.login(ftpServerAccount, ftpServerPassword)
        print(ftp.getwelcome())
        ftp.cwd('/files')
        ftp.dir()
        with open ('data.txt', 'wb') as fp:
            ftp.retrbinary('RETR ' + 'data.txt', fp.write)
        #number = round(random()*10, 3)
        #print(number)
        with open('data.txt') as csv_file:
            temp = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                for item in row:
                    temp.append(item)
            number1 = temp[0]
            number2 = temp[1]
            print(temp)
            
        socketio.emit('newnumber', {'number': "Machine1: "+ number1 + " Machine2:"+ number2}, namespace='/test')
        socketio.sleep(1)


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
        thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
