from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from database.DataBase import Execute

import pandas as pd

def home(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        name_file = str(myfile).split('.')
        n_file = name_file[0].lower().replace(' ', '_')
        file = pd.read_excel(myfile)
        file = file.replace(to_replace=r'^.$', value=None, regex=True)
        upload = Execute(file, n_file)
        if upload:
            uploaded_file_url = f'Archivo {myfile} convertido a Tabla en PostgreSQL'
        else:
            uploaded_file_url = f'Archivo {myfile} No pudo ser procesado por favor revisa inconsistencias'
        return render(request, 'home.html', {'uploaded_file': uploaded_file_url})
    return render(request, 'home.html')
