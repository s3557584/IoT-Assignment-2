import face_recognition
import cv2
from PIL import Image
from DatabaseUtil import DatabaseUtil
obj = DatabaseUtil()
class FaceAuthentication:
    """
    Task D
    
    FaceAuthentication class
    
    Mainly handles the face authentication
    """
    
    def __init__(self):
        """
        Empty Constructor
        """
        pass

    def loadImage(self, imgName):
        """
        This function loads the user's image from local image folder
        """
        img = ""
        try:
            img = face_recognition.load_image_file("/home/pi/Desktop/Assignment2/image/"+imgName+".jpg")
        except:
            print("Either image does not exists or wrong username")
        return img
    
    def captureImage(self):
        """
        This function uses the local machine's webcam and take a picture of the user
        """
        img = ""
        cam = cv2.VideoCapture(0)
        try:
            img = cam.read()
        except:
            print("")
            print("Error: Something went wrong.")     
        return img
    
    def faceAuthenticate(self, userInput, imgName, username):
        """
        Main face authenticate function
        
        Parameter:
            userInput(str): Takes in user's choice of using webcam or image to authenticate
            imgName(str): Takes in the image name that the user is using
            username(str): User's username
        
        Return:
            status(boolean): True if user is authenticated False if its not
        """
        img = ""
        status = False
        s = False
        
        #If user chooses A calls loadImage() function
        if userInput == "A" or userInput == "a":
            img = self.loadImage(imgName)
            if img != "":
                s = True   
        
        #If user chooses B calls captureImage() function        
        elif userInput == "B" or userInput == "b":
            img = self.captureImage()
            if img != "":
                s = True
        
        if s == True:
            count = 0
            result = obj.getImageName(username)
            
            #Checks if username is correct or not
            if len(result) == 0:
                print("Wrong username")
            else:
            #If correct loads registered image from local to compare with user input image 
                imageName = ""
                for i in result:
                    imageName= i[0]
                unknown_image = face_recognition.load_image_file("/home/pi/Desktop/Assignment2/image/"+str(imageName)+".jpg")
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
               

                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)


                rgb_small_frame = small_frame[:, :, ::-1]
                
                #Locate faces in picture
                face_locations = face_recognition.face_locations(rgb_small_frame)
                
                #Encode images
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                #Compare the two image
                check = face_recognition.compare_faces(unknown_encoding, face_encodings)

                #Assign image locations to 4 variables for display
                top, right ,bottom, left = (face_recognition.face_locations(img))[0]
                
                #Print face location in image
                print("fond face at top:{},left:{},bottom:{}.right:{}".format(top,left,bottom,right))
                face_image = img[top:bottom,left:right]
                pil_image=Image.fromarray(face_image)

                print(check)
                
                #If authenticated return true
                if check[0]:
                    status = True
                else:
                #If not return error message
                    print("unauthoerized access")
        return status

