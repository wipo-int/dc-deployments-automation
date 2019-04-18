import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_dbconfig_file(host):
    f = host.file('/var/atlassian/application-data/jira/dbconfig.xml')
    assert f.exists
    assert f.user == 'jira'
    assert f.contains("<driver-class>org.postgresql.Driver</driver-class>")
    assert f.contains("<username>atljira</username>")
    assert f.contains("<pool-min-size>20</pool-min-size>")

def test_setenv_file(host):
    f = host.file('/opt/atlassian/jira-software/current/bin/setenv.sh')
    assert f.exists
    assert f.contains('JVM_MINIMUM_MEMORY="PLACEHOLDER"')
    assert f.contains('JVM_MAXIMUM_MEMORY="PLACEHOLDER"')

def test_cluster_file(host):
    f = host.file('/var/atlassian/application-data/jira/cluster.properties')
    assert f.exists
    assert f.contains('jira.node.id = FAKEID')
    assert f.contains('jira.shared.home = /media/atl/jira/shared')
