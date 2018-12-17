import os

file_locations = {
    'output data':
        ['excluded returns.csv', 'unclassified.csv', 'classified.csv'],
    'input data':
        ['categories.csv', 'raw data.csv']
}

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
    common = r"C:\Users\Eimantas\Dropbox\finances"

    if opts:
        opt = opts[0]
        ok_opts = {'Pm': r'plots\Monthly', 'Pa': r'plots\Annual'}
        if opt in ok_opts:
            subdir = ok_opts[opt]

    if not(subdir):
        for tempdir in file_locations:
            if filename in file_locations[tempdir]:
                subdir = tempdir
                break

    absolute_path = os.path.join(common,subdir,filename)
    return absolute_path
