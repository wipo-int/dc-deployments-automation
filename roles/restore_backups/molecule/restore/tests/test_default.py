import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('exe', [
    '/usr/bin/pg_dump',
    '/usr/bin/pg_restore',
    '/usr/bin/psql'
])
def test_postgresql_amazon_linux_extras_exes(host, exe):
    assert host.file(exe).exists
