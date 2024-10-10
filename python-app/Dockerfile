FROM python:3.11-slim

WORKDIR /app

COPY ./src .

# Actualizo el administrador de paquetes de python
RUN pip install --upgrade pip

# instala los requerimientos
RUN pip install -r requirements.txt

# COPY --from=builder /app /app
# Copia los archivos de la aplicación
# install FreeTDS and dependencies
RUN apt-get update 
RUN apt-get install curl -y
RUN apt-get install unixodbc -y 
RUN apt-get install unixodbc-dev -y 
RUN apt-get install freetds-dev -y 
RUN apt-get install freetds-bin -y
RUN apt-get install tdsodbc -y 
RUN apt-get install --reinstall build-essential -y

RUN chmod +x ./installodbc.sh
RUN ./installodbc.sh

# populate "ocbcinst.ini"
# RUN echo "[FreeTDS]\n\
#     Description = FreeTDS unixODBC Driver\n\
#     Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
#     Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini


EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
# CMD ["flask", "run", "--host","0.0.0.0"]

