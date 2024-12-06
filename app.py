import os
import cv2
from flask import Flask, render_template, Response, jsonify, request, redirect, url_for
import pickle
import math

app = Flask(__name__)

print(f"Templates folder: {os.path.join(os.getcwd(), 'templates')}")

# Load parking slots positions from the annotated CarParkPos file
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []

# Define width and height of parking slot
width, height = 110, 52

# Dictionary to store slot names and occupancy status
slot_occupancy = {slot_name: {'position': (x, y), 'occupied': False} for x, y, slot_name in posList}

# To store the entry point set by the user
entry_point = None

# Calculate Euclidean distance to find the nearest parking slot
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Find nearest empty parking slot based on user's entry point
def find_nearest_empty_slot(entry_point):
    if entry_point is None:
        return None

    nearest_slot = None
    min_distance = float('inf')  # Initialize min_distance to infinity

    for slot_name, slot_info in slot_occupancy.items():
        if not slot_info['occupied']:
            slot_position = slot_info['position']
            distance = euclidean_distance(entry_point, slot_position)
            if distance < min_distance:
                min_distance = distance
                nearest_slot = slot_name

    return nearest_slot

# Streaming video feed for the webpage
def generate_frames():
    global entry_point
    cap = cv2.VideoCapture('carPark.mp4')  # Replace with your video feed source

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Check parking space occupancy and update slot information
        for slot_name, slot_info in slot_occupancy.items():
            x, y = slot_info['position']
            imgCrop = frame[y:y + height, x:x + width]
            gray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
            count = cv2.countNonZero(binary)
            slot_info['occupied'] = count > 900  # Adjust threshold value as needed

        # Draw parking slots and mark them as occupied or empty
        for slot_name, slot_info in slot_occupancy.items():
            x, y = slot_info['position']
            occupied = slot_info['occupied']
            color = (0, 0, 255) if occupied else (0, 255, 0)  # Red for occupied, Green for empty
            cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
            cv2.putText(frame, slot_name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Highlight the nearest slot if entry point is set
        if entry_point:
            nearest_slot = find_nearest_empty_slot(entry_point)
            cv2.putText(frame, f'Nearest Slot: {nearest_slot}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.circle(frame, entry_point, 5, (255, 0, 0), -1)

        # Convert the frame to JPEG and yield as a byte stream
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Routes for the Flask app

@app.route('/')
def home():
    # Render the login page (index.html)
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login_post():
    # Get the form data from the login page
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the username and password match for admin or user
    if username == "admin" and password == "123456@admin":
        return redirect(url_for('dashboard_admin'))
    elif username == "user" and password == "123456@user":
        return redirect(url_for('dashboard_user'))
    else:
        return render_template('index.html', error="Invalid credentials, please try again.")

@app.route('/dashboard_admin')
def dashboard_admin():
    # Render the admin dashboard page (index2.html)
    return render_template('index1.html')

@app.route('/dashboard_user')
def dashboard_user():
    # Render the user dashboard page (index3.html)
    return render_template('index2.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_entry_point', methods=['POST'])
def set_entry_point():
    global entry_point
    try:
        data = request.get_json()

        # Validate data
        if 'x' not in data or 'y' not in data:
            return jsonify({"success": False, "message": "Missing 'x' or 'y' in request data"}), 400

        # Ensure coordinates are integers
        x = int(data['x'])
        y = int(data['y'])
        entry_point = (x, y)

        # Compute nearest slot
        nearest_slot = find_nearest_empty_slot(entry_point)

        # Log the entry point
        print(f"Entry point set to: {entry_point}")

        # Return the entry point and nearest slot in JSON format
        return jsonify({
            "success": True,
            "entry_point": entry_point,
            "nearest_slot": nearest_slot
        })
    except ValueError:
        return jsonify({"success": False, "message": "Invalid 'x' or 'y' value, must be numeric"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



