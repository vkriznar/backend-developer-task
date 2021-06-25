# Database

Mock database is done with SQLite and is in `app/app.db`. You can open it with SQLite like explorer such as DBBrowser(SQLite).

For testing an in-memory sqlite database was used that is created, mocked and finally removed for every testing scenario. Database mocking is done with the help of .json files located in `tests/database/data`.
