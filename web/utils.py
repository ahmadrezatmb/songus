import  os
from django.template.defaultfilters import slugify

def get_file_upload_path(instance, filename):


    ext = filename.split('.')[-1]
    original_filename = filename.replace('.'+ext, '')

    return os.path.join('files/', "%s.%s" % (slugify(original_filename), ext.lower())) 

