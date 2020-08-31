import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service_file(host):
    systemd_prefix = "/lib" if host.system_info.distribution == "ubuntu" else "/usr/lib"
    f = host.file(systemd_prefix+'/systemd/system/synchrony.service')
    assert f.contains("^ExecStart=/opt/atlassian/bin/start-synchrony$")
    assert f.contains("^EnvironmentFile=/etc/atl$")
    assert f.contains("^EnvironmentFile=/etc/atl.synchrony$")
    assert f.contains("^WorkingDirectory=/opt/atlassian/confluence/current/logs/$")
