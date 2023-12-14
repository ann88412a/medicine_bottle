setup new db user

`CREATE USER Demo@localhost IDENTIFIED BY 'Demo_0000';`

setting permissions
`GRANT ALL PRIVILEGES ON MedicationTalk.* TO Demo@localhost;`

ssl
`openssl req -x509 -new -nodes -sha256 -utf8 -days 3650 -newkey rsa:2048 -keyout server.key -out server.crt -config ssl.conf`

`openssl pkcs12 -export -in server.crt -inkey server.key -out server.pfx`