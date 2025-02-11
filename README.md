## 📌 Redirect Service API

####  This service allows you to create, update, and delete redirect rules.



## 🛠️ Installation


Start **Docker** and **create a superuser** automatically (**recommend**):
   ```bash
   bash bin/manage setup
   ```
   **OR**

Start **Docker** manual:
   ```bash
   docker-compose up --build -d
   ```


Run tests in **Docker**:
   ```bash
   bash bin/manage tests
   ```
---

## 🔑 Authentication

The service uses JWT authentication. You need to obtain a token before using private endpoints.

### 👉 Obtain a JWT token

```http
POST /auth/token/
```

**Request example:**

```json
{
  "username": "admin",
  "password": "adminpassword"
}
```

**Response example:**

```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

📉 Add the token to the `Authorization: Bearer <your_access_token>` header to access private endpoints.

---

## 🌍 Public Redirects

Public redirects are accessible to all users.

### 🔍 Get a redirect

```http
GET /api/v1/redirect/public/{redirect_identifier}
```

**Request example:**

```http
GET /api/v1/redirect/public/RR6AMgkdbd4suEZb
```

**Response:** HTTP 302 Redirect to the corresponding URL.

---

## 🔒 Private Redirects

Private redirects are only accessible to their owner.

### 🔍 Get a redirect (authentication required)

```http
GET /api/v1/redirect/private/{redirect_identifier}
```

**Request example:**

```http
GET /api/v1/redirect/private/RR6AMgkdbd4suEZb
Authorization: Bearer your_access_token
```

**Response:** HTTP 302 Redirect (if the redirect belongs to the user).

---

## ✏️ Managing Redirects

### 🔀 Create a redirect

```http
POST /api/v1/url/
```

**Request example:**

```json
{
  "redirect_url": "https://google.com",
  "is_private": false
}
```

**Response example:**

```json
{
  "redirect_identifier": "RR6AMgkdbd4suEZb"
}
```

---

### 📈 Update a redirect

```http
PUT /url/{redirect_identifier}
Authorization: Bearer your_access_token
```

**Request example:**

```json
{
  "redirect_url": "https://newsite.com"
}
```

**Response example:**

```json
{
  "redirect_identifier": "RR6AMgkdbd4suEZb"
}
```

---

### ❌ Delete a redirect

```http
DELETE /url/{redirect_identifier}
Authorization: Bearer your_access_token
```

**Response example:**

```json
{
  "message": "Redirect deleted successfully."
}
```

---


