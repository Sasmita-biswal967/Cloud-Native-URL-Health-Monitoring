import boto3
import json
from datetime import datetime

s3 = boto3.client("s3")

BUCKET_NAME = "cloud-url-monitor-reports-12345"


def upload_monitor_report(data):

    filename = (
        f"report_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ".json"
    )

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    s3.upload_file(
        filename,
        BUCKET_NAME,
        filename
    )

    return {
        "message": "Uploaded successfully",
        "file": filename
    }