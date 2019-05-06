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

def test_server_file(host):
    f = host.file('/opt/atlassian/jira-software/current/conf/server.xml')
    assert f.exists
    assert f.contains('Connector port="8080"')
    assert f.contains('Server port="8005"')
    assert f.contains('<Context path=""')
    assert f.contains('maxThreads="200"')
    assert f.contains('minSpareThreads="10"')
    assert f.contains('connectionTimeout="20000"')
    assert f.contains('enableLookups="false"')
    assert f.contains('protocol="HTTP/1.1"')
    assert f.contains('redirectPort=""')
    assert f.contains('acceptCount="10"')
    assert f.contains('secure="false"')
    assert f.contains('scheme="http"')
    assert not f.contains('proxyName=')
    assert not f.contains('proxyPort=')
