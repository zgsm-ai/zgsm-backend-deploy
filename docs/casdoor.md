# Login Configuration Guide

## Configuration Page

### Accessing the Configuration Page

Visit http://\{COSTRICT_BACKEND\}:\{PORT_CASDOOR\} to access the admin login page.

```commandline
Default account: admin
Default password: 123
```
![descript](casdoor-img/config-login-page.png)

Then enter the admin dashboard.

#### Adding an `oauth` Authentication Provider

Go to Identity → Providers → `Oauth` (template).

![descript](casdoor-img/add-oauth.png)

Fill in the standard `oauth` information.

![descript](casdoor-img/edit-oauth.png)

![descript](casdoor-img/id-secret.png)

After editing, scroll to the bottom of the page and click `Save & Exit`.

### Adding an SMS Authentication Provider

First, go to Identity → Providers → SMS (template).

![descript](casdoor-img/add-sms.png)

You only need to configure the region node settings.

![descript](casdoor-img/config-sms.png)

### Login Configuration

First, let's look at the normally enabled user login page.

![descript](casdoor-img/login-page.png)

Password login is for testing purposes and includes a built-in account that can be used directly.

```commandline
Account: demo
Password: test123
```

To configure login: go to Identity → Applications → loginApp (template).

![descript](casdoor-img/config-login.png)

First, modify the login page icon.

![descript](casdoor-img/edit-login-logo.png)

Click the delete button to remove the password login method.

![descript](casdoor-img/remove-password-login.png)

You can also remove the oauth login method (SMS verification cannot be removed).

![descript](casdoor-img/remove-oauth-login.png)

After configuration, scroll to the bottom of the page and click `Save & Exit`.

## Organization Configuration

> This section is mainly used to configure icons and title names.

![descript](casdoor-img/organization.png)

![descript](casdoor-img/edit-organization.png)

Please ensure the display name in `built-in` matches the user-group name, and replace `logo` and `Organization Favicon` with your own.