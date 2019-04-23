
# Atlassian Data-Center Installation Automation

## Introduction

This repository is a suite of Ansible roles, playbooks and support scripts to
automate the installation and maintenance of Atlassian Data-Center products in
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
sourced as environment variables to be retrieved at runtime. See the
helper-script `bin/ansible-with-atl-env` for an example.

### Maintenance playbooks

(None currently; TBW)

## Development philosophy

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
should be run firs).

## Ansible layout



* Global defaults in group_vars/all.yml
** This is where env-vars should be converted to Ansible vars. It also acts as a required-env list.
** The CF env is usually stored in /etc/atl. The script `bin/ansible-with-atl-env` will run Ansible with that environment set.
* Runtime information about the EC2 environment can be injected by depending on
  `apws_common` in a role's `meta/main.yml` (or adding it to the playbook before
  the requiring role.

## License

Copyright © 2019 Atlassian Corporation Pty Ltd.
Licensed under the Apache License, Version 2.0.


[cfn-init]: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-init.html
[ec2-user-data]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
[jira-cfn-tmpl]: https://github.com/aws-quickstart/quickstart-atlassian-jira/blob/develop/templates/quickstart-jira-dc.template.yaml#L967
[ec2-launch-config]: https://docs.aws.amazon.com/autoscaling/ec2/userguide/LaunchConfiguration.html
