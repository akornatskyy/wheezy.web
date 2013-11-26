from fabric.api import cd
from fabric.api import env
from fabric.api import lcd
from fabric.api import local
from fabric.api import put
from fabric.api import run
from fabric.api import sudo


# apt-get install sudo
# #adduser <username> sudo
# echo '<username> ALL=(ALL:ALL) NOPASSWD: ALL' >> /etc/sudoers
# env/bin/fab -H <host> -u <username> <command>

NAME = 'mysite'
ETC_PATH = '/usr/local/etc/' + NAME
LIB_PATH = '/usr/local/lib/' + NAME
USER = env['user']


def update():
    name = get_name()
    filename = name + '.tar.gz'
    with lcd('dist'), cd(LIB_PATH):
        put(filename, env.cwd)
        run('rm -rf ' + name)
        run('tar xzf ' + filename)
        run('rm ' + filename)
        run('rm -f current ')
        run('ln -s %s current' % name)
        with cd('current'):
            run('make install')
            sudo('cp content/maintenance.html /usr/share/nginx/www')


def config():
    with cd('%s/etc/' % CURRENT_PATH):
        run('cp *.conf *.ini %s' % ETC_PATH)
    with cd('/etc/nginx/sites-available'):
        sudo('rm -f %s.conf' % NAME)
        sudo('ln -s %s/nginx.conf %s.conf' % (ETC_PATH, NAME))
    with cd('/etc/nginx/sites-enabled'):
        sudo('rm -f %s.conf' % NAME)
        sudo('ln -s /etc/nginx/sites-available/%s.conf' % NAME)
    sudo('rm -f /etc/nginx/sites-enabled/default')
    sudo('/etc/init.d/nginx restart')
    with cd('/etc/uwsgi/apps-available'):
        sudo('rm -f %s.ini' % NAME)
        sudo('ln -s %s/config.ini %s.ini' % (ETC_PATH, NAME))
    with cd('/etc/uwsgi/apps-enabled'):
        sudo('rm -f %s.ini' % NAME)
        sudo('ln -s /etc/uwsgi/apps-available/%s.ini' % NAME)


def install():
    sudo('mkdir -p %s %s' % (ETC_PATH, LIB_PATH))
    sudo('chown -R %s %s %s' % (USER, ETC_PATH, LIB_PATH))
    update()


def uninstall():
    sudo('rm -rf ' + LIB_PATH)


def purge():
    uninstall()
    sudo('rm -rf ' + ETC_PATH)


def debian():
	sudo('apt-get update')
	sudo('apt-get install --no-install-recommends -y build-essential '
		 'python2.7 python2.7-dev python-setuptools '
		 'python-virtualenv gettext libgmp3-dev '
         'nginx-full uwsgi uwsgi-plugin-python')
	sudo('apt-get clean')


def start():
    sudo('/etc/init.d/uwsgi start')


def stop():
    sudo('/etc/init.d/uwsgi stop')


def restart():
    sudo('/etc/init.d/uwsgi restart')


# region: internal details
#
# Allow members of group sudo to execute any command without password
# %sudo   ALL=(ALL:ALL) NOPASSWD: ALL

def get_name():
    revision = local("hg head --template '{rev}'", capture=True)
    assert int(revision)
    name = local('env/bin/python setup.py --fullname', capture=True)
    return name + '.' + revision


CURRENT_PATH = LIB_PATH + '/current'


env.colorize_errors = True
env.key_filename = '~/.ssh/id_rsa'
env.ssh_config_path = '~/.ssh/config'
env.use_ssh_config = True
