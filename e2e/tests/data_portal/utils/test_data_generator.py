import json
import re
from uuid import uuid4

from e2e.tests.data_portal.mock import manifest, record, workflow
from e2e.tests.data_portal.utils.osdu_data_unit import OsduDataUnit


class DataGenerator:
    """Generate unique test data for OSDU integration tests."""

    def __init__(self, base_api_url: str):
        # Extract domain from base_api_url
        parts = base_api_url.split("//")
        if len(parts) < 2:
            raise ValueError(f"Invalid base_api_url: {base_api_url}")
        self.domain = parts[1]

    def get_unique_name(self, prefix: str = "", suffix: str = "") -> str:
        """
        Generate a unique name using UUID (first 8 chars).

        Args:
            prefix: String to prepend to unique ID
            suffix: String to append to unique ID

        Returns:
            Unique name in format: prefix + uuid + suffix
        """
        unique = str(uuid4()).split("-")[0]
        return f"{prefix}{unique}{suffix}"

    def _replace(self, data: dict, replacements: dict[str, str]) -> dict:
        """
        Replace placeholders in data structure using regex.

        Args:
            data: Dict or list to perform replacements on
            replacements: Dict mapping placeholder names to values

        Returns:
            Updated data structure with replacements applied
        """
        data_string = json.dumps(data, indent=2)
        for key, value in replacements.items():
            data_string = re.sub(key, value, data_string)
        return json.loads(data_string)

    def get_record(self) -> OsduDataUnit:
        """
        Generate a unique OSDU well master-data record.

        Returns:
            OsduDataUnit containing record with unique ID
        """
        record_id = self.get_unique_name("osdu:master-data--Well:")
        updated_record = self._replace(
            record.RECORD_DATA, {"RECORD_ID": record_id, "DOMAIN": self.domain}
        )
        return OsduDataUnit(record_id, updated_record)

    def get_manifest(self) -> OsduDataUnit:
        """
        Generate a unique OSDU manifest.

        Returns:
            OsduDataUnit containing manifest data
        """
        updated_manifest = self._replace(
            manifest.MANIFEST_DATA, {"DOMAIN": self.domain}
        )
        return OsduDataUnit("", updated_manifest)

    def get_workflow(self) -> OsduDataUnit:
        """
        Generate a unique OSDU workflow.

        Returns:
            OsduDataUnit containing workflow with unique name
        """
        workflow_id = self.get_unique_name("workflow-")
        updated_workflow = self._replace(
            workflow.WORKFLOW_DATA,
            {"WORKFLOW_NAME": workflow_id, "DOMAIN": self.domain},
        )
        return OsduDataUnit(workflow_id, updated_workflow)
