import aioboto3


def create_async_boto3_session():
    return aioboto3.Session()


async def search_s3_bucket(
        s3_session,
        bucket: str,
        keyword: str,
        prefix: str = None
) -> list[str]:
    try:
        async with s3_session.resource("s3") as s3:
            # get list of objects in s3 bucket
            response = await s3.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix
            )

            # filter by keyword
            search_results = []
            for hit in response["Contents"]:
                if keyword in hit["Key"]:
                    search_results.append(hit["Key"])

            return search_results
    except Exception as e:
        raise e


async def get_object_s3(bucket: str, key: str, s3_session):
    try:
        async with s3_session.resource("s3") as s3:
            response = await s3.get_object(
                Bucket=bucket,
                Key=key
            )

            obj = response["Body"].read().decode("utf-8")
            return obj

    except Exception as e:
        raise e


async def upload_object_s3(
        s3_session,
        filename: str,
        bucket: str,
        prefix: str = None
) -> None:
    try:
        async with s3_session.resource("s3") as s3:
            if prefix:
                key = f"{prefix}/{filename}"
            else:
                key = filename

            await s3.upload_fileobj(
                Bucket=bucket,
                Key=key
            )
    except Exception as e:
        raise e
