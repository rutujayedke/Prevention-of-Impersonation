from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
from django.templatetags.static import static
import face_recognition
import cv2
import pyttsx3
"""def index(request):
	return HttpResponse("<h2>Hey!</h2>")
"""
def index(request):
    #play_video("/home/roshan/Downloads/Aashiq Banaya Aapne -Hate Story IV.mp4")
    print("Roshan")
    name = "roshan"
    a = 5
    i = 0
    for i in range(5):
        a = a + 1
    print(a)
    return HttpResponse("<h2>hi %s %d</h2>" %name %a)

def hello(request):
	#play_video("/home/roshan/Downloads/Aashiq Banaya Aapne -Hate Story IV.mp4")
	a = 5
	i = 0
	for i in range(5):
		a = a + 1
	print(a)
	a = str(a)
	video_capture = cv2.VideoCapture(0)
	#STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'static'),)
	#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
	#file_path = os.path.join(settings.STATIC_ROOT, 'names.txt')
	#fp = open(file_path, "r+")
#	fp = open("/static/webapp/names.txt", "r+")
	#file_path = url = static('webapp/names.txt')
	fp = open("/home/roshan/python/Django/mysite/webapp/static/webapp/names.txt", "r+")
	name = fp.readline()
	#name = "roshan.jpg"	
	load_face_encodings = []
	names = []
	while(name):
		name = name.strip()
		names.append(name)
		load = face_recognition.load_image_file("/home/roshan/python/"+name)
		load_face_encodings.append(face_recognition.face_encodings(load)[0])
		name = fp.readline()
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True
	while True:
    # Grab a single frame of video
		ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
		small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
		rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
		if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
			face_locations = face_recognition.face_locations(rgb_small_frame)
			face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

			face_names = []
			for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
				n = 0

				matches = face_recognition.compare_faces(load_face_encodings, face_encoding)
				name = "Unknown"

				if True in matches:
					first_match_index = matches.index(True)
					name = names[first_match_index]
					print(name)
                #name = name[0:len(name) -4]
                #engine.say("Hello " + name+ "Verification completed")
                #engine.say("Hello " + name)
                #engine.runAndWait() 

				face_names.append(name)
			process_this_frame = not process_this_frame


    # Display the results
			for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
				top *= 4
				right *= 4
				bottom *= 4
				left *= 4

        # Draw a box around the face
				cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
				cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
		cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

# Release handle to the webcam
	video_capture.release()
	cv2.destroyAllWindows()




	
	name = "roshan"
	html= "<html><body>My name is %s %s.</body></html>" % (name, a)
	return HttpResponse(html)	



# Create your views here.
