import os
import shutil

def move(path,target):
    if not os.path.isdir(target):
        os.makedirs(target)
    shutil.move(path,target)
    return True

def copy(filename,path):
    shutil.copy(filename,path)
    return True

def delete(path):
    shutil.delete(path)
    return True

def clean_dir(root,path=''):
    if path =='':
        root = path
    for f in os.listdir(root):
        if os.path.isdir(f):
            clean_dir(root,os.path.join(root,f))
        elif os.path.isfile(f):
            if f.endswith('.tmp'):
                delete(os.path.join(root,f))
            else:
                if not os.path.isdir(os.path.join(root,f.split('.')[-1])):
                    os.makedirs(os.path.join(root,f.split('.')[-1]))
                move(os.path.join(root,f),os.path.join(root,f.split('.')[-1]))