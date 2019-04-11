
# !! Rough notes for now, expand later.


## Ansible layout

* Global defaults in group_vars/all.yml
** This is where env-vars should be converted to Ansible vars. It also acts as a required-env list.
** The CF env is usually stored in /etc/atl. The script `bin/ansible-with-atl-env` will run Ansible with that environment set.
* Runtime information about the EC2 environment can be injected by depending on
  `aws_common` in a role's `meta/main.yml` (or adding it to the playbook before
  the requiring role.
