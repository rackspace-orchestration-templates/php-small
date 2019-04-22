Description
===========

#### Production
This stack is intended for low to medium traffic production
websites and can be scaled as needed to accommodate future
growth.  This stack includes a Cloud Load Balancer, Cloud
Database, and a Master server (plus optional secondary
servers).  It also includes Cloud Monitoring and Cloud
Backups.

This stack is running the latest version of
[nginx](https://www.nginx.com/),
and [PHP FPM](http://php-fpm.org/).
with a Cloud Database running
[MySQL 5.6](http://www.mysql.com/about/).


Instructions
===========

#### Getting Started
If you're new to PHP, the [Getting
Started](http://www.php.net/manual/en/getting-started.php) page can walk you
through the basics of PHP and it's uses.

If you chose to enable PHPMyAdmin, you can access it using the username and
password found in the Credentials section, with the URL listed under
PHPMyAdmin URL.

#### Scaling out
This deployment is configured to be able to scale out easily.  However,
if you are expecting higher levels of traffic, please look into one of our
larger-scale stacks.

#### Details of Your Setup
This deployment was stood up using [Ansible](http://www.ansible.com/).
Once the stack has been deployed, Ansible will not run again unless you update the
stack. **Any changes made to the configuration may be overwritten when the stack
is updated.**

[nginx](https://www.nginx.com/) was configured to serve contents out of /var/www/vhosts/example.com/httpdocs,
where example.com is the domain that you provided during the setup.

[PHP-FPM](http://php-fpm.org/) was installed using the packaged version for
the chosen operating system, in order to ensure that you have the latest
stable release.

[Lsyncd](https://github.com/axkibe/lsyncd) has been installed in order to
sync static content from the Master server to all secondary servers.
When uploading content, it only needs to be uploaded to the Master node,
and will be automatically synchronized to all secondary nodes.  By default,
/var/www will be synchronized, unless otherwise specified during setup.

MySQL is being hosted on a Cloud Database instance, running MySQL 5.6.
Backups will need to be configured manually.

Backups are configured using Cloud Backups.  The Master server is configured
to back up /var/www once per week, and to retain
these backups for 30 days.

Monitoring is configured to verify that nginx is running on both the Master
and all secondary servers, as well as that the Cloud Load Balancer is
functioning.  Additionally, the default CPU, RAM, and Filesystem checks
are in place on all servers.

#### Logging in via SSH
The private key provided with this deployment can be used to log in as
root via SSH. We have an article on how to use these keys with [Mac OS X and
Linux](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-linuxmac)
as well as [Windows using
PuTTY](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-windows).
This key can be used to log into all servers on this deployment.
Additionally, passwordless authentication is configured from the Master
server to all secondary servers.

#### Additional Notes
You can add additional servers to this deployment by updating the
"server_count" parameter for this stack. This deployment is
intended for low to medium traffic production websites and can be
scaled as needed to accommodate future growth.

When scaling this deployment by adjusting the "server_count" parameter,
make sure that you DO NOT change the "database_flavor" and "database_disk"
parameters, as this will result in the loss of all data within the
database.

This stack will not ensure that PHP or the servers themselves are
up-to-date.  You are responsible for ensuring that all software is
updated.


Requirements
============
* A Heat provider that supports the following:
  * OS::Heat::RandomString
  * OS::Heat::ResourceGroup
  * OS::Heat::SoftwareConfig
  * OS::Heat::SoftwareDeployment
  * OS::Nova::KeyPair
  * OS::Nova::Server
  * OS::Trove::Instance
  * Rackspace::Cloud::BackupConfig
  * Rackspace::Cloud::LoadBalancer
  * Rackspace::CloudMonitoring::Check
* An OpenStack username, password, and tenant id.
* [python-heatclient](https://github.com/openstack/python-heatclient)
`>= v0.2.8`:

```bash
pip install python-heatclient
```

We recommend installing the client within a [Python virtual
environment](http://www.virtualenv.org/).

Parameters
==========
Parameters can be replaced with your own values when standing up a stack. Use
the `-P` flag to specify a custom parameter.

* `php_url`: Domain used to configure Nginx (Default: example.com)
* `db_user`: Username to configure for SQL (Default: example)
* `db_name`: Database to configure in SQL (Default: example)
* `php_myadmin`: Enable or disable PHPMyAdmin (Default: False)
* `backup_email`: E-mail address to be notified for failing backups (Default: admin@example.com)
* `lsync_directory`: This directory will be synchronized between all servers within this stack.  Leave blank to manually configure Lsyncd (Default: /var/www)
* `server_flavor`: Flavor of Cloud Server to be used for all servers in this stack (Default: 4 GB General Purpose v1)
* `database_disk`: Size of the Cloud Database volume in GB (Default: 5)
* `database_flavor`: Flavor for the Cloud Database (Default: 1GB Instance)
* `server_count`: Number of secondary web nodes (Default: 0)

Outputs
=======
Once a stack comes online, use `heat output-list` to see all available outputs.
Use `heat output-show <OUTPUT NAME>` to get the value of a specific output.

* `php_public_ip`: Load Balancer IP
* `php_public_url`: Public URL
* `phpmyadmin_url`: PHPMyAdmin URL (if enabled)
* `mysql_user`: Database User
* `mysql_database`: Database Name
* `mysql_password`: Database Password
* `mysql_host`: Database Host
* `ssh_private_key`: SSH Private Key
* `server_ip`: Server Public IP
* `secondary_ips`: Secondary Node IPs

For multi-line values, the response will come in an escaped form. To get rid of
the escapes, use `echo -e '<STRING>' > file.txt`. For vim users, a substitution
can be done within a file using `%s/\\n/\r/g`.
