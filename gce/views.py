from django.shortcuts import render
import cv2
import numpy as np
import pytesseract
from django.db.models import Q

# Create your views here.
from rest_framework.views import APIView, Response, status
from .serializers import ResultSerializer, StudentSerializer, InstitutionSerializer, AdmissionRequirementSerializer
from .Utils import NamedEntities
from .models import Result, Student, Institution, Certificate, AdmissionRequirement
from core.models import User
from .data.filterList import fetchAllData, preProcessed
from django.core import serializers

class GCEView(APIView):
    def get(self, request):
        name = request.data.get('name', None)
        level = request.data.get('level', None)
        student = Student.objects.filter(name = name).first()

        grade = Result.objects.filter(student_id = student).all()
        
        # serializer = ResultSerializer(grade, many=True)
        serialized_data = serializers.serialize('json', grade)
        return Response( serialized_data, status=status.HTTP_200_OK)


class GceCertificateView(APIView):

    def processImage(self, image):
        cleaned_image = self.cleanImage(image)
        # self.openImage(cleaned_image)

        
        top_half, bottom_half = self.fineTuneImage(cleaned_image)
        date, person, level = self.findEntities(top_half)
        extractedBottomHalf = self.extractData(bottom_half)

        is_valid, message = self.checkValid(person, date, level, extractedBottomHalf)

        if is_valid:
            self.saveCertificate(person, image)
        # self.openImage(top_half)
        data = {
            'is_valid': is_valid,
            'message': message,
            'level': level,
            'year': date,
            'name': person,
            'results': extractedBottomHalf
        }
        return data
    
    def saveCertificate(self, studentName, certificate):
        res = Certificate.objects.create(student_name=studentName, subject=certificate)
        return res

    def checkValid(self, person, year, level, result):
        try:
            student = Student.objects.filter(Q(name=person) & Q(year=year) & Q(level=level)).first()
            validSubject = []
            if not student:
                return False, "No such student in the server"
            
            subjects = Result.objects.filter(student_id = student.id).all()
            if len(subjects) != len(result):
                return False, "Results don't match"
            
            for res in result:
                for sub in subjects:
                    if res["Subject"] == sub.subject and res["Grade"] == sub.grade:
                        validSubject.append(res)
                        continue

            if len(validSubject) == len(result):
                return True, "valid certificate"

        except Exception as e:
            return e
        return False
    
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
                if grade == 'Cc':
                    grade = 'C'

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
            date, person = NamedEntities.getName(text)
            
            level = ''
            lines = text.splitlines()
            for index, line in enumerate(lines):
                if len(line) < 2:
                    continue
                if  'Advanced' in line or 'advanc' in line:
                    level = 'advanced'
                    
                elif 'Ordinary' in line or 'Ondinary' in line:
                    level = 'ordinary'
                elif line.__contains__(person):
                    person = line

            return date, person, level
                

        except Exception as e:
            print(e)
        return 

    def extractData(self, imageSection):
        try:
            config = '--psm 4 --oem 3 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            text = pytesseract.image_to_string(imageSection, lang='eng', config=config)
            # text = text.rstrip()
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
        student = self.get_student(name=name, year=year, level=level)
        if not student:
            return False
        return Result.objects.filter(student_id = student).all()


    def get_student(self, name, year, level):
        student = Student.objects.filter(Q(name=name) & Q(year=year) & Q(level=level)).first()
        return student

    def checkValid(self, server_result, result):
        try:
            
            validSubject = []
            if len(server_result) != len(result):
                return False, "Results don't match"
            
            for res in result:
                for sub in server_result:
                    if res["subject"].lower() == sub.subject.lower() and res["grade"].lower() == sub.grade.lower():
                        print(res)
                        print(sub)
                        print()
                        validSubject.append(res)
                        continue

            if len(validSubject) == len(result):
                return True, validSubject, "valid Input"

        except Exception as e:
            return e
        return False, validSubject, "Not valid"
    
    def post(self, request):
        name = request.data.get('name')
        level = request.data.get('level')
        year = request.data.get('year')
        results = request.data.get('subjects')
        education = request.data.get('education')

        server_results = self.get_results(name = name, level = level, year = year)
        if not server_results:
            return Response({"message": "Student not found", "is_valid": False}, status=status.HTTP_404_NOT_FOUND)
        
        state, responseList, message = self.checkValid(server_results, results)

        data = {
            'is_valid': state,
            'message': message,
            'level': level,
            'year': year,
            'name': name,
            'results': responseList
        }
        return Response(data, status=status.HTTP_202_ACCEPTED)

    

def populateDB(level, year, education):
    data = fetchAllData()
    save_db(data, level, year, education)

def processPopulate(level, year, education):
    data = preProcessed()
    save_db(data, level, year, education)

def save_db(data, level, year, education):
    for dataItem in data:
        name = dataItem['name']
        grades = dataItem['grades']
        new_student = Student.objects.create(name=name, level=level, year=year, education = education )
        for grade in grades:
            Result.objects.create(student_id=new_student, subject=grade['title'], grade=grade['grade'].strip())



class RestrictApiView( APIView ):
    def get(self, request):
        userId = request.data.get('id')
        postByUser = AdmissionRequirement.objects.filter(id=userId).all()

        serializers = AdmissionRequirementSerializer(postByUser)

        return Response({serializers.data}, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        institutionName = request.data.get('name')
        user_id = request.data.get('user_id')
        purpose = request.data.get('purpose')
        level = request.data.get('level')
        name = Institution.objects.filter(Q(name=institutionName) & Q(purpose = purpose) & Q(level = level)).first()

        if name:
            return Response({"message": "institution requirement already set"}, status = status.HTTP_403_FORBIDDEN)
       
        user = User.objects.filter(id=user_id).first()

        serializer = InstitutionSerializer(data=request.data) 

        if serializer.is_valid():
            serializer.save()

            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "response message"}, status=status.HTTP_200_OK)
    

    # def post(self, request):
    #     institutionName = request.data.get('name')
    #     purpose = request.data.get('purpose')
    #     level = request.data.get('level')
    #     name = Institution.objects.filter(Q(name=institutionName) & Q(purpose = purpose) & Q(level = level)).first()

    #     if name:
    #         return Response({"message": "institution requirement already set"}, status = status.HTTP_403_FORBIDDEN)
       
    #     serializer = InstitutionSerializer(data=request.data)   

    #     if serializer.is_valid():
    #         serializer.save()

    #         data = serializer.data
    #         return Response(data, status=status.HTTP_201_CREATED)
    #     # else:
    #     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #     return Response({"message": "response message"}, status=status.HTTP_200_OK)






# populateDB(level = 'advanced', year = '2011', education = 'general')  
# processPopulate(level = 'advanced', year = '2019', education = 'general')  