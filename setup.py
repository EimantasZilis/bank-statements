import os

def user_dir(subpath=''):
    user_dir = r"C:\Users\Eimantas\Dropbox\finances"
    return user_idr

def output_plot_dir(filename=''):
    working_dir = user_dir()
    plot_dir = os.path.join(working_dir,'plots',filename)
    return plot_dir


def input_filepath(filename=''):
    path = user_dir('input data')
    if filename:
        path = os.path.join(path,filename)
    absolute_path = os.path.abspath(path)
    return path


def output_filepath(filename=''):
    path = user_dir('output data')
    if filename:
        path = os.path.join(path,filename)
    absolute_path = os.path.abspath(path)
    return absolute_path
