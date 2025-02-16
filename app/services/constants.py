from app.core.config import settings


SPREADSHEET_BODY = {
    "sheets": [
        {
            "properties": {
                "sheetType": "GRID",
                "sheetId": 0,
                "title": "Лист1",
                "gridProperties": {"rowCount": 100, "columnCount": 11},
            }
        }
    ],
}

PERMISSIONS_BODY = {
    "type": "user",
    "role": "writer",
    "emailAddress": settings.email
}


TABLE_VALUES = [
    ["Топ проектов по скорости закрытия"],
    ["Название проекта", "Время сбора", "Описание"],
]


UPDATE_BODY = {"majorDimension": "ROWS"}
