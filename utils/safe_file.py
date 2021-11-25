import os

def iter_incrementing_file_names(path):
    """
    Iterate incrementing file names. Start with path and add " (n)" before the
    extension, where n starts at 1 and increases.

    :param path: Some path
    :return: An iterator.
    """
    yield path
    prefix, ext = os.path.splitext(path)
    for i in itertools.count(start=1, step=1):
        yield prefix + ' ({0})'.format(i) + ext


def safe_open(path, mode):
    """
    Open path, but if it already exists, add " (n)" before the extension,
    where n is the first number found such that the file does not already
    exist.

    Returns an open file handle. Make sure to close!

    :param path: Some file name.

    :return: Open file handle... be sure to close!
    """
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

    if 'b' in mode and platform.system() == 'Windows':
        flags |= os.O_BINARY

    for filename in iter_incrementing_file_names(path):
        try:
            file_handle = os.open(filename, flags)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise
        else:
            return os.fdopen(file_handle, mode)

# Example
with safe_open("some_file.txt", "w") as fh:
    print("Hello", file=fh)