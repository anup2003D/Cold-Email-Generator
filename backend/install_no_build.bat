@echo off
echo ========================================
echo Quick Fix: Installing Core Packages Only
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing packages that don't need compilation...
echo This will skip hnswlib to avoid C++ build tool requirement.
echo.

pip install --upgrade pip

echo Installing core packages...
pip install fastapi==0.109.0 uvicorn==0.27.0 pydantic==2.5.3 python-dotenv==1.0.0

echo Installing Google packages...
pip install google-auth==2.27.0 google-auth-oauthlib==1.2.0 google-auth-httplib2==0.2.0 google-api-python-client==2.115.0

echo Installing LangChain packages...
pip install langchain-community langchain-core langchain-groq

echo Installing ChromaDB (without hnswlib)...
pip install chromadb --no-deps
pip install chroma-hnswlib requests pydantic-settings posthog opentelemetry-api opentelemetry-exporter-otlp-proto-grpc opentelemetry-sdk pypika build overrides importlib-resources grpcio bcrypt typer kubernetes uvicorn fastapi

echo Installing other packages...
pip install pandas sentence-transformers

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Now starting the server...
echo.

python main.py
