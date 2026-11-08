"""PostgreSQL database helper built on psycopg 3."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import psycopg
from psycopg.rows import dict_row

from ..utils.config import config


class Database:
    """Run SQL statements against a PostgreSQL database.

    Each operation opens its own connection and commits automatically when
    successful. Use ``%s`` placeholders in statements and pass their values in
    ``params`` to keep data separate from SQL.
    """

    def __init__(
        self,
        host: str | None = None,
        password: str | None = None,
        dbname: str | None = None,
        *,
        user: str | None = None,
        schema: str | None = None,
        port: int | None = None,
        **connection_options: Any,
    ) -> None:
        self.schema = schema or config.get("DB_SCHEMA", "public")
        configured_port = port if port is not None else config.get("DB_PORT", "5432")
        self.connection_parameters = {
            key: value
            for key, value in {
                "host": host or config.get("DB_HOST"),
                "password": password or config.get("DB_PASSWORD"),
                "dbname": dbname or config.get("DB_NAME"),
                "user": user or config.get("DB_USER"),
                "port": int(configured_port),
                **connection_options,
            }.items()
            if value is not None
        }

    def connect(self) -> psycopg.Connection:
        """Open a psycopg connection; the caller is responsible for closing it."""
        return psycopg.connect(**self.connection_parameters, row_factory=dict_row)

    def _run(
        self, statement: str, params: Sequence[Any] | None = None
    ) -> list[dict[str, Any]]:
        connection = self.connect()
        try:
            cursor = connection.execute(statement, params or ())
            rows = cursor.fetchall() if cursor.description is not None else []
            connection.commit()
            return rows
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def create(self, statement: str, params: Sequence[Any] | None = None) -> list[dict[str, Any]]:
        """Execute a CREATE statement (table, index, schema, and so on)."""
        return self._run(statement, params)

    def insert(self, statement: str, params: Sequence[Any] | None = None) -> list[dict[str, Any]]:
        """Execute an INSERT statement; use RETURNING to receive inserted rows."""
        return self._run(statement, params)

    def update(self, statement: str, params: Sequence[Any] | None = None) -> list[dict[str, Any]]:
        """Execute an UPDATE statement; use RETURNING to receive changed rows."""
        return self._run(statement, params)

    def delete(self, statement: str, params: Sequence[Any] | None = None) -> list[dict[str, Any]]:
        """Execute a DELETE statement; use RETURNING to receive deleted rows."""
        return self._run(statement, params)

    def execute(self, statement: str, params: Sequence[Any] | None = None) -> list[dict[str, Any]]:
        """Execute any SQL statement, including SELECT, and return rows if present."""
        return self._run(statement, params)
