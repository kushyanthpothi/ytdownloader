from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from yt_dlp import YoutubeDL
import os
import subprocess
from .forms import DownloadForm

def index(request):
    return render(request, 'downloader/index.html')

def fetch_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'noplaylist': True
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                
                video_details = {
                    'title': info_dict.get('title', None),
                    'thumbnail_url': info_dict.get('thumbnail', None),
                    'duration': info_dict.get('duration', 0),
                    'view_count': info_dict.get('view_count', 0),
                    'like_count': info_dict.get('like_count', 0),
                    'channel': info_dict.get('uploader', None),
                    'upload_date': info_dict.get('upload_date', None),
                    'description': info_dict.get('description', None),
                    'streams': [],
                    'audio_streams': []
                }
                
                duration = info_dict.get('duration', 0)
                seen_resolutions = set()
                seen_bitrates = set()

                formats = info_dict.get('formats', [])
                formats.sort(key=lambda x: (x.get('height', 0) or 0, x.get('tbr', 0) or 0), reverse=True)

                for f in formats:
                    # Video streams
                    if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                        height = f.get('height', 0)
                        width = f.get('width', 0)
                        resolution = f"{width}x{height}"
                        
                        if height > 0 and resolution not in seen_resolutions:
                            seen_resolutions.add(resolution)
                            filesize = f.get('filesize') or f.get('filesize_approx')
                            
                            if filesize is None:
                                tbr = f.get('tbr', 0) * 1024
                                filesize = (tbr * duration) / 8 if tbr > 0 else None

                            video_details['streams'].append({
                                'resolution': resolution,
                                'format': f.get('ext', 'unknown'),
                                'filesize': f"{filesize / (1024 * 1024):.2f} MB" if filesize else "Unknown",
                                'fps': f.get('fps', None),
                                'vcodec': f.get('vcodec', None)
                            })
                    
                    # Audio streams
                    elif f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                        bitrate = f.get('abr', 0) or 0  # Handle None case
                        if bitrate and bitrate >= 96 and bitrate not in seen_bitrates:
                            seen_bitrates.add(bitrate)
                            filesize = f.get('filesize') or f.get('filesize_approx')
                            
                            if filesize is None:
                                abr = bitrate * 1024
                                filesize = (abr * duration) / 8 if abr > 0 else None

                            video_details['audio_streams'].append({
                                'bitrate': int(bitrate),
                                'format': f.get('ext', 'unknown'),
                                'filesize': f"{filesize / (1024 * 1024):.2f} MB" if filesize else "Unknown",
                                'acodec': f.get('acodec', None)
                            })

                return JsonResponse(video_details)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def download_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        resolution = request.POST.get('resolution')

        try:
            if not video_url or not resolution:
                raise ValueError('Invalid video URL or resolution')

            ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg', 'bin', 'ffmpeg.exe')
            height = resolution.split("x")[1]

            # Download video
            video_opts = {
                'format': f'bestvideo[height<={height}]',
                'outtmpl': 'downloaded_videos/video.%(ext)s',
                'ffmpeg_location': ffmpeg_path,
                'extractor_args': {'youtube': {'formats': 'missing_pot'}}
            }

            # Download audio
            audio_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloaded_videos/audio.%(ext)s',
                'ffmpeg_location': ffmpeg_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'extractor_args': {'youtube': {'formats': 'missing_pot'}}
            }

            with YoutubeDL(video_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = info['title']
                video_path = ydl.prepare_filename(info)

            with YoutubeDL(audio_opts) as ydl:
                ydl.download([video_url])
                audio_path = 'downloaded_videos/audio.mp3'

            output_path = 'downloaded_videos/final_output.mp4'
            
            # Merge video and audio
            command = [
                ffmpeg_path,
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'copy',
                output_path
            ]

            subprocess.run(command, check=True)

            with open(output_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{video_title}.mp4"'
                return response

        except Exception as e:
            return HttpResponse(f'Error: {e}')
        finally:
            # Cleanup
            for file in [video_path, audio_path, output_path]:
                if 'file' in locals() and os.path.exists(file):
                    os.remove(file)

    return render(request, 'downloader/index.html', {'form': DownloadForm()})

def download_audio(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        bitrate = request.POST.get('bitrate')

        try:
            if not video_url or not bitrate:
                raise ValueError('Invalid video URL or bitrate')

            ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg', 'bin', 'ffmpeg.exe')

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloaded_audios/%(title)s.%(ext)s',
                'ffmpeg_location': ffmpeg_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': bitrate,
                }],
                'extractor_args': {
                    'youtube': {
                        'formats': 'missing_pot'  # Allow formats without PO token
                    }
                }
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                audio_title = info['title']
                audio_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'

                # Read and return the file
                with open(audio_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='audio/mp3')
                    response['Content-Disposition'] = f'attachment; filename="{audio_title}.mp3"'
                return response

        except Exception as e:
            return HttpResponse(f'Error: {e}')
        finally:
            # Cleanup
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)
    else:
        return render(request, 'downloader/index.html', {'form': DownloadForm()})