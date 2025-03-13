import os
import pandas as pd
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import Appointment

class UploadCSVView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # Define the fixed folder
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        # Save the file
        file_path = os.path.join(upload_dir, file.name)
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Read CSV and store data
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            patient_name = row['Full Name (Code)']
            patient_folder = os.path.join(upload_dir, patient_name)
            os.makedirs(patient_folder, exist_ok=True)

            # Save patient data in the database
            Appointment.objects.create(
                date=row['Date'],
                time=row['Time'],
                full_name=row['Full Name (Code)'],
                location_description=row['Location Description (Code)'],
                mrn=row['MRN'],
                appointment_description=row['Appointment Description'],
                appointment_comment=row.get('Appointment Comment', ''),
                appointment_type=row['Appointment Type'],
                customize_date=row['Customize Date (Appt Details)'],
                default_division=row['Default Division'],
                location_region=row['Location Region'],
                location_type=row['Location Type'],
                main_appt=row['Main Appt'],
                phressia_filter=row['Phressia Filter'],
                provider_type_group=row['Provider Type (group)'],
                quality_specialty=row['Quality Specialty'],
                walk_in_filter=row['Walk-In Filter'],
                appt_scheduled_by=row['Appt Scheduled First Time By'],
                provider_type=row['Provider Type']
            )

        return Response({'message': 'File uploaded and processed successfully'}, status=status.HTTP_201_CREATED)

class AppointmentListView(APIView):
    def get(self, request):
        appointments = Appointment.objects.all().values()
        return Response(appointments, status=status.HTTP_200_OK)
