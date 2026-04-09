
# Django Google Auth Email Website

This project allows users to sign in with Google (using django-allauth), search a built-in investor directory, and send outreach emails after authentication.

## Features
- Google sign-in via django-allauth
- Logged-in dashboard for investor search
- Searchable venture-capital lead table with contact details
- Send emails to selected investors with Gmail
- Testable and ready for local development

---

## 1. Setup & Configuration

### a. Change Credentials
Edit the `.env` file in the project root:

- `SECRET_KEY`: Set a secure Django secret key.
- `SOCIAL_AUTH_GOOGLE_CLIENT_ID`: Your Google OAuth client ID.
- `SOCIAL_AUTH_GOOGLE_SECRET`: Your Google OAuth client secret.
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Your SMTP email backend settings.

**Example:**
```
SECRET_KEY=your-django-secret-key
SOCIAL_AUTH_GOOGLE_CLIENT_ID=your-google-client-id
SOCIAL_AUTH_GOOGLE_SECRET=your-google-client-secret
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

### b. Install Dependencies
```
pip install -r requirements.txt
```

### c. Run Migrations
```
python manage.py migrate
```

---

## 2. Running the Backend (Django Server)
Start the Django development server:
```
python manage.py runserver
```
The backend will be available at: http://127.0.0.1:8000/

---

## 3. Accessing the Frontend
- Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Click "Login with Google" to sign in.
- After login, you will land on the dashboard where you can search investors and send email to selected contacts.

---

## 4. Testing
Run backend tests with:
```
python manage.py test
```

---

## 5. Temporary Render Deployment

This repo now includes a Render blueprint in `render.yaml` for the service URL `https://leadly-ew8k.onrender.com`.

### Render setup
1. Push this repository to GitHub.
2. In Render, create a new Web Service from the repo or use the blueprint import flow.
3. Confirm these environment variables are set:
	- `DEBUG=False`
	- `ALLOWED_HOSTS=leadly-ew8k.onrender.com`
	- `CSRF_TRUSTED_ORIGINS=https://leadly-ew8k.onrender.com`
	- `SECRET_KEY` set to a strong value
	- `SOCIAL_AUTH_GOOGLE_CLIENT_ID` and `SOCIAL_AUTH_GOOGLE_SECRET`
	- Any email backend variables you need in production
4. Deploy.

### Google OAuth update
In Google Cloud Console, add these values for the same OAuth client used by the app:
- Authorized JavaScript origin: `https://leadly-ew8k.onrender.com`
- Authorized redirect URI: `https://leadly-ew8k.onrender.com/accounts/google/login/callback/`

### Important note
If you do not attach a PostgreSQL database, Render will use the default SQLite fallback. That works for a temporary deployment, but data will be lost when the instance is rebuilt or the filesystem is reset.

---

## 6. Directory Structure
- `accounts/`: User management and email logic
- `core/`: Main Django project
- `templates/`: HTML templates (frontend)
- `static/`: Static files (CSS, JS, images)
- `.env`: Environment variables (edit this for your credentials)

---

**Remember:** Replace all placeholder credentials in `.env` before deploying or using in production.
