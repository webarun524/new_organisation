import logging
import zipfile
from pathlib import Path

from ..models.enums import FolderName
from ..models.errors import MissingReportFiles, MissingReportsDirectory

logger = logging.getLogger(__name__)

# 5 days in seconds
DEFAULT_EXPIRATION = 60 * 60 * 24 * 5


class ReportUploader:
    def __init__(self, s3_client, bucket_name: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def _validate_reports_directory(self, reports_dir: Path):
        """
        Validate that reports directory exists.
        """
        if not reports_dir.exists():
            logging.error(f"Reports directory not found: {reports_dir}")
            raise MissingReportsDirectory

        if not reports_dir.is_dir():
            logging.error(f"Reports path is not a directory: {reports_dir}")
            raise MissingReportsDirectory

        if not any(reports_dir.iterdir()):
            logging.warning(f"Reports directory is empty: {reports_dir}")
            raise MissingReportFiles

    def _create_zip_archive(self, zip_filename: str, reports_dir: Path) -> Path:
        """
        Create a zip archive of the reports directory.
        """

        zip_path = Path(zip_filename)

        logger.info(f"Creating zip archive: {zip_path}")

        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in reports_dir.rglob("*"):
                    if file_path.is_file():
                        # Skip .gitkeep and other git metadata files
                        if file_path.name in [".gitkeep", ".gitignore"]:
                            logger.debug(
                                f"Skipping git metadata file: {file_path.name}"
                            )
                            continue

                        arcname = file_path.relative_to(reports_dir.parent)
                        zipf.write(file_path, arcname=arcname)
                        logger.debug(f"Added to zip: {arcname}")

            logger.info(
                f"Zip archive created successfully: {zip_path} "
                f"({zip_path.stat().st_size} bytes)"
            )
            return zip_path

        except (OSError, IOError) as e:
            logger.error(f"Failed to create zip archive due to I/O error: {e}")
            raise
        except zipfile.BadZipFile as e:
            logger.error(f"Failed to create zip archive due to invalid zip format: {e}")
            raise

    def _upload_to_s3(self, zip_path: Path, folder: str) -> str:
        """
        Upload the zip file to S3.
        """

        if not zip_path.exists():
            raise FileNotFoundError(f"Zip file not found: {zip_path}")

        s3_key = f"{folder}/{zip_path.name}"

        logger.info(f"Uploading {zip_path} to s3://{self.bucket_name}/{s3_key}")

        try:
            self.s3_client.upload_file(str(zip_path), self.bucket_name, s3_key)
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

    def main(
        self, test_marker: str, execution_id: str, reports_dir: str = "./reports"
    ) -> str:
        """
        Main entry point.
        """

        folder = FolderName[test_marker].value
        reports_dir_path = Path(reports_dir)
        zip_filename = f"{execution_id}.zip"

        # Validate reports directory
        self._validate_reports_directory(reports_dir_path)

        # Create zip archive
        zip_path = self._create_zip_archive(zip_filename, reports_dir_path)

        # Upload to S3
        s3_key = self._upload_to_s3(zip_path, folder)

        logger.info(
            f"Reports uploaded successfully to s3://{self.bucket_name}/{s3_key}"
        )

        return self._get_presigned_url(s3_key)
