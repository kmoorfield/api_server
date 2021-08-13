﻿START TRANSACTION;

DO $$
BEGIN
    CREATE TABLE "Dogs" (
        "Id" integer GENERATED BY DEFAULT AS IDENTITY,
        "Fact" text NULL,
        CONSTRAINT "PK_Id" PRIMARY KEY ("Id")
    );
END $$;

COMMIT;