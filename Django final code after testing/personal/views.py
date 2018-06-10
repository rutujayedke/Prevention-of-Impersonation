from django.shortcuts import render
from django import forms
from django.http import HttpResponse
import MySQLdb
from django.contrib.auth import login, authenticate
from personal.forms import LoginForm, Form


import base64
import cv2
import re
import face_recognition
import pyttsx3	#text to speech library
engine = pyttsx3.init()

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def recognize(img, mis1):
	load_face_encodings = []
	names = []
	mis = "images_reg/" + mis1 + ".jpg"
	names.append(mis)
	try:
		load = face_recognition.load_image_file(mis)
	except:
		engine.say("Match Not Found")
		engine.runAndWait() 
		return False
	load_face_encodings.append(face_recognition.face_encodings(load)[0])


	# Initialize some variables
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True

	
	# Grab a single frame of video
	frame = img

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
				name = name[0:len(name) -4]
				mis1 = int(mis1)
				if(mis1 == 111507047):
					name = "Roshan"
				elif(mis1 == 111508079):
					name = "Rutuja"
				elif(mis1 == 111510001):
					name = Aanchal
				else:
					name= "Not Known"
				engine.say("Hi " + name +"Match successful")
				engine.runAndWait() 
				return True
			else:
				engine.say("Match Not Found")
				engine.runAndWait() 
				return False
			face_names.append(name)



def index(request):
	questions = None
	if request.POST.get('mis',''):
		mis = request.POST.get('mis')
	else:
		mis = "0"
	if request.POST.get('image', ''):
		data = request.POST.get('image')
		dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
		image_data=data
		image_data = dataUrlPattern.match(image_data).group(2)
		image_data = image_data.encode()
		image_data = base64.b64decode(image_data)

		conn = MySQLdb.connect(user="root", passwd="roshan", db="Impersonation_System", host='localhost')
		cur = conn.cursor()
		misId = int(mis)
		with open('screenshot.jpg', 'wb') as f:
			f.write(image_data)
		img = cv2.imread('screenshot.jpg')
		if(recognize(img, mis)):
			args = {'msg': "MATCH FOUND", 'n': 0}
			mis = int(mis)
			try:				
				cur.execute("INSERT INTO status values (%d, 'Match Found correctly','Present')" %(mis))
				conn.commit()
			except:
				args = {'msg': "Match Already Found and Entry has been Done", 'n':0}
			cur.close()
			conn.close()
			return render(request, "personal/home.html", args)
			
		else:
			args = {'msg': "MATCH NOT FOUND ", 'n': 0}
			mis = int(mis)
			try:
				cur.execute("INSERT INTO status values (%d, 'Match Not Found', 'Absent')" %(mis))
				conn.commit() 
			except:
				pass
			cur.close()
			conn.close()
			return render(request, "personal/home.html", args)



def studentdetails(request):
	return render(request, 'personal/studentdetails.html')

def showdetails(request):
	form = Form(request.POST)
	misId = request.GET.get('misId')
	conn = MySQLdb.connect(user="root", passwd="roshan", db="Impersonation_System",  host='localhost')
	cur = conn.cursor()
	misId = int(misId)
	cur.execute("SELECT * FROM student where MIS_No = %d" %(misId))
	row = cur.fetchone()
	name = row[1]
	sname = row[2]
	sId = row[3]
	image = row[6]
	args = {'misId' : misId, 'FullName' : name, 'SchoolName' : sname, 'SchoolId' : sId, 'image' : image }
	cur.close()
	conn.close()
	return render(request, 'personal/showdetails.html', args)


def contact(request):
	return render(request, "personal/basic.html", {'content': ['If you would like to contact me just email me', 'dn.roshan2@gmail.com']})

def main(request):
	class NameForm(forms.Form):
		your_name = forms.ImageField(label='snapshot', max_length=100)
	return render(request, "personal/main.html")

def success(request):
	return render(request, "personal/login_success.html")

def center_list(request):
	db = MySQLdb.connect(user='root', db='Impersonation_System',  passwd='roshan', host='localhost')
	cursor = db.cursor()
	cursor.execute('SELECT adminPassword FROM admin where adminId = 111')
	centerId = [row[0] for row in cursor.fetchall()]
	db.close()    
	return render(request, 'personal/show.html',  {'centerId': centerId})


def login(request):
	username = "not logged in"
	if request.method == "POST":
		MyLoginForm = LoginForm(request.POST)
		if MyLoginForm.is_valid():
			username = MyLoginForm.cleaned_data.get('username')
			raw_password = MyLoginForm.cleaned_data.get('password')
			raw_centerid = request.POST.get('id')
			request.session['centerid_session'] = raw_centerid
			user = authenticate(username=username, password=raw_password)
			db = MySQLdb.connect(user='root', db='Impersonation_System',  passwd='roshan', host='localhost')
			cursor = db.cursor()
			username = int(username)
			cursor.execute('SELECT * FROM admin where adminId = %d' %(username))
			rows = cursor.fetchall()
			for row in rows:
         			pass1 = row[2]
         			center1 = row[3]
			if((raw_password) == (pass1) and int(raw_centerid) == int(center1)):
				db.close()
				return render(request, 'personal/home.html')
			else:
				return render(request, 'personal/main.html')
	else:
		MyLoginForm = LoginForm()
	return render(request, 'personal/home.html')


def centerinfo(request):
	centerid_session1= request.session['centerid_session']
	centerid_session1= int(centerid_session1)
	conn = MySQLdb.connect(user="root", passwd="roshan", db="Impersonation_System",  host='localhost')
	cur = conn.cursor()
	cur.execute("SELECT * FROM school where schoolId=%d " %(centerid_session1))
	rows = cur.fetchall()
	for col in rows:
		centerId = col[0]
		Name = col[1]
		Address = col[2]
		contact = col[3]
		location = col[4]    	
	args = {'centerId' : centerId, 'Name': Name, 'Address': Address, 'contact': contact, 'location': location}
	cur.close()
	conn.close()
	return render(request, 'personal/center_info.html', args)



def report(request):
	conn = MySQLdb.connect(user="root", passwd="roshan", db="Impersonation_System",  host='localhost')
	cur = conn.cursor()
	cur.execute("SELECT * FROM status")
	rows = cur.fetchall()
	rollno = []
	name= []
	status = []
	remark = []
	for col in rows:
		rollno.append(col[0])
		if(col[0] == 111507047):	
			name.append("Roshan Nalawade")
		elif(col[0] == 111508079):
			name.append("Rutuja Yedke")
		elif(col[0] == 111510001):
			name.append("Aanchal Chugh")
		elif(col[0] == 111508002):
			name.append("Adheesh Phadake")
		elif(col[0] == 111508065):
			name.append("Shubham Mukkawar")
		elif(col[0] == 111508050):
			name.append("Onkar Marbhal")
		else:
			name.append("Not Known")
		status.append(col[1])
		remark.append(col[2])
	l = len(rollno)
	args = {'rollno' : rollno, 'name' : name, 'status' : status, 'remark' : remark}
	cur.close()
	conn.close()
	return render(request, 'personal/report.html',  args)


# Create your views here.
