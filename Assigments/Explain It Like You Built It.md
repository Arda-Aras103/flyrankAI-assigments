# Explain It Like You Built It

## How my API connects to PostgreSQL

In my project, the API and PostgreSQL run in separate Docker containers. In the Compose setup, the PostgreSQL service is named `db`, so the API uses `db` in its database connection address to reach it over Docker's shared network. From inside the API container, `localhost` means the API container itself, not the database. That is why the API uses `db` to find PostgreSQL.
