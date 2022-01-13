def extract_objects(objects, many: bool = False):
    if not many:
        return objects[0]
    objects_list: list = list()
    for object_tuple in objects:
        objects_list.append(object_tuple[0])
    return objects_list