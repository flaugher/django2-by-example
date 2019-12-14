# README

## How login works

1. The user enters http://127.0.0.1:8000/account/login/ in their browser.
2. bookmarks/urls.py sends the request to account/urls.py.
3. account/urls.py parses /login/ from the path and passes the request to auth_views.LoginView.
4. LoginView processes the request and returns the response rendered in the registration/login.html template.
5. The login.html template includes the base.html template which sees that the user is not authenticated so it just displays the "Bookmarks" logo in the header div and a "Login" link.
6. Next the rest of the login.html template is rendered.  The template displays the Login header and a login form.  The form contains a hidden field named 'next'.  If next isn't provided, Django redirects to settings.LOGIN_REDIRECT_URL which in our case is 'dashboard' (see [class LoginView](https://shrtm.nu/ZEDv)).
7. If the user enters an incorrect username/password pair, the form fails validation and the login template re-displays the Login form with an error message.
8. If the user enters their correct credentials, the hidden 'next' value in the form, which contains 'dashboard', is passed to bookmarks/urls.py which passes it to account/urls.py which passes the request to the dashboard view which in turn renders the dashboard.html template.
9. dashboard.html includes base.html.  This time base.html sees that the user is authenticated so it renders the links in the header, a Logout link, and the remainder of the dashboard.html template.