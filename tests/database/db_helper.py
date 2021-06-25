from datetime import datetime
import json
from os import listdir, path, getcwd
from pydoc import locate
from typing import Any, List
from sqlalchemy.orm.session import Session
from app.context.context import AppContext


class DbHelper:
    db: Session
    json_files: List[str]
    added_files: List[str]

    RELATIVE_PATH: str = path.join(getcwd(), "tests/database/data/")
    DATETIME_COLUMNS: List[str] = ["iat", "exp"]

    def __init__(self, context: AppContext):
        self.db = context.db

    def mock_db_data(self):
        """
        Gets all json files from /data folder and adds models to test database.
        """
        self.added_files = []
        self.json_files = [file for file in listdir(self.RELATIVE_PATH) if file.endswith(".json")]

        for file in self.json_files:
            if file not in self.added_files:
                self.mock_model(file)

    def mock_model(self, file: str):
        """
        Recursive function that adds model to test database. It checks if model depends
        on some other model and recursively adds that one first.
        """
        with open(self.RELATIVE_PATH + file) as f:
            model_json = json.load(f)
        for dependency_file in model_json["depends"]:
            if dependency_file not in self.added_files:
                self.mock_model(dependency_file)

        t: Any = locate(model_json["type_name"])
        for row in model_json["data"]:
            row = self.convert_datetimes(row)
            model = t(**row)
            self.db.add(model)
        self.db.commit()
        self.added_files.append(file)

    def convert_datetimes(self, d: dict) -> dict:
        """
        Converts all necessary columns which require datetime format.
        """
        for column in self.DATETIME_COLUMNS:
            if column in d and d[column] is not None:
                d[column] = datetime.strptime(d[column], "%Y-%m-%d %H:%M:%S.%f")
        return d
