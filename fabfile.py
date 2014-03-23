import os
from os.path import expanduser

from fabric.api import cd, env, hide, run, put, settings, local, abort, sudo, prompt, open_shell
from fabric.network import disconnect_all


PROJECT_NAME = 'shev'
USERNAME = 'ubuntu'
USER_DIR = '/usr/{}'.format(USERNAME)
DEPLOY_PATH = '{}/{}'.format(USER_DIR, PROJECT_NAME)

env.hosts = os.environ['HOST']
env.password = ''
env.use_ssh_config = True


def setup():
    env.user = 'root'
    create_user(USERNAME)
    setup_ssh()
    install_dependancies()
    env.user = USERNAME
    disconnect_all()
    # setup_user_env()
    clone_repo(repo=os.environ['REPO'], destination=DEPLOY_PATH)
    with cd(DEPLOY_PATH):
        run('virtualenv venv')
        run('source venv/bin/activate && pip install -r requirements.txt')


def create_user(username):
    home_dir = '/usr/{}'.format(username)
    ensure_dir(home_dir)
    with settings(warn_only=True):
        user_present = run('id {u}'.format(u=username)).return_code == 0
        if user_present is False:
            run('useradd {} --home {} --shell /bin/bash'.format(username, home_dir))
    run('chown {} {}'.format(username, home_dir))
    run('adduser {} sudo'.format(username))


def ensure_dir(path):
    run('mkdir -p {}'.format(path))


def setup_ssh():
    """
    Ensures the correct private and public keys are on local machine before
    adding public part to authorized_keys on remote host
    """
    with settings(warn_only=True):
        have_key = run('ls ~/.ssh/id_rsa').return_code == 0
        if have_key is False:
            run('ssh-keygen')
    put(local_path='./deploy/templates/sshd_config.txt', remote_path='/etc/ssh/sshd_config', use_sudo=True)
    key_name = 'nhs_shev'
    pem_key = expanduser('~/.ssh/{}.pem'.format(key_name))
    pub_key = expanduser('~/.ssh/{}.pub'.format(key_name))
    ssh = '{}/.ssh'.format(USER_DIR)
    ensure_dir(ssh)
    authorized_keys = '{}/.ssh/authorized_keys'.format(USER_DIR)
    put(local_path=pub_key, remote_path=authorized_keys)
    run('chmod 600 {}'.format(authorized_keys))
    chown(USERNAME, ssh)

    # set local ssh config
    local_config = 'Host {}\nUser {}\nIdentityFile {}'.format(env.host_string, USERNAME, pem_key)
    config_filename = expanduser('~/.ssh/config')
    print "You'll want to put the following in your file '{}' and then add {} to your ssh-agent:\n\n{}\n\n".format(config_filename, pem_key, local_config)
    prompt("Yep, I've got it thanks!")


def chown(username, file_or_dir):
    run('chown -R {} {}'.format(username, file_or_dir))


def setup_user_env():
    put('deploy/templates/bashrc', '~/.bashrc')
    put('deploy/templates/profile', '~/.profile')


def clone_repo(repo, destination):
    run('mkdir -p {}'.format(destination))
    with settings(warn_only=True):
        not_present = run('ls {}/.git'.format(destination)).return_code != 0
    if not_present:
        run('git clone {} {}'.format(repo, destination))


def install_dependancies():
    run('apt-get install -y python-pip git')
    run('pip install virtualenv')
