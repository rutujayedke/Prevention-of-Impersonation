from django.shortcuts import render
from django import forms
from django.http import HttpResponse

import base64
import cv2
import re
import face_recognition
import pyttsx3
engine = pyttsx3.init()

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def index(request):
	questions = None
	if request.POST.get('image', ''):
		data = request.POST.get('image')
		dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
	#image_data = self.cleaned_data['image_data']
		image_data=data
		image_data = dataUrlPattern.match(image_data).group(2)
		image_data = image_data.encode()
		image_data = base64.b64decode(image_data)
 
		with open('screenshot.jpg', 'wb') as f:
			f.write(image_data)
		img = cv2.imread('roshan.jpg')
		print(img)
		#cv2.imshow('image', img)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()

		load_face_encodings = []
		load = face_recognition.load_image_file("roshan.jpg")
		print("File opened")
		load_face_encodings.append(face_recognition.face_encodings(load)[0])
		small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
		rgb_small_frame = small_frame[:, :, ::-1]
		

		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

		face_names = []
		print("Hi")
		for face_encoding in face_encodings:
			n = 0
			print("inside for loop")
			#exit()
			matches = face_recognition.compare_faces(load_face_encodings, face_encoding)
			name = "Unknown"
			

			if True in matches:
				first_match_index = matches.index(True)			
				#name = names[first_match_index]
				#name = name[0:len(name) -4]
				engine.say("Hi " + "Roshan")
				print("Roshan Match found")
				engine.runAndWait()
 
			face_names.append(name)	
	

	return render(request, "personal/home.html")

def contact(request):
	return render(request, "personal/basic.html", {'content': ['If you would like to contact me just email me', 'dn.roshan2@gmail.com']})

# Create your views here.
