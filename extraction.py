import boto3
from pathlib import Path
s3 = boto3.client("s3")
local_path = Path("db.sqlite")
s3.download_file(
    "carolebrun",
    "NLP_3A/sciencespo-archelec-20260129-223203.sqlite",
    local_path
)
print("1")
db_path = Path("/home/onyxia/work/NLP_3A/sciencespo-archelec-20260129-223203.sqlite")