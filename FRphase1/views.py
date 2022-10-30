from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
import face_recognition
import cv2
import numpy as np
from .models import FRdata2

def home(request):
    return render(request,'login.html')

def login(request):
    user1 = str(request.POST['user'])
    pass1 = str(request.POST['passwd'])

    print("username,password:",user1,pass1)
    #Getting User Credntials
    username = user1
    if username=="":
        print("======No Username written!======")
        return render(request,'Errorpage.html',{'signin':"Please Enter Username!"})
    else:
        user_credentials = []
        data_base = FRdata2.objects.filter(Username=username).only('img','Password')
        print("Database:",data_base)
        if len(list(data_base))==0:
            print("======Username Invalid!======")
            return render(request,'Errorpage.html',{'signin':"Username Invalid"})        
        else:
            for i in FRdata2.objects.filter(Username=username).only('img','Password'):
                user_credentials.append(i.img)
                user_credentials.append(i.Password)
            print("User-Credentials:",user_credentials)
            print("passw",user_credentials[1])
            #Checking all Formalities
            if pass1==str(user_credentials[1]):
                if FaceRecognition(request,pass1,user_credentials):
                    return render(request,'userpage.html',{'signin':user1})   
                else:
                    Error = "Face unable to recognise"
                    return render(request,'Errorpage.html',{'signin':Error})
            else:
                Error = "Wrong Password!"
                condition = 1 == 2
                return render(request,'Errorpage.html',{'signin':Error,'condition':condition})


def FaceRecognition(request,pass1,user_credentials):
    print("PASS1:",pass1)
    
    video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    print(user_credentials[0])
    load_Image = face_recognition.load_image_file(f"D:\MyPythonFolder6(Face_recognition)\FaceRecognition_website\media\{user_credentials[0]}")
    loadedImages_Encodings =face_recognition.face_encodings(load_Image)[0]

    #Remember to Save Encodings in List;)
    known_face_encodings = [loadedImages_Encodings]
    print('known face encodings',known_face_encodings)

    face_match = False
    face_locations = []
    face_encodings = []
    process_this_frame = True
    i=0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        print(ret)
        print(frame)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                print(matches)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    # name = known_face_names[best_match_index]
                    face_match = True
                    i+=1

                print(i)

        process_this_frame = not process_this_frame
        video_capture.release()
        cv2.destroyAllWindows()
        print("fface",face_match)

        if face_match:
            return True
        else:
            return False




