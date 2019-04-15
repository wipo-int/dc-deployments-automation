import os
import urllib.request

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_version_downloaded(host):
    verfile = host.file('/media/atl/jira/shared/jira-software.version')
    assert verfile.exists


def test_version_is_latest(host):
    verfile = host.file('/media/atl/jira/shared/jira-software.version')
    assert verfile.exists

    assert verfile.content.decode("UTF-8").strip() == "7.13.2"

