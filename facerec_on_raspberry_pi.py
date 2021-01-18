# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
from send_sms import send_sms
import png
import cv2
from save_to_s3 import upload_to_aws
import time;

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading ....")
time.sleep(10)
print("Loading ........")

# EDIT THE FILE NAME OF THE KNOW IMAGE 
image1 = face_recognition.load_image_file("known_faces/myphoto.jpg")
image1_face_encoding = face_recognition.face_encodings(image1)[0]

# EDIT THE FILE NAME OF THE KNOW IMAGE 
image2 = face_recognition.load_image_file("known_faces/friend.jpg")
image2_face_encoding = face_recognition.face_encodings(image2)[0]

known_face_encodings = [
    image1_face_encoding,
    image2_face_encoding
]

# EDIT THE PERSON NAMES FOR THE KNOW IMAGES 
known_face_names = [
    "Akshay",
    "Mehir"
]

# Initialize some variables
face_locations = []
face_encodings = []
countFaces = 0;
imgCount = 1;
while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
    
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Captured {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "<Unknown Person>"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if match[best_match_index]:
                name = known_face_names[best_match_index]
                
                #img_name = "{}.png".format(imgCount)
                #cv2.imwrite(img_name, output)
                #print("{} written!".format(img_name))
                #upload_to_aws(img_name,'unkown-faces-picam', img_name);
                imgCount = imgCount + 1;
                print("Known Face of : " +name +" detected in your room")
                #send_sms("Welcome to room :  "+ name,img_name)
                break;
        else:
                img_name = "{}.png".format(imgCount)
                cv2.imwrite(img_name, output)
                print("{} uploading image to AWS!".format(img_name))
                upload_to_aws(img_name,'unkown-faces-picam', img_name)
                imgCount = imgCount + 1;
                print("Unknown face detected in you room..SEedning SMS") 
                send_sms("Unkown Face Detected in you Room!", img_name)
                time.sleep(30);
                break;

        print("I can see you {}!".format(name))
