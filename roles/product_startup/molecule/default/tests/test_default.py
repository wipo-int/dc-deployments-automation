import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service_file(host):
    systemd_prefix = "/lib" if host.system_info.distribution == "ubuntu" else "/usr/lib"
    f = host.file(systemd_prefix+'/systemd/system/jira-software.service')
    assert f.contains("^ExecStart=/opt/atlassian/jira-software/current/bin/start-jira.sh -fg >/opt/atlassian/jira-software/current/logs/catalina.out 2>&1$")
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o0640


def test_atl_startup_restart(host):
    f = host.file('/tmp/ansible-vars.yml')
    # value should appear as YAML boolean true (i.e., string 'true' will fail)
    assert f.contains(r'^\s*atl_startup_restart: true$')
