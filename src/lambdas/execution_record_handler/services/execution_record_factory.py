import os
from datetime import datetime, timezone
from uuid import uuid4

from ..const.env_variable_keys import HASH_KEY_NAME_ENV_VAR
from ..models.execution_record import ExecutionRecordModel


class ExecutionRecordFactory:
    @staticmethod
    def make_test_execution_record(payload: dict) -> dict:
        hash_record_name = os.environ.get(HASH_KEY_NAME_ENV_VAR)

        # fetch existing record from DynamoDB if 'Id' exists
        record = {}
        record_id = payload.get(hash_record_name)
        if record_id:
            existing_record = ExecutionRecordModel.get(record_id)
            record = existing_record.to_dict()

        # merge updates from payload
        record.update(payload)
        if not record.get(hash_record_name):
            record[hash_record_name] = str(uuid4())

        # update & convert dates
        now = datetime.now(timezone.utc)
        if not record.get("CreatedAt"):
            record["CreatedAt"] = now
        record["UpdatedAt"] = now
        for ts_field in ["CreatedAt", "UpdatedAt"]:
            if ts_field in record and isinstance(record[ts_field], datetime):
                record[ts_field] = record[ts_field].isoformat()

        return record
