import shutil

from fastapi import UploadFile, File


def extract_object(object: tuple):
    return object[0]


def extract_objects(objects: tuple):
    for object_tuple in objects:
        yield object_tuple[0]
        

def write_file(filepath, file: UploadFile = File(...)):
    with open(filepath, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)