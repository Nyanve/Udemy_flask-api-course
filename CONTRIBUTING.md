# CONTRIBUTING

## How to run dockerfile localy

docker run -dp 5000:5000 -w /app -v "$(pwd):/app" teclado-site-flask sh -c "flask run --host 0.0.0.0"

docker run -p 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api-email sh -c "flask run --host 0.0.0.0"

