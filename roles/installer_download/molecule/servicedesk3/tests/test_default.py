import os
import urllib.request

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_version_is_correct(host):
    verfile = host.file('/media/atl/jira/shared/jira-servicedesk.version')
    assert verfile.exists

    assert verfile.content.decode("UTF-8").strip() == "3.0.2"

def test_is_downloaded(host):
    installer = host.file('/opt/atlassian/tmp/jira-software.7.0.11.tar.gz')
    assert installer.exists
    assert installer.user == 'root'

def test_is_unpacked(host):
    installer = host.file('/opt/atlassian/jira-servicedesk/3.0.2')
    assert installer.exists
    assert installer.is_directory
    assert installer.user == 'jira'
    assert installer.mode == 0o0755

def test_sd_is_downloaded(host):
    installer = host.file('/opt/atlassian/tmp/jira-servicedesk.3.0.2.obr')
    assert installer.exists
    assert installer.user == 'root'

def test_is_unpacked(host):
    installer = host.file('/media/atl/jira/shared/plugins/installed-plugins/jira-servicedesk-application-3.0.2.jar')
    assert installer.exists
    assert installer.user == 'jira'
    assert installer.mode == 0o0750
