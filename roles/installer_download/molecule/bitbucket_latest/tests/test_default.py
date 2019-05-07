import os
import urllib.request
import json

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_version_downloaded(host):
    verfile = host.file('/media/atl/stash/shared/bitbucket.version')
    assert verfile.exists

def test_symlink_created(host):
    target = host.file('/opt/atlassian/bitbucket/current')
    assert target.exists
    assert target.is_symlink

def test_unpacked(host):
    verfile = host.file('/opt/atlassian/bitbucket/current/bin/start-bitbucket.sh')
    assert verfile.exists

def test_version_file_is_latest(host):
    verfile = host.file('/media/atl/stash/shared/bitbucket.version')
    assert verfile.exists

    upstream_fd = urllib.request.urlopen("https://marketplace.atlassian.com/rest/2/applications/bitbucket/versions/latest")
    upstream_json = json.load(upstream_fd)
    upstream = upstream_json['version']

    assert verfile.content.decode("UTF-8").strip() == upstream.strip()

def test_latest_is_downloaded(host):
    upstream_fd = urllib.request.urlopen("https://marketplace.atlassian.com/rest/2/applications/bitbucket/versions/latest")
    upstream_json = json.load(upstream_fd)
    upstream = upstream_json['version']

    installer = host.file('/opt/atlassian/tmp/bitbucket.'+upstream+'.bin')
    assert installer.exists
    assert installer.user == 'root'
