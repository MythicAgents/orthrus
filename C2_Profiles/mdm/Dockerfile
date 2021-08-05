FROM itsafeaturemythic/python38_sanic_c2profile:0.0.5

RUN apt update && apt install -y unzip wget
RUN wget https://github.com/micromdm/micromdm/releases/download/v1.8.0/micromdm_v1.8.0.zip && unzip micromdm_v1.8.0.zip && mkdir /pkg

COPY certs /certs

COPY micromdm.db /var/db/micromdm/micromdm.db

RUN /build/linux/micromdm serve \
	-server-url=https://localhost \
	-api-key mythic \
	-filerepo /pkg \
	-tls-cert /certs/mdm.crt \
	-tls-key /certs/mdm.key \
	-command-webhook-url http://localhost:5000/webhook & sleep 1 && \
    /build/linux/mdmctl config set -name c2 -api-token mythic -server-url https://localhost -skip-verify true && \
    /build/linux/mdmctl config switch -name c2 && \
    /build/linux/mdmctl mdmcert upload -cert /certs/apn.pem -private-key /certs/apn.key