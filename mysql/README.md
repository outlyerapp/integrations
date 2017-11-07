# MySQL Integration

The plugin for this integration runs `mysql show global status` on the command line with some options. By default it will use
the user name `root` with "mysql" as the password.

To create a new user specifically for this integration with a minimum set of privileges use the following command:

```
GRANT USAGE ON *.* TO 'outlyer'@'localhost' IDENTIFIED BY 'password'
```

Then configure the username and password to match.
