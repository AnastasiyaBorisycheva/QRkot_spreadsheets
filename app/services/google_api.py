from datetime import datetime

from aiogoogle import Aiogoogle

from .constants import (PERMISSIONS_BODY, SPREADSHEET_BODY, TABLE_VALUES,
                        UPDATE_BODY)

FORMAT = "%Y-%m-%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')

    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = SPREADSHEET_BODY
    spreadsheet_body['properties'] = {
        "title": f"Отчёт на {now_date_time}",
        "locale": "ru_RU"
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:

    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    now_date_time = datetime.now().strftime(FORMAT)
    table_values = TABLE_VALUES
    table_values.insert(0, ["Отчёт от", now_date_time])

    for res in charity_projects:
        table_values.append(res)

    update_body = UPDATE_BODY
    update_body['values'] = table_values

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
