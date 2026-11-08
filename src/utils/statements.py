from ..utils.config import config

# Add SQL strings here, then import the name where it is used, for example:
# from ..utils.statements import CREATE_APPLICATIONS_TABLE
CREATE_EMAILS_TABLE = f"""CREATE TABLE {config['DB_SCHEMA']}.t_emails (
                        emailID  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        email    VARCHAR(255) NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    );"""

CREATE_APPLICATION_TABLE = f"""CREATE TABLE {config['DB_SCHEMA']}.t_jobs (
                                jobID        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                emailID      INTEGER NOT NULL REFERENCES {config['DB_SCHEMA']}.t_emails(emailID),
                                company      TEXT NOT NULL,
                                position     TEXT NOT NULL,
                                status       TEXT NOT NULL CHECK (status IN ('applied', 'accepted', 'rejected')),
                                date_applied TIMESTAMP NOT NULL
                            );"""
