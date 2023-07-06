from django.shortcuts import render
import cv2
import numpy as np
import pytesseract


# Create your views here.
from rest_framework.views import APIView, Response, status
from .serializers import ResultSerializer, StudentSerializer
from .Utils import NamedEntities
from .models import Result, Student
from .data.filterList import fetchAllData
from django.core import serializers

class GCEView(APIView):
    def get(self, request):
        name = request.data.get('name', None)
        level = request.data.get('level', None)
        student = Student.objects.filter(name = name).first()

        grade = Result.objects.filter(student_id = student).all()
        
        # serializer = ResultSerializer(grade, many=True)
        serialized_data = serializers.serialize('json', grade)
        print(serialized_data)
        return Response( serialized_data, status=status.HTTP_200_OK)


class GceCertificateView(APIView):

    def processImage(self, image):
        cleaned_image = self.cleanImage(image)
        # self.openImage(cleaned_image)

        
        top_half, bottom_half = self.fineTuneImage(cleaned_image)
        extractedBottomHalf = self.extractData(bottom_half)
        certificate_entities = self.findEntities(top_half)
        self.openImage(bottom_half)
        data = {
            'is_valid': True,
            'level': 'Ordinary',
            'year': '2017',
            'name': 'NJI KIMBI DARLINGTON',
            'results': extractedBottomHalf
        }
        return data

    def fineTuneImage(self, image):
        """
        Split the text into paragraphs based on the bounding box coordinates
        image: img
            The image you want to clean
        Returns
        -------
        image_tophalf: img
            the top half of the image
        image_bottomhalf: img
            the bottom half of the image
        """
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        paragraphs = []
        current_paragraph = []
        top_half = ''
        bottom_half = ''
        img_height, width = image.shape[:2]
        for i, word in enumerate(data['text']):
            if(data['text'][i]) == 'Name':
                print('conde =========', data['text'][i])
                left = data['left'][i]
                top = data['top'][i]
                width = data['width'][i]
                height = data['height'][i]
                text = data['text'][i]

                top_half = image[:top - 10, :]
                bottom_half = image[top - 10:, :]
                break
            else:
                top_half = image[:img_height // 2, :]
                bottom_half = image[img_height // 2:, :]


        # height, width = bottom_half.shape[:2]
        # middle = bottom_half[:height // 2, :]
        return top_half, bottom_half
    
                
    def openImage(self, image):
        """
        Preview the image
        Parameters
        ----------
        image: str
            The image you want to preview
        """
        cv2.imshow('Processed Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cleanImage(self, image):
        """
        Receives image and cleans it by resizing, converting to grayscale and making it binary
        Parameters
        ----------
        image: img
            The image you want to clean
        Returns
        -------
        image: img
            A binary image
        """
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # scale the image to half it's original size
        height, width = gray.shape[:2]
        scaled_image = cv2.resize(gray, (width // 2, height // 2), interpolation=cv2.INTER_LINEAR)

        # Get the original size of the image
        threshold_value = 127
        max_value = 255
        retval, image_binary = cv2.threshold(scaled_image, threshold_value, max_value, cv2.THRESH_BINARY)

        return image_binary

    def cleanData(self, text):
        """
        Removes all uncertainties from the image text and return a dictionary of subjects and grades
        Parameters
        ----------
        text: str
            extracted string of subjects
        Response
        --------
        text: obj
            An object of subject code, subject name and grade
        """

        responseData = []
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if index == 0:
                continue
            if len(line) < 1:
                continue
            if line == 'Grade':
                continue
            tokens = line.split()
            code = tokens[0]
            if len(tokens[-1]) > 3:
                subject = " ".join(tokens[1:])
                grade = ""
            else:
                subject = " ".join(tokens[1:-1])
                grade = tokens[-1]

            data = {
                "code": code,
                "Subject": subject,
                "Grade": grade
            }
            responseData.append(data)
        return responseData

    def findEntities(self, imageSection):
        try:
            config = '--psm 4 --oem 3 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            text = pytesseract.image_to_string(imageSection, lang='eng', config=config)
            # entity = NamedEntities.getName(text)
            # print(entity)
            level = ''
            lines = text.splitlines()
            for index, line in enumerate(lines):
                if len(line) < 2:
                    continue
                print(index)
                if line.startswith('Advance'):
                    level = 'advanced'
                    
                elif line.startswith('Ordinary'):
                    level = 'Ordinary'
                
                # print('line->', line)

        except Exception as e:
            print(e)
        return 

    def extractData(self, imageSection):
        try:
            config = '--psm 4 --oem 3 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            text = pytesseract.image_to_string(imageSection, lang='eng', config=config)
            print(text)
        except Exception as e:
            return e
        return self.cleanData(text)
    
        # text_cv = pytesseract.image_to_string(img_cv)

    def post(self, request, *args, **kwargs):
        if request.FILES.get('image'):
            image_file = request.FILES['image']
            try:
                image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
                
                res = self.processImage(image)
                
                return Response(res)
            except:
                return Response( "Error opening file", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response( 'error fetching data', status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ValidateResultView(APIView):
    def get_results(self, name, level, year):
        stud_id = self.get_student(name)
        grade = Result.objects.filter(student_id = stud_id).all()
        serialized_data = serializers.serialize('json', grade)

    def get_student(self, name):
        student = Student.objects.filter(name = name).first()

    def post(self, request):
        name = request.data.get('name')
        level = request.data.get('level')
        year = request.data.get('year')
        subjects = request.data.get('subjects')

        stud_res = self.get_results(name = name, level = level, year = year)
        for subject in subjects: 
            print(subject['subject'] + " --- " + subject['grade'])


        return Response("this is the server response", status=status.HTTP_200_OK)

    


# class Create(APIView):
#     def post(self, request):
#         body = self.request.body

#         print(body)

#         return Response({"message": "meet me"}, status=status.HTTP_200_OK)
    

def populateDB():
    data = fetchAllData()
    for dataItem in data:
        name = dataItem['name']
        grades = dataItem['grades']
        new_student = Student.objects.create(name=name)
        for grade in grades:
            Result.objects.create(student_id=new_student, subject=grade['title'].strip(), grade=grade['grade'].strip(), level='ordinary', education='general')

# populateDB()  