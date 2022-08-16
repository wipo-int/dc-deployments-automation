import os
from six.moves import urllib
import json

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_version_downloaded(host):
    verfile = host.file('/media/atl/confluence/shared-home/confluence.version')
    assert verfile.exists
    assert verfile.content.decode("UTF-8").strip() == "7.20.0-CONFSERVER-63193-m01"

def test_symlink_created(host):
    target = host.file('/opt/atlassian/confluence/current')
    assert target.exists
    assert target.is_symlink

def test_unpacked(host):
    verfile = host.file('/opt/atlassian/confluence/current/bin/catalina.sh')
    assert verfile.exists
