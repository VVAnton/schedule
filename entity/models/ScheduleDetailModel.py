from sqlalchemy.sql import any_
from settings import logger

from .BaseModel import BaseModel

from entity.validators import ScheduleDetailCreateSchema, ScheduleDetailSchema
from entity.schedule import Schedule
from entity.schDetail import SCHDetail

from common.managers.sessionManager import SessionManager


# business-model by entity User
class ScheduleDetailModel(BaseModel):
    def __init__(self, select_fields: set=set()):
        """
        :param select_fields: set, list fields for result
        """
        super().__init__(
            entity_cls=SCHDetail,
            all_fields=(
                'id',
                'time',
                'description',
                'members',
                'schedule_id',
                'created_at',
                'updated_at',
            ),
            select_fields=select_fields
        )

    # Schema for create
    def _get_create_schema(self):
        return ScheduleDetailCreateSchema()

    # Schema for update
    def _get_update_schema(self):
        return ScheduleDetailSchema()

    # GET Entity
    async def get_entities(self, ids: list, schedule_ids: set = None, filter_name: str = None) -> tuple:
        # result vars
        result = []
        errors = []

        # check permissions for schedule_ids by account
        if schedule_ids:
            # select schedules by ids
            schedule_items = await Schedule.select_by_ids(model_ids=schedule_ids)
            # get allowed schedule_ids ids and errors by schedule_ids
            allowed_schedule_ids, errs = self.get_allowed_ids_by_list(all_ids=schedule_ids, items=schedule_items)
            # add ids-errors in all errors
            errors.extend(errs)

        # get all schedule_ids by account
        else:
            schedule_items = await Schedule.select_all()
            # allowed schedule_ids
            allowed_schedule_ids = [schedule_item['id'] for schedule_item in schedule_items]

        # conditions by select users
        conditions = []

        # condition by allowed Fleets
        conditions.append(self.entity_cls.schedule_id == any_(allowed_schedule_ids))

        # condition by selector ids
        if ids:
            conditions.append(self.entity_cls.id == any_(ids))

        # condition by selector name
        if filter_name:
            conditions.append(self.entity_cls.name.contains(filter_name))

        # select by conditions
        records = await self.entity_cls.select_where(
            str_fields=self.select_fields,
            conditions=conditions
        )

        # ids by selected items
        select_ids = set()
        # format data
        format_result = dict()
        # generate result list
        for record in records:
            select_ids.add(record['id'])
            format_result.setdefault(record['schedule_id'], [])
            format_result[record['schedule_id']].append(self.get_result_item(record, self.select_fields))

        # add not selected items in errors
        if ids:
            # get ids not selected
            ids = set(ids)
            ids_diff = ids.difference(select_ids)
            # add errors by not found ids
            for id_diff in ids_diff:
                errors.append(
                    self.get_error_item(selector='id', reason='Schedule or schedule-detail is not found', value=id_diff))
        result.append(format_result)
        return result, errors

    # CREATE Entity
    async def create_entity(self, data: dict, **kwargs) -> tuple:
        result, errors = await super().create_entity(data, **kwargs)

        return result, errors

    # UPDATE Entity
    async def update_entity(self, data: dict, **kwargs) -> tuple:
        # update
        result, errors = await super().update_entity(data, **kwargs)

        return result, errors