import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_atl_startup_restart(host):
    f = host.file('/tmp/ansible-vars.yml')
    # value should appear as YAML boolean false (i.e., boolean true or string 'false' will fail)
    assert f.contains(r'^\s*atl_startup_restart: false$')
