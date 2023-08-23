

from django.shortcuts import render
from django.http import HttpResponse
from testweb1.forms import audioAccept
import os
from django.conf import settings

def sample(request):
    if request.method == 'POST':
        form = audioAccept(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['audioFile']
            
            # Determine the path to save the uploaded file
            save_path = os.path.join(settings.MEDIA_ROOT, 'accepted_Audio')  # 'accepted_Audio' is the subdirectory where you want to save the files
            os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
            
            # Construct the full file path
            file_name = uploaded_file.name
            file_path = os.path.join(save_path, file_name)
            
            # Save the uploaded file to the desired location
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Handle the uploaded file processing here, if needed
            
    else:
        form = audioAccept()
    
    context = {'form': form}
    return render(request, 'uiDesign.html', context)



from django.http import JsonResponse
from .forms import VideoIdForm  # Import your VideoIdForm
import requests

def convert_mp3(request):
    if request.method == 'POST':
        form = VideoIdForm(request.POST)
        if form.is_valid():
            video_id = form.cleaned_data['video_id']
            
            if not video_id:
                return render(request, 'uiDesign.html', {'success': False, 'message': 'Please enter a video ID'})
            
            api_key = '618c641402msh87f3cbb65fc2a64p16e8f2jsn2685ae2145b5'
            api_host = 'youtube-mp36.p.rapidapi.com'
            
            response = requests.get(f'https://youtube-mp36.p.rapidapi.com/dl?id={video_id}', 
                                    headers={"x-rapidapi-key": api_key, "x-rapidapi-host": api_host})
            
            fetch_response = response.json()
            
            if fetch_response.get('status') == 'ok':
                return render(request, 'uiDesign.html', {'success': True, 
                                                        'song_title': fetch_response.get('title'), 
                                                        'song_link': fetch_response.get('link')})
            else:
                return render(request, 'uiDesign.html', {'success': False, 'message': fetch_response.get('msg')})
    # else:
    #     form = VideoIdForm()

    return render(request, 'uiDesign.html', {'form': form})



             
