import sys, os
sys.path.extend(['lib'])

def pypath():
    """ Setup the environment and python path for django and for dev_appserver.
    """

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    # Set up the python path using dev_appserver
    for path in os.environ.get('PATH').split(os.pathsep):
        # ignore non-existing directories in PATH
        if not os.path.exists(path):
            continue
        if 'dev_appserver.py' in os.listdir(path):
            sdk_path = os.path.dirname(os.path.join(path, 'dev_appserver.py'))
            sys.path.insert(0, sdk_path)
            from dev_appserver import fix_sys_path
            fix_sys_path()

            # django 1.3 at top of path to obscure hobbled version
            sys.path.insert(0, os.path.join(sdk_path, 'lib', 'django_1_3'))
