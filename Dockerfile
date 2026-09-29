# syntax=docker/dockerfile:1
FROM node:24-slim AS web
WORKDIR /web
RUN corepack enable && corepack prepare pnpm@11.25.0 --activate
COPY apps/web/package.json apps/web/pnpm-lock.yaml apps/web/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
COPY apps/web/ ./
RUN pnpm build

FROM python:3.14-slim AS backend
WORKDIR /app
COPY requirements.lock pyproject.toml ./
COPY packages/engine/ ./packages/engine/
COPY apps/api/ ./apps/api/
RUN pip install --no-cache-dir -r requirements.lock && pip install --no-cache-dir --no-deps .
FROM backend AS catalog
RUN lazcon build --output /release/catalog.sqlite
COPY scripts/verify_release.py /app/scripts/verify_release.py
COPY tests/fixtures/reference.json /app/tests/fixtures/reference.json
RUN python scripts/verify_release.py /release/catalog.sqlite > /release/verification.json

FROM backend AS runtime
COPY --from=catalog /release/ /app/release/
RUN chmod 0555 /app/release && chmod 0444 /app/release/*
COPY --from=web /web/dist /app/web
ENV LAZ_DATABASE=/app/release/catalog.sqlite LAZ_WEB_DIST=/app/web PYTHONDONTWRITEBYTECODE=1
USER 10001
# Check database access and application setup with the same user used at runtime.
RUN python -c "from laz_api.app import create_app; create_app()"
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health', timeout=3).close()"]
CMD ["lazcon", "serve", "--host", "0.0.0.0", "--port", "8000"]
