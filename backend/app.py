# app.py
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
                # Swap
                data[j], data[j + 1] = data[j + 1], data[j]
                # Create a color array for visualization (for example, green for sorted part)
                colorArray = ['green' if index >= n - i else 'red' for index in range(n)]
                # Call the callback with a copy of the data and colors
                drawData(data.copy(), colorArray)
                time.sleep(speed)  # delay to control speed
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
        # Emit updated state to the client
        emit('update', {'array': current_array, 'colors': colorArray}, broadcast=True)
    
    # Run the sorting algorithm (this will call callback repeatedly)
    bubble_sort(arr, callback, speed)
    
    # Notify client that sorting is complete
    emit('done', {'message': 'Sorting complete'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
