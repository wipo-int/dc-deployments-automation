
# Atlassian Data-Center Installation Automation

## Introduction

This repository is a suite of Ansible roles, playbooks and support scripts to
automate the installation and maintenance of Atlassian Data Center products in
cloud environments.

## Usage

### Cloud DC-node deployment playbooks

The usual scenario for usage as part of a cloud deployment is to invoke the
script as part of post-creation actions invoked while a new product node is
being brought up. In the case of AWS, this would usually be done by
[cfn-init][cfn-init]/[user-data][ec2-user-data]. For example, the [Jira
quickstart template][jira-cfn-tmpl] creates a per-node [launch
configuration][ec2-launch-config] that fetches this repository and runs the
appropriate AWS/product playbook, which invokes the appropriate roles.

In practice, the Ansible roles require some information about the infrastructure
that was deployed (e.g. RDS endpoint/password). The way this is currently
achieved (on AWS) is that have the CloudFormation template dump this information
into the file `/etc/atl` as `RESOURCE_VAR=<resource>` lines. This can be then
sourced as environment variables to be retrieved at runtime . See the
helper-script `bin/ansible-with-atl-env` and the corresponding
`groups_vars/aws_node_local.yml` var-file.

#### Overriding parameters

If you want to customise the playbook behaviour the simplest method is to fork
this repository and add your own. However, for some one-off tasks you can also
override the default and calculated settings with special values. To do this, provide
command-line overrides to
[ansible-playbook](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html).

The most likely use-case for this is to download a custom product distribution
for testing (for example, a pre-release version of Jira). If you are running `ansible-playbook`
directly, the command for this would look like the following:

    ansible-playbook \
        -e atl_product_download_url=http://s3.amazon.com/atlassian/jira-9.0.0-PRE-TEST.tar.gz \
        -e atl_use_system_jdk=true \
        -e atl_download_format=tarball \
        \
        -i inv/aws_node_local aws_jira_dc_node.yml

You can also do this on a CloudFormation template where the stack details are in `/etc/atl`.
On such templates, the variable `ATL_ANSIBLE_EXTRA_PARAMS` is added to the
`ansible-playbook` parameters in `bin/ansible-with-alt-env`. In this case you
need to set it to:

    ATL_ANSIBLE_EXTRA_PARAMS="-e atl_product_download_url=http://s3.amazon.com/atlassian/jira-9.0.0-PRE-TEST.tar.gz -e atl_use_system_jdk=true -e atl_download_format=tarball"

To set the same parameters in the AWS Quick Starts for
[Jira Data Center](https://aws.amazon.com/quickstart/architecture/jira/),
[Confluence Data Center](https://aws.amazon.com/quickstart/architecture/confluence/), and
[Bitbucket Data Center](https://aws.amazon.com/quickstart/architecture/bitbucket/), enter
them in the `Custom command-line parameters for Ansible` field:

    -e atl_product_download_url=http://s3.amazon.com/atlassian/jira-9.0.0-PRE-TEST.tar.gz -e atl_use_system_jdk=true -e atl_download_format=tarball


## Development

### Development philosophy

The suite is intended to consist of a number of small, composable roles that can
be combined together into playbooks. Wherever possible the roles should be
platform-agnostic as possible, with platform-specific functionality broken out
into more specific roles.

Where possible the roles are also product-agnostic (e.g. downloads), with more
specific functionality added in later product-specific roles.

Roles should be reasonably self-contained, with sensible defaults configured in
`<role>/defaults/main.yml` and overridden by the playbook at runtime. Roles may
implicitly depend on variables being defined elsewhere where they cannot define
them natively (e.g. the `jira_config` role depends on the `atl_cluster_node_id`
var being defined; on AWS this is provided by the `aws_common` role, which
should be run first).

### Development and testing

See [Development](DEVELOPMENT.md) for details on setting up a development
environment and running tests.

## Ansible layout

* Helper scripts are in `bin/`. In particular the `bin/ansible-with-atl-env`
  wrapper is of use during AWS node initialisation. See _Usage_ above for more
  information.
* Inventory files are under `inv/`. For AWS `cfn-init` the inventory
  `inv/aws_node_local` inventory is probably what you want.
 * Note that this expects the environment to be setup with infrastructure
   information; see _Usage_ above.
* Global group vars loaded automatically from `group_vars/<group>.yml`. In
  particular note `group_vars/aws_node_local.yml` which loads infrastructure
  information from the environment.
* Roles are under `roles/`
 * Platform specific roles start with `<platform-shortname>_...`,
   e.g. `roles/aws_common/`.
 * Similarly, product-specific roles should start with `<product>_...`.

## License

Copyright © 2019 Atlassian Corporation Pty Ltd.
Licensed under the Apache License, Version 2.0.


[cfn-init]: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-init.html
[ec2-user-data]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
[jira-cfn-tmpl]: https://github.com/aws-quickstart/quickstart-atlassian-jira/blob/develop/templates/quickstart-jira-dc.template.yaml#L967
[ec2-launch-config]: https://docs.aws.amazon.com/autoscaling/ec2/userguide/LaunchConfiguration.html
