"""
Supabase JWT verification middleware.
- Skips /health, /docs, /openapi.json, /redoc
- Fetches JWKS from Supabase to verify ES256/HS256 tokens
- Injects user_id into request.state
- Returns 401 on any failure
"""
from __future__ import annotations

import logging
import httpx
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from jose import jwt, JWTError, jwk
from jose.utils import base64url_decode

logger = logging.getLogger(__name__)

# Paths that do NOT require authentication
_PUBLIC_PATHS = frozenset({"/health", "/docs", "/openapi.json", "/redoc"})

# Cache for JWKS keys
_jwks_cache: dict | None = None


async def _fetch_jwks(supabase_url: str) -> dict:
    """Fetch and cache JWKS from Supabase."""
    global _jwks_cache
    if _jwks_cache is not None:
        return _jwks_cache

    jwks_url = f"{supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(jwks_url)
        resp.raise_for_status()
        _jwks_cache = resp.json()
        logger.info("Fetched JWKS from %s (%d keys)", jwks_url, len(_jwks_cache.get("keys", [])))
        return _jwks_cache


def _find_jwk_key(jwks: dict, kid: str) -> dict | None:
    """Find a JWK key by its kid."""
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    return None


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Reject every request that does not carry a valid Supabase JWT."""

    def __init__(self, app, jwt_secret: str, supabase_url: str = "", algorithms: list[str] | None = None):
        super().__init__(app)
        self.jwt_secret = jwt_secret
        self.supabase_url = supabase_url
        self.algorithms = algorithms or ["HS256", "ES256"]

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # Allow public paths and CORS preflight
        if request.url.path in _PUBLIC_PATHS or request.method == "OPTIONS":
            return await call_next(request)

        auth_header = request.headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse({"detail": "Missing or malformed Authorization header."}, status_code=401)

        token = auth_header[7:]
        try:
            unverified_header = jwt.get_unverified_header(token)
            alg = unverified_header.get("alg", "HS256")
            kid = unverified_header.get("kid")

            if alg == "ES256" and kid and self.supabase_url:
                # Fetch JWKS and verify with matching public key
                jwks = await _fetch_jwks(self.supabase_url)
                jwk_key = _find_jwk_key(jwks, kid)
                if not jwk_key:
                    raise JWTError(f"No matching JWK found for kid: {kid}")
                # Construct the public key from the JWK
                public_key = jwk.construct(jwk_key, algorithm="ES256")
                payload = jwt.decode(
                    token,
                    public_key,
                    algorithms=["ES256"],
                    options={"verify_aud": False},
                )
            else:
                # Fallback to symmetric HS256
                payload = jwt.decode(
                    token,
                    self.jwt_secret,
                    algorithms=["HS256"],
                    options={"verify_aud": False},
                )

            user_id = payload.get("sub")
            if not user_id:
                raise JWTError("Token missing 'sub' claim.")
            request.state.user_id = user_id
        except JWTError as exc:
            logger.warning("JWT verification failed: %s", exc)
            return JSONResponse({"detail": "Invalid or expired token."}, status_code=401)

        return await call_next(request)
