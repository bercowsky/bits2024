import glob
import os
import sys


def get_root_dir() -> str:
    '''
    Returns the "bits2024" directory absolute path.

    Returns
    -------
    str
        The "bits2024" directory absolute path.
    '''

    main_file = sys.argv[0]
    main_dir = os.path.dirname(main_file)

    # # If I am executing from main.py, I have to go up one level.
    # if main_file.endswith('.py'):
    #     main_dir = os.path.join(main_dir, '..')
    main_dir = os.path.join(main_dir, '..')

    main_dir = os.path.abspath(main_dir)

    return main_dir


def get_db_dir() -> str:
    '''
    Returns the folder where the database files are stored.


    Returns
    -------
    str
        The folder where the database files are stored.
    '''
    return os.path.join(get_root_dir(), 'db')


def get_models_dir() -> str:
    return os.path.join(get_db_dir(), 'models')


def get_available_models() -> tuple[str]:

    model_files = glob.glob(os.path.join(get_models_dir(), '*.pkl'))

    return tuple(set(map(lambda x: os.path.basename(x)[:-4], model_files)))


def get_preprocessing_dir() -> str:
    return os.path.join(get_db_dir(), 'preprocessing')
