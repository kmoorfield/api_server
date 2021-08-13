FROM flyway/flyway:latest
COPY SQL_Migrations/*.sql /flyway/sql/
ENTRYPOINT ["flyway"]
CMD ["-?"]