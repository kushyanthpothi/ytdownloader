from django import forms

class DownloadForm(forms.Form):
    url = forms.URLField(label='YouTube Video URL', max_length=200)
    resolution = forms.CharField(label='Resolution', max_length=10)
    bitrate = forms.CharField(max_length=10, required=False)
    title = forms.CharField(max_length=255, required=False)
    
    # You can add more fields as needed

    def clean_url(self):
        url = self.cleaned_data['url']
        # Custom validation for YouTube URL format
        if not url.startswith('https://www.youtube.com/'):
            raise forms.ValidationError('The URL must be a valid YouTube video URL.')
        return url

    def clean_resolution(self):
        resolution = self.cleaned_data['resolution']
        # Custom validation for resolution format
        try:
            resolution_value = int(resolution[:-1])
            if resolution_value <= 0:
                raise forms.ValidationError('Resolution must be a positive integer.')
        except ValueError:
            raise forms.ValidationError('Invalid resolution value.')
        return resolution

from django import forms

class DownloadForm(forms.Form):
    video_url = forms.URLField(label='Video URL', required=True)
    resolution = forms.CharField(max_length=10, required=False)
    bitrate = forms.CharField(max_length=10, required=False)
    title = forms.CharField(max_length=255, required=False)
