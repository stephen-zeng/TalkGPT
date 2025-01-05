import os
from django.http import HttpResponse, Http404
from django.conf import settings

def audioFile(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'audio', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    raise Http404("File not found")
