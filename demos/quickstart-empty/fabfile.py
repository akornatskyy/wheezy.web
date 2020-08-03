from fabric.api import cd, env, hide, lcd, local, put, run, sudo

# apt-get install sudo
# #adduser <username> sudo
# echo '<username> ALL=(ALL:ALL) NOPASSWD: ALL' >> /etc/sudoers
# env/bin/fab -H <host> -u <username> <command>

NAME = "mysite"
ETC_PATH = "/usr/local/etc/" + NAME
LIB_PATH = "/usr/local/lib/" + NAME
USER = env["user"]


def update():
    name = get_name()
    filename = name + ".tar.gz"
    with lcd("dist"), cd(LIB_PATH):
        put(filename, env.cwd)
        run("rm -rf " + name)
        run("tar xzf " + filename)
        run("rm " + filename)
        with cd(name):
            run("make install")
            sudo("cp content/maintenance.html /usr/share/nginx/www")
        run("rm -f current && ln -s %s current" % name)


def config():
    with cd("%s/etc/" % CURRENT_PATH):
        run("cp *.conf *.ini %s" % ETC_PATH)
    # sysctl
    with cd("%s/etc/" % CURRENT_PATH):
        run("cp *.conf *.ini %s" % ETC_PATH)
    with cd("/etc/sysctl.d"):
        sudo("rm -f boc.conf")
        sudo("ln -s %s/sysctl.conf boc.conf" % ETC_PATH)
        sudo("sysctl -f boc.conf")
    # nginx
    with cd("/etc/nginx/sites-available"):
        sudo("rm -f %s.conf" % NAME)
        sudo("ln -s %s/nginx.conf %s.conf" % (ETC_PATH, NAME))
    with cd("/etc/nginx/sites-enabled"):
        sudo("rm -f %s.conf" % NAME)
        sudo("ln -s /etc/nginx/sites-available/%s.conf" % NAME)
    sudo("rm -f /etc/nginx/sites-enabled/default")
    sudo("/usr/sbin/nginx -s quit && sleep 5")
    sudo("/etc/init.d/uwsgi stop")
    sudo("/etc/init.d/nginx start")
    # memcached
    sudo("/etc/init.d/memcached stop")
    with cd("/etc"):
        sudo("rm -f memcached.conf")
        sudo("ln -s %s/memcached.conf" % ETC_PATH)
    sudo("/etc/init.d/memcached start")
    # uwsgi
    with cd("/etc/uwsgi/apps-available"):
        sudo("rm -f %s.ini" % NAME)
        sudo("ln -s %s/config.ini %s.ini" % (ETC_PATH, NAME))
    with cd("/etc/uwsgi/apps-enabled"):
        sudo("rm -f %s.ini" % NAME)
        sudo("ln -s /etc/uwsgi/apps-available/%s.ini" % NAME)
    sudo("/etc/init.d/uwsgi start")


def install():
    sudo("mkdir -p %s %s" % (ETC_PATH, LIB_PATH))
    sudo("chown -R %s %s %s" % (USER, ETC_PATH, LIB_PATH))
    update()


def uninstall():
    sudo("rm -rf " + LIB_PATH)


def purge():
    uninstall()
    sudo("rm -rf " + ETC_PATH)


def reload():
    sudo("/etc/init.d/uwsgi reload")


def start():
    sudo("/etc/init.d/memcached start")
    sudo("/etc/init.d/uwsgi start")


def stop():
    sudo("/usr/sbin/nginx -s quit && sleep 5")
    sudo("/etc/init.d/nginx stop")
    sudo("/etc/init.d/uwsgi stop")
    sudo("/etc/init.d/nginx start")
    sudo("/etc/init.d/memcached stop")


def restart():
    stop()
    start()


def flush_cache():
    sudo(
        "echo flush_all | socat unix-connect:/var/tmp/memcached-%s.sock -"
        % NAME
    )


def cache_stats():
    with hide("output", "running"):
        stats = sudo(
            "echo stats | socat unix-connect:"
            "/var/tmp/memcached-%s.sock -" % NAME
        )
        items = dict(
            (r[1], r[2].strip())
            for r in [i.split(" ") for i in stats.split("\n")[:-1]]
        )
        c = float(items["cmd_get"])
        h = c and 100.0 * float(items["get_hits"]) / c or 0.0
        print(
            "Cache: %.2f%% hit rate, %.2fM gets, %.2fG read, %.2f days"
            % (
                h,
                c / 1e6,
                float(items["bytes_read"]) / pow(1024, 3),
                float(items["uptime"]) / 86400.0,
            )
        )


def debian():
    sudo("apt-get -dqq update")
    sudo(
        "apt-get --no-install-recommends -yq install build-essential "
        "ntpdate python2.7 python2.7-dev python-setuptools "
        "python-virtualenv gettext libgmp3-dev "
        "nginx-full uwsgi uwsgi-plugin-python "
        "libmemcached-dev memcached mailutils socat"
    )
    sudo("/etc/init.d/uwsgi start")
    sudo("/etc/init.d/nginx start")
    sudo("/etc/init.d/memcached start")
    sudo("apt-get -q clean")
    sudo("ntpdate pool.ntp.org")


def os_upgrade():
    sudo("apt-get -dqq update")
    sudo("apt-get -yq upgrade")
    sudo("apt-get -q clean; apt-get -q autoclean; apt-get -q autoremove")


# region: internal details
#
# Allow members of group sudo to execute any command without password
# %sudo   ALL=(ALL:ALL) NOPASSWD: ALL


def get_name():
    revision = local("hg head --template '{rev}'", capture=True)
    assert int(revision) >= 0
    name = local("env/bin/python setup.py --fullname", capture=True)
    return name + "." + revision


CURRENT_PATH = LIB_PATH + "/current"


env.colorize_errors = True
env.key_filename = "~/.ssh/id_rsa"
env.ssh_config_path = "~/.ssh/config"
env.use_ssh_config = True
