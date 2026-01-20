## Local Email Service (FastAPI + Gmail)

This is a small FastAPI service that sends **HTML emails via Gmail SMTP** behind a simple authenticated HTTP endpoint.

The service is containerized with Docker and, by default, listens on port **5015**.

---

## Environment Variables

Define these in a `.env` file (or your environment) before running:

- **`GMAIL_USER`**: Gmail address used as the sender (`From`).
- **`GMAIL_APP_PASSWORD`**: Gmail **App Password** (not your main Gmail password).
- **`EMAIL_API_KEY`**: Secret key required in the `x-api-key` HTTP header for all requests.

Example `.env`:

```bash
GMAIL_USER="yourgmail@gmail.com"
GMAIL_APP_PASSWORD="your_app_password_here"
EMAIL_API_KEY="some-long-random-secret"
```

---

## Running the Service

### 1. Run with Python (no Docker)

Install dependencies (assuming `requirements.txt` exists):

```bash
pip install -r requirements.txt
```

Run with Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 5015
```

The API will be available at:

```text
http://localhost:5015
```

### 2. Run with Docker

Build the image:

```bash
docker build -t local-email-service .
```

Run the container (forwarding port 5015 and passing env vars / .env):

```bash
docker run --env-file .env -p 5015:5015 local-email-service
```

The API will now be available at:

```text
http://localhost:5015
```

---

## API

### `POST /send-email`

- **Description**: Sends an HTML email via Gmail.
- **Method**: `POST`
- **URL**: `http://<host>:5015/send-email`
- **Auth**: Header `x-api-key: <your EMAIL_API_KEY>`
- **Request body** (`application/json`):
  - `to_email` (string, valid email) — Recipient email address.
  - `subject` (string) — Email subject line.
  - `body` (string, HTML) — Email body as HTML.

**Successful response** (`200 OK`, JSON):

```json
{
  "status": "success",
  "message": "Email sent to recipient@example.com"
}
```

If `x-api-key` is missing or invalid, the API returns:

- `401 Unauthorized` with `{"detail": "Invalid API key"}`.

---

## `curl` Examples

### 1. Basic `curl` request (Linux/macOS / Git Bash)

```bash
curl -X POST "http://localhost:5015/send-email" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_EMAIL_API_KEY_HERE" \
  -d '{
    "to_email": "recipient@example.com",
    "subject": "Test Email from Local Service",
    "body": "<h1>Hello!</h1><p>This is a <strong>test</strong> email sent from the local email service.</p>"
  }'
```

### 2. PowerShell-friendly example (Windows)

```powershell
$API_KEY = "YOUR_EMAIL_API_KEY_HERE"
$URL = "http://localhost:5015/send-email"

curl -Method POST $URL `
  -Headers @{ "Content-Type" = "application/json"; "x-api-key" = $API_KEY } `
  -Body '{
    "to_email": "recipient@example.com",
    "subject": "PowerShell Test",
    "body": "<p>Sent using PowerShell curl (Invoke-WebRequest under the hood).</p>"
  }'
```

### 3. Targeting a remote host (deployed container)

```bash
curl -X POST "http://your-server-host-or-ip:5015/send-email" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_EMAIL_API_KEY_HERE" \
  -d '{
    "to_email": "recipient@example.com",
    "subject": "Deployed Service Test",
    "body": "<p>This email was sent from the deployed FastAPI service.</p>"
  }'
```

---

## Notes

- Make sure **less secure app access is not required** because you are using a **Gmail App Password**, which is the recommended way to use Gmail SMTP.
- The email body is treated as **HTML** (`text/html`), so you can safely include basic HTML tags.


