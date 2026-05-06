
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from .dings import db
from .routes import begriffe
from .routes import kategorien
from .routes import users
from .routes import begriff_history

app = FastAPI(docs_url=None)  # Standard Swagger abschalten

# DB initialisieren
db.init_db()

# Router registrieren
app.include_router(begriffe.router)
app.include_router(kategorien.router)
app.include_router(users.router)
app.include_router(begriff_history.router)

# Statische Dateien für Swagger UI bereitstellen
app.mount("/static", StaticFiles(directory="static"), name="static")

# Eigene Swagger-UI-Route
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
	return get_swagger_ui_html(
		openapi_url=app.openapi_url,
		title="API Dokumentation",
		swagger_js_url="/static/swagger/swagger-ui-bundle.js",
		swagger_css_url="/static/swagger/swagger-ui.css",
	)