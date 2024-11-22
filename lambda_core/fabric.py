import os

# CONNECT GIT REPO

# ssh-keygen -b 2048 -t rsa -f /home/ubuntu/.ssh/id_rsa -q -N ""
# cat ~/.ssh/id_rsa.pub
# ssh -T git@bitbucket.org

# CONFIG TIMEZONE/LOCALE

# sudo dpkg-reconfigure tzdata
# sudo dpkg-reconfigure locales

# SSL CONFIG

# sudo certbot --nginx -d <DNS>
# sudo certbot renew # RENEW
# sudo certbot renew --dry-run # CHECK


def setup(c, config):
    # c.sudo('yum -y update')
    c.sudo('apt-get update -y')
    # c.sudo('yum install -y python3')
    # c.sudo('yum install epel-release')
    c.sudo('apt-get install -y python3 python3-pip python3-dev python3-virtualenv')
    c.sudo('apt-get install language-pack-es-base')
    # cmd = 'amazon-linux-extras install -y nginx%s' % NGINX_VERSION
    # c.sudo(cmd)
    c.sudo('sudo apt-get install -y nginx')
    c.run('pip3 install --upgrade pip')
    c.run('pip3 install virtualenv')

    nginx_conf = '/etc/nginx/nginx.conf'

    cmd = 'cp %s /etc/nginx/nginx.conf.bak' % nginx_conf
    c.sudo(cmd)

    c.put(os.path.join(config['LAMBDA_EXTENSIONS_DIR'], 'nginx.conf'), config['BASE_DIR'])

    cmd = 'mv %s %s' % (os.path.join(config['BASE_DIR'], 'nginx.conf'), nginx_conf)
    c.sudo(cmd)
    c.sudo('mkdir /etc/nginx/sites-enabled', hide=True, warn=True)

    nginx = c.sudo('nginx -t')
    assert nginx.ok

    c.sudo('systemctl start nginx')
    c.sudo('systemctl enable nginx.service')
    c.sudo('service nginx status')

    # SSL Config

    c.sudo('add-apt-repository ppa:certbot/certbot -y')
    c.sudo('apt-get install -y python-certbot-nginx')


def deploy(c, config):

    """
    ----------------------------
    INSTALL DEPENDENCIES
    ----------------------------
    """

    c.sudo('apt-get update -y')
    cmd = 'apt-get install -y %s' % ' '.join(config['PACKAGES'])
    c.sudo(cmd)

    """
    ----------------------------
    CREATE DIRECTORIES
    ----------------------------
    """

    dirs = [
        config['APP_DIR'],
        config['APP_LOGS_DIR'],
        config['APP_CONF_DIR'],
    ]

    for d in dirs:
        cmd = "test -d %s" % d
        if c.run(cmd, warn=True).failed:
            cmd = 'mkdir %s' % d
            c.run(cmd)

    """
    ----------------------------
    CREATE VIRTUALENV
    ----------------------------
    """
    cmd = "test -d %s" % config['APP_VENV_DIR']
    if c.run(cmd, warn=True).failed:
        cmd = 'virtualenv %s --python=python3' % config['APP_VENV_DIR']
        c.run(cmd)

    """
    ----------------------------
    SYNC REPOS
    ----------------------------
    """

    if c.run("test -d {}".format(config['APP_HTDOCS_DIR']), warn=True).failed:
        c.run("git clone -b {} {} {}".format(config['BRANCH'], config['REPOSITORY_URL'], config['APP_HTDOCS_DIR']))
    else:
        c.run("cd {} && git pull origin {}".format(config['APP_HTDOCS_DIR'], config['BRANCH']))

    """
    ----------------------------
     SET ENV VARS
    ----------------------------
    """

    c.put(os.path.join(config['LAMBDA_EXTENSIONS_DIR'], 'env'), os.path.join(config['APP_DIR'], '.env'))

    cmd = 'cat %s |  sed -e "s/^export //" > %s' % (
        os.path.join(config['APP_DIR'], '.env'),
        os.path.join(config['APP_DIR'], '.env.gunicorn')
    )
    c.sudo(cmd)

    """
    ----------------------------
    INSTALL PROJECT DEPENDENCIES
    ----------------------------
    """

    cmd = 'source %s && pip3 install -r %s' % (
        os.path.join(config['APP_VENV_DIR'], 'bin/activate'),
        os.path.join(config['APP_HTDOCS_DIR'], 'requirements.txt'),
    )
    c.run(cmd)

    """
    ----------------------------
    RUN PROJECT SCRIPTS
    ----------------------------
    """

    for dj_command in config['DJANGO_COMMANDS']:
        cmd = 'source %s' % os.path.join(config['APP_VENV_DIR'], 'bin/activate')
        cmd = '%s && source %s' % (cmd, os.path.join(config['APP_DIR'], '.env'))
        cmd = '%s && python3 %s %s' % (cmd, os.path.join(config['APP_HTDOCS_DIR'], 'manage.py'), dj_command)
        print('python3 manage.py %s' % dj_command)
        c.run(cmd)

    """
    ----------------------------
    CONFIG VHOST SERVER
    ----------------------------
    """

    if config['SSL_SETUP']:
        vhost_file = 'nginx.vhost-setup.conf'
    else:
        vhost_file = 'nginx.vhost.conf'

    c.put(os.path.join(config['LAMBDA_EXTENSIONS_DIR'], vhost_file), config['APP_DIR'])

    cmd = 'mv %s %s' % (os.path.join(config['APP_DIR'], vhost_file), config['NGINX_VHOST_FILE'])
    c.sudo(cmd)

    c.put(os.path.join(config['LAMBDA_EXTENSIONS_DIR'], 'gunicorn.service'), config['APP_DIR'])

    cmd = 'mv %s %s' % (
        os.path.join(config['APP_DIR'], 'gunicorn.service'),
        config['GUNICORN_SERVICE']
    )
    c.sudo(cmd)

    c.sudo('systemctl daemon-reload')

    cmd = 'chown -R ubuntu:www-data %s' % config['APP_DIR']
    c.sudo(cmd)

    """
    ----------------------------
    START NGINX
    ----------------------------
    """

    nginx = c.sudo('nginx -t')
    assert nginx.ok

    c.sudo('systemctl restart nginx')
    c.sudo('systemctl status nginx')

    if c.run('systemctl is-active nginx', warn=True).failed:
        c.sudo('systemctl enable nginx')

    """
    ----------------------------
    START GUNICORN
    ----------------------------
    """

    gunicorn_service = '%s.service' % config['APP_NAME']

    cmd = 'systemctl restart %s' % gunicorn_service
    c.sudo(cmd)

    cmd = 'systemctl status %s' % gunicorn_service
    c.sudo(cmd)

    cmd = 'systemctl is-active %s' % gunicorn_service

    if c.run(cmd, warn=True).failed:
        cmd = 'systemctl enable %s' % gunicorn_service
        c.sudo(cmd)


