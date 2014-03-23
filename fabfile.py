import os
from os.path import expanduser
from StringIO import StringIO

from fabric.api import cd, env, hide, run, get, put, settings, abort, prompt
from fabric.network import disconnect_all
from fabric.contrib.files import exists, upload_template


PROJECT_NAME = 'shev'
USERNAME = 'ubuntu'
ROOT_USER = 'root'
USER_DIR = '/usr/{}'.format(USERNAME)
DEPLOY_PATH = '{}/{}'.format(USER_DIR, PROJECT_NAME)
VENV_PATH = '{}/venv'.format(DEPLOY_PATH)

env.hosts = os.environ['HOST']
env.password = ''
env.use_ssh_config = True


def as_root():
    env.user = ROOT_USER
    disconnect_all()


def as_ubuntu():
    env.user = USERNAME
    disconnect_all()


def setup(repo='git@github.com:AJamesPhillips/shev.git'):
    as_root()
    create_user(USERNAME)
    setup_ssh()
    install_dependancies()
    ensure_dir('/var/log/{}'.format(PROJECT_NAME), USERNAME)
    setup_nginx()

    as_ubuntu()
    setup_user_env()
    clone_repo(repo=repo, destination=DEPLOY_PATH)
    install_repo_dependancies()
    setup_db()


def create_user(username):
    home_dir = '/usr/{}'.format(username)
    ensure_dir(home_dir, username)
    with settings(warn_only=True):
        user_present = run('id {u}'.format(u=username)).return_code == 0
        if user_present is False:
            run('useradd {} --home {} --shell /bin/bash'.format(username, home_dir))
    # run('adduser {} sudo'.format(username))


def ensure_dir(path, username):
    run('mkdir -p {}'.format(path))
    run('chown {} {}'.format(username, path))


def setup_ssh():
    """
    Ensures the correct private and public keys are on local machine before
    adding public part to authorized_keys on remote host
    """
    if not exists('~/.ssh/id_rsa'):
        run('ssh-keygen')
        pub_key = get_contents('~/.ssh/id_rsa.pub')
        prompt('You will need to add the public key to your github repo:' +
               '\n\n{}\n\n> Ok, got it thanks! (press enter to continue)'.format(pub_key))
    put(local_path='./deploy/templates/sshd_config.txt', remote_path='/etc/ssh/sshd_config', use_sudo=True)
    key_name = 'nhs_shev'
    pem_key = expanduser('~/.ssh/{}.pem'.format(key_name))
    pub_key = expanduser('~/.ssh/{}.pub'.format(key_name))
    ssh = '{}/.ssh'.format(USER_DIR)
    ensure_dir(ssh, USERNAME)
    authorized_keys = '{}/.ssh/authorized_keys'.format(USER_DIR)
    put(local_path=pub_key, remote_path=authorized_keys)
    run('chmod 600 {}'.format(authorized_keys))

    # set local ssh config
    local_config = 'Host {}\nUser {}\nIdentityFile {}'.format(env.host_string, USERNAME, pem_key)
    config_filename = expanduser('~/.ssh/config')
    print "You'll want to put the following in your file '{}' and then add {} to your ssh-agent:\n\n{}\n\n".format(config_filename, pem_key, local_config)
    print ("And you'll want to add the following to your sudoers using visudo:\n\n" +
           "# Allow the ubuntu use to manage upstart applications" +
           "ubuntu ALL=(ALL:ALL) NOPASSWD: /usr/sbin/service, /sbin/start, /sbin/restart, /sbin/stop\n\n")
    prompt("> Yep, I've got it thanks! (press enter to continue)")


def chown(username, file_or_dir):
    run('chown -R {} {}'.format(username, file_or_dir))


def get_contents(remote_path):
    fd = StringIO()
    get(remote_path, fd)
    return fd.getvalue()


def setup_user_env():
    put('deploy/templates/bashrc', '~/.bashrc')
    put('deploy/templates/profile', '~/.profile')


def clone_repo(repo, destination):
    run('mkdir -p {}'.format(destination))
    if not exists('{}/.git'.format(destination)):
        run('git clone {} {}'.format(repo, destination))


def install_dependancies():
    run('apt-get update')
    run('apt-get install -y gcc libevent-dev python-all-dev python-pip git nginx')
    run('pip install virtualenv')


def setup_nginx():
    as_root()
    context = {
      'PORT': os.environ['PORT'],
      'DEPLOY_PATH': DEPLOY_PATH,
    }
    upload_template(filename='./deploy/templates/nginx-sites-enabled/app',
      context=context, backup=False,
      destination='/etc/nginx/sites-enabled/app.conf')
    run('update-rc.d nginx defaults')


def install_repo_dependancies():
    with cd(DEPLOY_PATH):
        if not exists('venv'):
            run('virtualenv venv')
        run_with_venv('pip install -r requirements.txt')


def run_with_venv(cmd):
    with cd(DEPLOY_PATH):
        run('source venv/bin/activate && {}'.format(cmd))


def setup_db():
    with cd(DEPLOY_PATH):
        run_with_venv('honcho run -e conf/stage.env python manage.py syncdb')


def restart(redefine='f'):
    as_ubuntu()
    with cd(DEPLOY_PATH):
        env = 'conf/stage.env'
        put(local_path=env, remote_path=env)
        context = {'VENV': VENV_PATH, 'PORT': os.environ['PORT']}
        upload_template(filename='deploy/templates/Procfile.stage',
          destination='Procfile.stage', backup=False, context=context)
        upload_template(filename='deploy/templates/gunicorn.conf',
          destination='gunicorn.conf', backup=False,)

    if redefine != 'f':
        as_root()
        run_with_venv('honcho export --user {} --app {} --shell /bin/bash -e {} -f Procfile.stage upstart /etc/init'.format(USERNAME, PROJECT_NAME, env))
        setup_nginx()

    as_ubuntu()
    if not run_succeeds('sudo restart {}-web'.format(PROJECT_NAME)):
        run('sudo start {}-web'.format(PROJECT_NAME))
    if not run_succeeds('sudo service nginx restart'):
        run('sudo service nginx start')


def run_succeeds(cmd):
  with settings(warn_only=True):
      return run(cmd).return_code == 0


def deploy(redefine='f'):
    as_ubuntu()
    install_repo_dependancies()
    with cd(DEPLOY_PATH):
        run('git pull')
        run_with_venv('honcho run -e conf/stage.env python manage.py collectstatic')
    restart(redefine)


def logs():
    run('tail -f /var/log/shev/*.log /var/log/nginx/*.log')
