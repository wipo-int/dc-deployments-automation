## Prerequisites

You should have the following software installed:
* Python; 3.x by preference, but 2.7 works.
 * You may also need the Python development packages depending on how it’s installed.
* Python Virtualenv
* Docker
* Cloudtoken

All other requirements will be installed under Virtualenv.

## Step 1: Install and test the playbooks locally

### Step 1.1: Get the repo

    git clone git@bitbucket.org:atlassian/dc-deployments-automation.git

### Step 1.2: Install Ansible

To ensure compatibility we specify a specific Ansible version; currently 2.7.10
(some older versions had issues with RDS). We do this by creating a virtualenv
and installing a pinned version:

    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install ansible==2.7.10

### Step 1.3: Install Molecule for testing

Molecule is a testing framework for Ansible. We use this to test the
functionality of individual and groups of roles, and to ensure cross-platform
compatibility (currently Amazon Linux 2 and Ubuntu LTS).

    pip install molecule docker

### Step 1.4: Run some tests against a role

We’re going to check that the role that downloads the products works for both
Jira Core and Confluence, on boths supported Linux distributions. So run the
following:

    cd roles/installer_download/
    molecule test -s jira_version_latest
    molecule test -s servicedesk3

This starts Docker containers for each distro, runs the playbook in
molecule/<scenario>/playbook.yml and runs testinfra tests against the
results. In practice, when developing roles is better to run molecule create -s
<scenario> and then molecule converge -s <scenario> repeatedly do iteratively
develop.

## Step 2: Test out the playbook with AWS Cloudformation

### Step 2.1: Get the updated Cloudformation template

There is a slightly modified version for the official Atlassian Jira Quickstart
that uses the baseline Amazon Linux 2 AMI and Ansible. The branch containing the
changes is in the Atlassian Github fork of the upstream repository, in the
branch DCD-221-jira-dc-linux2-ansible-rework.

### Step 2.2: Install taskcat

Taskcat is a tool for testing Cloudformation templates. It is generally the
simplest method of getting a template up and running from local changes.

Assuming you’re still in the virtualenv, install it with:

    pip install taskcat

You may also need to create the file ~/.aws/taskcat_global_override.json and set
the KeyPair parameter to access the deployed EC2 instances. See the taskcat docs
for details.

### Step 2.3: Configure and deploy your Jira instance with Cloudformation and Ansible

You should probably modify some of the parameters, as we want to do some manual testing:

* Edit ci/taskcat.yml and update the region (last line). You will need to select
  a region that does not have another quickstart running it.
* Edit ci/quickstart-jira-dc-params.json and modify the following:
 * Set AssociatePublicIpAddress to true.
 * Set CidrBlock and AccessCIDR to 0.0.0.0/0.
 * If you want to test any other deployment parameters with the Ansible playbook
   this is where to modify them.

To deploy the modified Cloudformation template, refresh your AWS keys with
cloudtoken, and run:

    taskcat -c ci/taskcat -n

*NOTE*: The -n flag disables teardown of the instance, so you must do this yourself via
the Cloudformation console.

### Step 2.4: Configure and verify the installed Jira instance

The output of the Cloudformation template included the URL of the deployed
load-balancer. Access this to finalise the configuration and install a license.

You may also want to use the EC2 console to enable clustering after
configuration, and create and destroy cluster nodes.

### Step 2.5: Accessing logs, and looking around inside the deployed node

To manually inspect the deployed Jira nodes, do the following:

* Fetch the bastion public IP address from either template output, or the EC2
  console.
* Login to it with ssh ec2-user@<ip-address>.
* Get the node internal IP address from the EC2 console
* Login to the node with ssh <ip-address>.
* Change to root with sudo -i

Some notable files and locations:

* The output cfn-init is under /var/log/cfn-init.log .
* The output of the Ansible playbook is in there, and also
  /var/log/ansible-bootstrap.log.
* The Jira installation is under /opt/atlassian/jira/<version>and symlinked to
  /opt/atlassian/jira/current.
* The systemd service is configured in /etc/systemd/system/jira.service. Its
  stdout can be viewed with systemctl status jira.service and journalctl -u
  jira.service.
* Other Tomcat logs can be located under /opt/atlassian/jira/current/logs/...
