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

def test_postgresql_version(host):
    pg_dump_version_output = host.check_output('pg_dump --version')
    assert '(PostgreSQL) 9.6' in pg_dump_version_output

def test_shared_home_owner(host):
    for root, dirs, files in os.walk('/media/atl/jira/shared'):
        for fileName in files + dirs:
            assert host.file(fileName).user == 'jira'
            assert host.file(fileName).group == 'jira'