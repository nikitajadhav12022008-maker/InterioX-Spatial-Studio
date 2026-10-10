# InterioX Backend (FastAPI)

Starter API for InterioX Spatial Studio: mobile-OTP auth, whole-house projects,
designer directory + review requests, catalog, and server-side collision/audit.

## Run locally
```bash
docker compose up -d            # PostgreSQL+PostGIS and Redis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py                  # demo designers
uvicorn app.main:app --reload   # http://localhost:8000/docs
```

## Auth flow (two-step verification)
1. `POST /auth/otp/request` `{ "mobile": "+919876543210" }` — sends a 6-digit code (5 min expiry, 30 s resend cooldown).
2. `POST /auth/otp/verify` `{ "mobile": "...", "code": "123456", "name": "Your Name" }` — `name` only needed on first sign-in. Returns a JWT.
3. Send `Authorization: Bearer <token>` on all other routes.

`OTP_PROVIDER=console` prints codes in the server log (dev). Set `OTP_PROVIDER=twilio`
plus Twilio credentials for real SMS, or add another class implementing `OTPProvider`
in `app/otp.py` (e.g. MSG91) for India-local delivery.

## Endpoints
| Method | Path | Purpose |
|---|---|---|
| POST | /auth/otp/request | Send OTP |
| POST | /auth/otp/verify | Verify OTP, get JWT |
| GET/POST | /projects | List / create whole-house or single-room designs |
| PUT/DELETE | /projects/{id} | Save / delete |
| POST | /projects/{id}/audit | Server-side collision + ergonomic audit |
| GET | /designers?city=Pune&lat=&lon= | Nearby designers (distance-sorted) |
| POST | /designers/{id}/review-requests | Ask a designer to verify a design |
| GET | /designers/review-requests/mine | Track your requests |
| GET | /catalog?room=&category=&style= | Catalog |

## Connecting the frontend
The published demo stores everything in the browser. To go live, replace the
`localStorage` calls and the local OTP generation in the HTML with `fetch()` calls to
the endpoints above. Production checklist: restrict CORS origins, use HTTPS,
rotate `JWT_SECRET`, add rate limiting at NGINX, and notify designers on new
review requests (email/WhatsApp).

## New in this version
- **Building types**: `Project.building_type` (house|office|hospital|cafe) — the
  frontend's whole-building view and AI generator are scoped to whichever type
  is active.
- **Photo uploads on review requests**: `POST /uploads/photo` (JPEG/PNG/WEBP,
  5MB max) returns a `photo_url`; pass it in `POST /designers/{id}/review-requests`.
  Swap the local-disk save in `app/routers/uploads.py` for S3/Cloud Storage in production.
- **Ratings**: `POST /ratings` `{ "value": 1-5, "comment": "" }` and
  `GET /ratings/summary` for the average + count shown in the app.
