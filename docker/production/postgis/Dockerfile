FROM postgis:11-3.0-alpine

COPY ./docker/production/postgis/backup.sh /usr/local/bin/backup
RUN chmod +x /usr/local/bin/backup

COPY ./docker/production/postgis/restore.sh /usr/local/bin/restore
RUN chmod +x /usr/local/bin/restore

COPY ./docker/production/postgis/list-backups.sh /usr/local/bin/list-backups
RUN chmod +x /usr/local/bin/list-backups
