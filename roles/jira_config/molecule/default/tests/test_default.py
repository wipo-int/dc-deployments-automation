import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_varfile(host):
    f = host.file('/opt/atlassian/tmp/jira.varfile')
    assert f.exists
    assert f.is_file
    assert f.contains("app.jiraHome=/var/atlassian/application-data/jira")
    assert f.contains("existingInstallationDir=/opt/atlassian/jira")
    assert f.contains("sys.installationDir=/opt/atlassian/jira")
