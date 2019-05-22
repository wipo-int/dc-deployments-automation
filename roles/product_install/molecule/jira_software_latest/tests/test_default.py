import os
import urllib.request

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_version_downloaded(host):
    verfile = host.file('/media/atl/jira/shared/jira-software.version')
    assert verfile.exists

def test_symlink_created(host):
    target = host.file('/opt/atlassian/jira-software/current')
    assert target.exists
    assert target.is_symlink

def test_unpacked(host):
    verfile = host.file('/opt/atlassian/jira-software/current/bin/catalina.sh')
    assert verfile.exists

def test_version_file_is_latest(host):
    verfile = host.file('/media/atl/jira/shared/jira-software.version')
    assert verfile.exists

    upstream_fd = urllib.request.urlopen("https://s3.amazonaws.com/atlassian-software/releases/jira-software/latest")
    upstream = upstream_fd.read()

    assert verfile.content.decode("UTF-8").strip() == upstream.decode("UTF-8").strip()

def test_latest_is_downloaded(host):
    upstream_fd = urllib.request.urlopen("https://s3.amazonaws.com/atlassian-software/releases/jira-software/latest")
    upstream = upstream_fd.read().decode("UTF-8").strip()

    installer = host.file('/opt/atlassian/tmp/jira-software.'+upstream+'.bin')
    assert installer.exists
    assert installer.user == 'root'
