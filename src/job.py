import boto3


class Job:

    def __init__(self):
        pass

    def get_object_from_s3(self, bucket, key):
        client = boto3.client("s3")
        response = client.get_object(Bucket=bucket, Key=key)
        obj = response['Body'].read()
        return obj

    def prepare_data(self, data):
        prepared_data = data  # Data would be preprocessed here
        return prepared_data

    def predict(self, prepared_data):
        model_object = self.get_object_from_s3(
            bucket="my-bucket",
            key="model_object.tar.gz"
        )

        loaded_model = ModelLoader(model_object)

        prediction = loaded_model.predict(prepared_data)

        return prediction

