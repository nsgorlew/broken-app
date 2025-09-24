from .custom_exceptions import AuthenticationError
from .s3_connector import (
    create_async_boto3_session,
    search_s3_bucket,
    get_object_s3,
    upload_object_s3
)
from .supabase_connector import SupabaseConnector
import os

from dotenv import load_dotenv

os.environ["local"] = "true"  # for local dev
if os.environ["local"] == "true":
    load_dotenv(dotenv_path="../.env", override=True)

supabase_connector = SupabaseConnector()
