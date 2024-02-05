from django.core.files.storage import FileSystemStorage
from django.conf import settings

#this allows the user to overwrite their profile picture.
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name