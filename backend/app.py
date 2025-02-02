
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

def quick_sort(data, low, high, drawData, speed):
    if low < high:
        pivot_index = partition(data, low, high, drawData, speed)
        quick_sort(data, low, pivot_index - 1, drawData, speed)
        quick_sort(data, pivot_index + 1, high, drawData, speed)
    return data

def partition(data, low, high, drawData, speed):
    pivot = data[high]
    i = low - 1  # index of smaller element
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            # Create a color array: mark pivot position and current comparison
            colorArray = ['red'] * len(data)
            colorArray[high] = 'blue'  # pivot in blue
            colorArray[i] = 'green'
            colorArray[j] = 'green'
            drawData(data.copy(), colorArray)
            time.sleep(speed)
    # Place the pivot in the correct position
    data[i + 1], data[high] = data[high], data[i + 1]
    colorArray = ['red'] * len(data)
    colorArray[i + 1] = 'green'
    drawData(data.copy(), colorArray)
    time.sleep(speed)
    return i + 1



def merge_sort(data, left, right, drawData, speed):
    if left < right:
        mid = (left + right) // 2
        merge_sort(data, left, mid, drawData, speed)
        merge_sort(data, mid + 1, right, drawData, speed)
        merge(data, left, mid, right, drawData, speed)
    return data

def merge(data, left, mid, right, drawData, speed):
    # Copy data to temporary arrays
    leftPart = data[left:mid + 1]
    rightPart = data[mid + 1:right + 1]
    
    i = j = 0
    k = left

    while i < len(leftPart) and j < len(rightPart):
        if leftPart[i] <= rightPart[j]:
            data[k] = leftPart[i]
            i += 1
        else:
            data[k] = rightPart[j]
            j += 1
        # Mark the merged portion in green
        colorArray = ['green' if left <= idx <= k else 'red' for idx in range(len(data))]
        drawData(data.copy(), colorArray)
        time.sleep(speed)
        k += 1

    # Copy any remaining elements of leftPart
    while i < len(leftPart):
        data[k] = leftPart[i]
        i += 1
        colorArray = ['green' if left <= idx <= k else 'red' for idx in range(len(data))]
        drawData(data.copy(), colorArray)
        time.sleep(speed)
        k += 1

    # Copy any remaining elements of rightPart
    while j < len(rightPart):
        data[k] = rightPart[j]
        j += 1
        colorArray = ['green' if left <= idx <= k else 'red' for idx in range(len(data))]
        drawData(data.copy(), colorArray)
        time.sleep(speed)
        k += 1


@socketio.on('start_sort')
def handle_start_sort(message):
    """
    Expected message format (JSON):
      {
         "array": [list of numbers],
         "speed": (number, e.g., 0.5),
         "algorithm": algoritm type
      }
    """
    arr = message.get('array', [])
    speed = float(message.get('speed', 0.1))
    algorithm = message.get('algorithm',"bubble")
    print("Starting sort with array:", arr)
    
    def callback(current_array, colorArray):
        
        emit('update', {'array': current_array, 'colors': colorArray}, broadcast=True)
    
    print(algorithm)
    if algorithm=="bubble": bubble_sort(arr, callback, speed)
    elif algorithm == "quick": quick_sort(arr,0,len(arr)-1,callback,speed)
    elif algorithm == "merge": merge_sort(arr,0,len(arr)-1,callback,speed)
    else:
        emit("error",{"message":"unknown algorithm. Failed"}, broadcast=True)
        return
    emit('done', {'message': 'Sorting complete'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
