
from flask import Flask
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

def bubble_sort(data, drawData, speed):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                
                data[j], data[j + 1] = data[j + 1], data[j]
                colorArray = ['green' if index >= n - i else 'red' for index in range(n)]
                drawData(data.copy(), colorArray)
                time.sleep(speed) 
    return data

@socketio.on('start_sort')
def handle_start_sort(message):
    """
    Expected message format (JSON):
      {
         "array": [list of numbers],
         "speed": (number, e.g., 0.5)
      }
    """
    arr = message.get('array', [])
    speed = float(message.get('speed', 0.1))
    print("Starting sort with array:", arr)
    
    def callback(current_array, colorArray):
        
        emit('update', {'array': current_array, 'colors': colorArray}, broadcast=True)
    
    bubble_sort(arr, callback, speed)
    
    emit('done', {'message': 'Sorting complete'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
