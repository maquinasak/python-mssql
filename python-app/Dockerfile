FROM python:3.11-slim

WORKDIR /app

# COPY --from=builder /app /app

# Copia los archivos de la aplicación
COPY ./src .

# instala los requerimientos
RUN pip install -r requirements.txt


EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
# CMD ["flask", "run", "--host","0.0.0.0"]

