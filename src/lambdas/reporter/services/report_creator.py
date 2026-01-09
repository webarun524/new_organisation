import os
from datetime import datetime

from jinja2 import Template


class ReportCreator:
    def __init__(self, record: dict) -> None:
        self.record = record

    def _calculate_duration(self) -> str:
        created_at_str = self.record.get("CreatedAt")
        updated_at_str = self.record.get("UpdatedAt")

        if not created_at_str or not updated_at_str:
            return "unknown"

        try:
            created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            updated_at = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))

            delta = updated_at - created_at
            total_seconds = int(delta.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            return f"{hours}Hours {minutes}minutes"
        except (ValueError, AttributeError):
            return "unknown"

    def to_json(self, report_url: str):
        """
        Returns json that can be pushed as message to SNS
        Requires report_url that is full report uploaded to s3
        """
        execution_duration = self._calculate_duration()
        return {
            "status": self.record.get("Status", "unknown"),
            "failure_reason": self.record.get("failure_reason", "unknown"),
            "report_url": report_url,
            "report_id": self.record.get("Id", "unknown"),
            "started_at": self.record.get("CreatedAt"),
            "finished_at": self.record.get("UpdatedAt"),
            "duration": execution_duration,
            "test_results": {
                "operations_portal": 45,
                "data_portal": 0,
            },
        }

    def to_html(self) -> str:
        """
        Prepares detailed final report in html format
        """
        try:
            template_path = os.path.join(
                os.path.dirname(__file__), "../templates/template.html"
            )
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()

            template = Template(template_content)

            # Add duration to the record for template rendering
            self.record["duration"] = self._calculate_duration()

            report = template.render(self.record)
            return report
        except Exception as e:
            return f"<html><body>Error generating report: {str(e)}</body></html>"
