import os
import shutil
from datetime import datetime

from fastapi import UploadFile, File


def extract_object(object: tuple):
    return object[0]


def extract_objects(objects: tuple):
    for object_tuple in objects:
        yield object_tuple[0]
        

def write_file(filepath, file: UploadFile = File(...)):
    with open(filepath, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        
        
def delete_file(filepath: str):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
    
    
def get_file_path(filename):
    current_datetime = '-'.join(str(datetime.now()).split(' ')).replace(':', '-').replace('.', '-')
    filepath = f'{current_datetime}_{filename}'
    return filepath