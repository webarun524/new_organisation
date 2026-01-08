import logging
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

# 7 days in seconds
DEFAULT_EXPIRATION = 60 * 60 * 24 * 7
S3_REPORT_FOLDER = "final_reports"


class ReportUploader:
    def __init__(self, s3_client, bucket_name: str | None):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    @staticmethod
    def _create_file(file_content: str, file_name: str, file_type: str) -> Path:
        """
        Create a file in a temporary directory with the given content.
        Returns The absolute path to the created file
        """
        temp_dir = tempfile.gettempdir()
        file_path = Path(temp_dir) / f"{file_name}.{file_type}"

        file_path.write_text(file_content, encoding="utf-8")
        logger.info(f"Created file at {file_path}")

        return file_path

    def _upload_to_s3(self, path: Path) -> str:
        """
        Upload the zip file to S3.
        """

        if not path.exists():
            raise FileNotFoundError(f"Zip file not found: {path}")

        s3_key = f"{S3_REPORT_FOLDER}/{path.name}"

        logger.info(f"Uploading {path} to s3://{self.bucket_name}/{s3_key}")

        try:
            self.s3_client.upload_file(str(path), self.bucket_name, s3_key)
            logger.info(f"Successfully uploaded to s3://{self.bucket_name}/{s3_key}")
            return s3_key

        except (OSError, FileNotFoundError) as e:
            logger.error(f"Failed to upload to S3 due to file error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to upload to S3: {e}")
            raise

    def _get_presigned_url(
        self, object_name: str, expiration: int = DEFAULT_EXPIRATION
    ) -> str:
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )

    def main(self, html_report: str, file_name: str) -> str:
        """
        Main entry point.
        """
        # Create temp file
        file_path = self._create_file(
            file_content=html_report, file_name=file_name, file_type="html"
        )

        # Upload to S3
        s3_key = self._upload_to_s3(path=file_path)

        logger.info(
            f"Reports uploaded successfully to s3://{self.bucket_name}/{s3_key}"
        )

        return self._get_presigned_url(s3_key)
