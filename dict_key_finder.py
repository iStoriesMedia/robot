def find(key, object):
    if isinstance(object, dict):
        for k, v in object.items():
            if key == k: 
                yield v
            if isinstance(v, (list, dict)): 
                yield from find(key, v)
    if isinstance(object, list): 
        for item in object: 
            yield from find(key, item) 
            
if __name__ == '__main__':
    find(key, object)