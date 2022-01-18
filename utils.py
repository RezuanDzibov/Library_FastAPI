def extract_object(object: tuple):
    return object[0]


def extract_objects(objects: tuple):
    for object_tuple in objects:
        yield object_tuple[0]