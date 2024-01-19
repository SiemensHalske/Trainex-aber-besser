# Changelog

## [v2023-12-13] - 2023-12-13

- Add debug logging for incoming requests and successful login (H)
- Add JWT cookie CSRF protection and disable access token expiration (H)

## [v2023-12-05] - 2023-12-05

- eduCampus (H)
  
## [v2023-12-12] - 2023-12-12

- Refactor login function to set access_token_cookie (H)
- Update access token cookie name (H)
- Add JWT token location and secure cookie (H)
- Remove unused code in auth.py and update import in main.py (H)
- Fix import issue in auth.py (H)
- Update JWT authentication in app.py and auth.py (H)
- Add Waitress server for production deployment (H)
- Update login route to accept GET and POST requests (H)
- Add certificate and key path variables (H)
- Add JWT authentication and SSL support (H)
- This commit adds JWT authentication using the Flask-JWT-Extended library. It also adds SSL support to the application by specifying the SSL certificate and private key paths in the `app.run()` function. Additionally, some code comments and print statements have been updated. (H)
- Refactor user-related endpoints (H)
- Add query parameter handling for user endpoints (H)
- Move error templates (H)

## [v2023-12-07] - 2023-12-07

- added /static (H)

## [v2023-12-14] - 2023-12-14

- Add PrometheusMetrics for monitoring (H)
- Refactor code to improve performance and readability (H)
- Add methods to retrieve role, user, lecturer, and course information (H)
- Refactor User model and add user-related methods (H)
- Update database and logging functionality (H)
- Add new files and update .gitignore (H)
- This commit adds new files and updates the .gitignore file to exclude the newly generated Python cache files and the users.db binary file. (H)
- Merge pull request #1 from SiemensHalske/main (1)
- Updating Backend in Frontend Branch (1)
- Merge branch 'frontend' of https://github.com/SiemensHalske/Trainex-aber-besser (H)
- Update users.db (H)
- Add database files to .gitignore (H)
- removing .db from git commits (FO)
- Update .gitignore and remove SSL certificate path from app.py (H)
- adding welcome banner to aktuelles page (FO)
- Merge branch 'main' of https://github.com/SiemensHalske/Trainex-aber-besser (H)
- Update SSL configuration and logger name (H)
- making log path relative (FO)
- making extension path relative, ignoring all .pyc files (FO)

## [v2023-12-10] - 2023-12-10

- Update logout route to redirect to auth login (H)
- Refactor logging configuration and add logging endpoint (H)
- Enable inline suggestions and update log file path (H)
- Update settings.json and app.py (H)

## [v2023-12-09] - 2023-12-09

- Update banner.css and login.html (H)
- Add AuditLog model and set_audit_log function (H)
- Update database path and import os module (H)
- Add login route to auth blueprint (H)
- . (H)
- Add debug print statement in login function (H)
- Add login success message and update login failure message (H)
- Fix authentication and session management (H)

## [v2023-12-11] - 2023-12-11

- Update logging configuration in main.py (H)
- Add error handlers to main blueprint (H)
- Add session variable for user_id and implement new routes for retrieving user information (H)
- Add logging endpoint to handle logging requests (H)

## [v2023-12-08] - 2023-12-08

- Add signal handler and new routes (H)
- Add banner route and update templates (H)
- Update banner iframe source (H)
- Update database path and form validators (H)

## [v2023-12-15] - 2023-12-15

- Update .gitignore, login form, error templates, and requirements generator (H)
- Add route info for retrieving calendar events by user ID (H)
- Fix check_login_attempts function (H)
- Add calendar endpoints and error handlers (H)
- Update app.py and main.py (H)
- Merge branch 'frontend' of https://github.com/SiemensHalske/Trainex-aber-besser (H)
- adding basic design for Aktuelles Page (FO)

