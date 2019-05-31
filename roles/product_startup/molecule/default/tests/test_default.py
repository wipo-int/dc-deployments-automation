import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service_file(host):
    f = host.file('/etc/systemd/system/jira-software.service')
    assert f.contains("^ExecStart=/opt/atlassian/jira-software/current/bin/start-jira.sh -fg$")
