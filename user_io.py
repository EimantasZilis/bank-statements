import os

# Initialise directories
print('Initialising user directories...')
common = r"C:\Users\Eimantas\Dropbox\finances"
folders = ["input data", "output data", "plots\\Monthly"]
for folder in folders:
    dir = os.path.join(common,folder)
    os.makedirs(dir, exist_ok=True)
    print(' >>',dir)

# Set up required files and their directories
input_files = ['categories.csv', 'raw data.csv']
output_files = ['excluded returns.csv', 'unclassified.csv', 'classified.csv']
file_locations = {'output data': output_files, 'input data': input_files}

def directory(filename='', *opts):
    """
    Get directory for filename. Returns default
    directory for all input/output paths if filename
    not specified.

    Opt used for dynamic filenames that can change, e.g categories
    The acceptable opt values are:
        Pm - Directory for monthly plots
        Pa - Directory for annual plots
    """

    subdir = ''
    if opts:
        opt = opts[0]
        ok_opts = {'Pm': r'plots\Monthly'}
        if opt in ok_opts:
            subdir = ok_opts[opt]

    if not(subdir):
        for tempdir in file_locations:
            if filename in file_locations[tempdir]:
                subdir = tempdir
                break

    absolute_path = os.path.join(common,subdir,filename)
    return absolute_path
