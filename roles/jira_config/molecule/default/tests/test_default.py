import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/var/atlassian/application-data/jira/dbconfig.xml')
    assert f.exists
    assert f.user == 'jira'
    assert f.contains("<driver-class>org.postgresql.Driver</driver-class>")
    assert f.contains("<username>atljira</username>")
    assert f.contains("<pool-min-size>20</pool-min-size>")
