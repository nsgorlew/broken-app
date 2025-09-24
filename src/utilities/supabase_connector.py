import asyncio
import os

from dotenv import load_dotenv
from gotrue.errors import AuthApiError
from structlog import get_logger
from supabase import (
    ASupabaseAuthClient,
    AsyncClient,
    acreate_client
)


os.environ["local"] = "true"  # for local dev
if os.environ["local"] == "true":
    load_dotenv(dotenv_path="../../.env", override=True)

logger = get_logger(src="utilities/supabase_connector.py")


class SupabaseConnector:

    client = None
    auth_client = None

    def __init__(self):
        asyncio.run(self.initialize_clients())

    async def initialize_clients(self):
        try:
            self.client = await self.create_client()
        except Exception as e:
            raise e
        """
        try:
            self.auth_client = await self.create_auth_client()
        except Exception as ex:
            raise ex
        """

    @staticmethod
    async def create_client() -> AsyncClient:
        return await acreate_client(
            supabase_url=os.environ["SUPABASE_URL"],
            supabase_key=os.environ["SUPABASE_KEY"]
        )

    """
    @staticmethod
    async def create_auth_client() -> ASupabaseAuthClient:
        return await ASupabaseAuthClient(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_KEY"]
        )
    """

    async def create_new_user(self, email: str, password: str):
        response = await self.client.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {
                    "email_redirect_to": f"{os.environ["FRONTEND_LOGIN_URL"]}"
                }
            }
        )
        return response

    async def sign_in_with_password(self, email: str, password: str):
        try:
            response = await self.client.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )
            # get access token with response.session.access_token
            # get refresh token with response.session.refresh_token
            return response
        except AuthApiError as ae:
            # logger.error("login failed")
            raise ae

    async def sign_out(self):
        response = await self.client.sign_out()
        return response

    async def reset_password_request(self, email: str, reset_password_url: str):
        response = await self.client.auth.reset_password_for_email(
            email,
            {
                "redirect_to": reset_password_url,
            }
        )
        return response

    async def update_user_password(self, new_password: str):
        response = self.client.auth.update_user(
            {"password": new_password}
        )
        return response

    async def retrieve_user(self, current_jwt: str):
        response = await self.client.auth.get_user(current_jwt)
        return response

    async def refresh_session(self, refresh_token: str):
        response = self.client.auth.refresh_session(refresh_token)
        return response


if __name__ == "__main__":
    supabase = SupabaseConnector()

    test_response = asyncio.run(
        supabase.sign_in_with_password(
            email="nsgorlew@gmail.com",
            password="testpassword"
        )
    )
    print(f"Access token: {test_response.session.access_token}")
    print(f"Refresh token: {test_response.session.refresh_token}")
