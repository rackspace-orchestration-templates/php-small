from fabric.api import env, run, hide, task
from envassert import detect, file, port, process, service, user
from hot.utils.test import get_artifacts
import socket

@task
def check():
  env.platform_family = detect.detect()

  assert port.is_listening(80), 'port 80/nginx is not listening'

  if (env.platform_family == "rhel"):
    assert process.is_up('nginx'), 'nginx is not running'
    assert process.is_up('php-fpm'), 'php-fpm is not running'
    assert service.is_enabled('nginx'), 'nginx is not enabled'
    assert service.is_enabled('php-fpm'), 'php-fpm is not enabled'
  elif (env.platform_family == 'debian'): 
    assert process.is_up('nginx'), 'nginx is not running' 
    assert process.is_up('php5-fpm'), 'php-fpm is not running'
    assert service.is_enabled('nginx'), 'nginx is not enabled'
    assert service.is_enabled('php5-fpm'), 'php-fpm is not enabled' 
  if ("secondary" not in socket.gethostname()):
    assert service.is_enabled('lsyncd'), 'lsyncd is not enabled'

@task
def artifacts():
  env.platform_family = detect.detect()
  get_artifacts()
