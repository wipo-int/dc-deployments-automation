import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_config_file(host):
    f = host.file('/media/atl/bitbucket/shared/bitbucket.properties')
    assert f.exists

    assert not f.contains("plugin.search.elasticsearch.username")
    assert not f.contains("plugin.search.elasticsearch.password")
    assert f.contains("plugin.search.elasticsearch.aws.region=us-east-2")
