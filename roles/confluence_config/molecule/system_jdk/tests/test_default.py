import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_seraph_file(host):
    f = host.file('/opt/atlassian/confluence/current/confluence/WEB-INF/classes/seraph-config.xml')
    assert f.exists
    assert f.contains('<param-value>COOKIEAGE</param-value>')

@pytest.mark.parametrize('font', [
    '/usr/lib/jvm/java/lib/fonts/fallback/NotoSansJavanese-Regular.ttf'
])
def test_fonts_installed_and_linked(host, font):
    f = host.file(font)
    assert f.exists
