import os
import yt_dlp
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from urllib.parse import quote
from django.conf import settings
from django.shortcuts import render
from allauth.account.views import LoginView
from django.urls import reverse_lazy
from allauth.account.views import SignupView
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse

def contact(request):
    return render(request, 'app/contact.html')

def top10hits(request):
    return render(request, 'app/top10hits.html')

def home(request):
    return render(request, 'app/home.html')

class CustomLoginView(LoginView):
    template_name ='account/login.html'
    success_url = reverse_lazy('home')  # Redirect after successful login


class CustomSignupView(SignupView):
    template_name = 'account/signup.html'
    success_url = reverse_lazy('home')  # Redirect after successful signup

class Home(View):

    def get(self, request):
        return render(request, 'app/home.html')

    def post(self, request):
        if request.POST.get('fetch-vid'):
            url = request.POST.get('given_url')
            try:
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': os.path.join(settings.MEDIA_ROOT, 'downloads', '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'merge_output_format': 'mp4',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get('formats', [])
                    video_formats = [f for f in formats if f.get('vcodec') != 'none']
                    vidTitle = info.get('title', 'No Title')
                    vidThumbnail = info.get('thumbnail', 'No Thumbnail')

                    context = {
                        'vidTitle': vidTitle,
                        'vidThumbnail': vidThumbnail,
                        'formats': video_formats,
                        'url': url
                    }
                    return render(request, 'app/home.html', context)
            except Exception as e:
                context = {'error': str(e)}
                return render(request, 'app/home.html', context)

        elif request.POST.get('download-vid'):
            url = request.POST.get('given_url')
            quality = request.POST.get('quality')

            try:
                ydl_opts = {
                    'format': f'{quality}+bestaudio/best',
                    'outtmpl': os.path.join(settings.MEDIA_ROOT, 'downloads', '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'merge_output_format': 'mp4',
                    'ffmpeg_location': 'C:/ffmpeg',  # Update to your ffmpeg path
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_name = ydl.prepare_filename(info)
                    return self.serve_file(file_name, request)
            except Exception as e:
                context = {'error': str(e)}
                return render(request, 'app/home.html', context)

        elif request.POST.get('download-2160p'):
            return self.download_video_by_quality(request, 'bestvideo[height=2160]+bestaudio/best')

        elif request.POST.get('download-1080p'):
            return self.download_video_by_quality(request, 'bestvideo[height=1080]+bestaudio/best')

        elif request.POST.get('download-playlist'):
            url = request.POST.get('given_url')

            try:
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': os.path.join(settings.MEDIA_ROOT, 'downloads', '%(playlist)s', '%(title)s.%(ext)s'),
                    'noplaylist': False,
                    'merge_output_format': 'mp4',
                    'ffmpeg_location': 'C:/ffmpeg',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    return redirect('home')
            except Exception as e:
                context = {'error': str(e)}
                return render(request, 'app/home.html', context)

        return render(request, 'app/home.html')

    def download_video_by_quality(self, request, quality):
        url = request.POST.get('given_url')
        try:
            ydl_opts = {
                'format': quality,
                'outtmpl': os.path.join(settings.MEDIA_ROOT, 'downloads', '%(title)s.%(ext)s'),
                'noplaylist': True,
                'merge_output_format': 'mp4',
                'ffmpeg_location': 'C:/ffmpeg',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info)
                return self.serve_file(file_name, request)
        except Exception as e:
            context = {'error': str(e)}
            return render(request, 'app/home.html')

    def serve_file(self, file_path, request):
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=quote(os.path.basename(file_path)))
            response['Content-Disposition'] += '; filename*=UTF-8\'\'' + quote(os.path.basename(file_path))
            return response
        else:
            raise Http404("File does not exist")


def download_video(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', file_name)

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=quote(file_name))
        response['Content-Disposition'] += '; filename*=UTF-8\'\'' + quote(file_name)
        return response
    else:
        raise Http404("File does not exist")
    

    

def download_video(request):
    # Your download logic here

    channel_layer = get_channel_layer()
    for progress in range(0, 101, 10):
        async_to_sync(channel_layer.group_send)(
            "progress_group",
            {
                "type": "send_progress",
                "progress": progress
            }
        )

    return HttpResponse('Download started')

