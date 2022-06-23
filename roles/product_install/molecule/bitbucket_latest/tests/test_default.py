import os
from six.moves import urllib
import json

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_version_downloaded(host):
    verfile = host.file('/media/atl/bitbucket/shared/bitbucket.version')
    assert verfile.exists

def test_symlink_created(host):
    target = host.file('/opt/atlassian/bitbucket/current')
    assert target.exists
    assert target.is_symlink

def test_unpacked(host):
    verfile = host.file('/opt/atlassian/bitbucket/current/bin/start-bitbucket.sh')
    assert verfile.exists

def test_version_file_is_latest(host):
    verfile = host.file('/media/atl/bitbucket/shared/bitbucket.version')
    assert verfile.exists

    upstream = get_version("https://marketplace.atlassian.com/rest/2/products/key/bitbucket/versions")

    assert verfile.content.decode("UTF-8").strip() == upstream.strip()

def test_latest_is_downloaded(host):
    upstream = get_version("https://marketplace.atlassian.com/rest/2/products/key/bitbucket/versions")

    installer = host.file('/media/atl/downloads/bitbucket.' + upstream + '-x64.bin')
    assert installer.exists
    assert installer.user == 'root'

def test_completed_lockfile(host):
    upstream = get_version("https://marketplace.atlassian.com/rest/2/products/key/bitbucket/versions")

    lockfile = host.file('/media/atl/downloads/bitbucket.' + upstream + '-x64.bin_completed')
    assert lockfile.exists
    assert lockfile.user == 'root'

def get_version(url):
    if url.lower().startswith('http'):
        upstream_req = urllib.request.Request(url)
    else:
        raise ValueError from None
    with urllib.request.urlopen(upstream_req) as upstream_response: #nosec
        upstream_json = json.load(upstream_response)
        upstream = upstream_json['_embedded']['versions'][0]['name']
    return upstream
