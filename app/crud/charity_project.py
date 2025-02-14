from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject

FORMAT = "%Y-%m-%d %H:%M:%S"


class CRUDCharityProject(CRUDBase):

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ):
        charity_projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    func.datetime(
                        CharityProject.create_date).label('createdate'),
                    func.datetime(
                        CharityProject.close_date).label('closedate'),
                    CharityProject.description]
            ).where(
                CharityProject.fully_invested == 1
            )
        )

        charity_projects = charity_projects.all()

        result_list = []

        for project in charity_projects:
            project_list = []
            createdate = datetime.strptime(project.createdate, FORMAT)
            closedate = datetime.strptime(project.closedate, FORMAT)

            delta = closedate - createdate

            project_list.append(project.name)
            project_list.append(delta)
            project_list.append(project.description)

            result_list.append(project_list)

        result_list.sort(key=lambda delta: delta[1])

        for res in result_list:
            days = res[1].days
            hours, remainder = divmod(res[1].seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            microseconds = res[1].microseconds
            res[1] = (f'{days} дней, '
                      f'{hours}:'
                      f'{minutes}:'
                      f'{seconds}:'
                      f'{microseconds}')

        return result_list


charity_project_crud = CRUDCharityProject(CharityProject)
