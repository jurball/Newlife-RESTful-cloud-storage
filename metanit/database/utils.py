import random
import string

def generate_file_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"