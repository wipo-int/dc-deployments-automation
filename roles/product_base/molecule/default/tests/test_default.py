import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_user_created(host):
    user = host.user('testuser')
    assert user.exists


@pytest.mark.parametrize('target', [
  '/opt/atlassian/product',
  '/opt/atlassian/temp'
])
def test_dirs_created(host, target):
    d = host.file(target)
    assert d.exists
    assert d.is_directory
    assert d.user == 'testuser'
