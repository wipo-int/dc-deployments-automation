import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service_file(host):
    f = host.file('/etc/systemd/system/bitbucket.service')
    assert f.contains("^ExecStart=/opt/atlassian/bitbucket/current/bin/start-bitbucket.sh -fg --no-search$")
    assert f.contains("^UMask=0027$")
    assert f.contains("^LimitNOFILE=4096$")
    assert f.contains("^Environment=BITBUCKET_HOME=/media/atl/bitbucket$")
