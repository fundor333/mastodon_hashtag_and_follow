from typing import Annotated
import typer
import requests
from rich.console import Console
from rich.table import Table
import logging

logger = logging.getLogger(__name__)
app = typer.Typer()


class MastodonSocial:
    def __init__(self, token: str, domain: str) -> None:
        self.token = token
        self.domain = domain

    def follow(self, account_id: str) -> None:
        url = f"https://{self.domain}/api/v1/accounts/{account_id}/follow"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(f"Success: {account_id}")
            print(response.json())
            logger.info("Success")

    def get_users_from_hashtags(self, hashtag: str) -> None:
        url = f"https://{self.domain}/api/v1/timelines/tag/{hashtag}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return list({user["account"]["id"] for user in response.json()})
        else:
            raise Exception("Error")

    def get_list(self) -> list[dict]:
        url = f"https://{self.domain}/api/v1/lists"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error")

    def run_hashtag_follow(self, hashtag: str) -> None:
        users = self.get_users_from_hashtags(hashtag)
        for user in users:
            self.follow(user)

    def add_user_to_list(self, list_id: str, list_users_id: list[str]) -> None:
        url = f"https://{self.domain}/api/v1/lists/{list_id}/accounts"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(
            url, headers=headers, data={"account_ids": list_users_id}
        )
        if response.status_code == 200:
            logger.info("Success")
        else:
            logger.error(response.json())
            raise Exception("Error")

    def run_hashtag_follow_list(self, hashtag: str, list_id: str) -> None:
        users = self.get_users_from_hashtags(hashtag)
        self.add_user_to_list(list_id, users)


@app.command()
def get_lists(
    token: Annotated[str, typer.Argument(help="Token for Mastodon")],
    domain: Annotated[
        str, typer.Argument(help="Mastodon Server")
    ] = "mastodon.social",
):
    ms = MastodonSocial(token=token, domain=domain)
    console = Console()
    table = Table()
    table.add_column("Id")
    table.add_column("Title")
    for e in ms.get_list():
        table.add_row(e["id"], e["title"])
    console.print(table)


@app.command()
def add_list_from_hashtag(
    token: Annotated[str, typer.Argument(help="Token for Mastodon")],
    hashtag: Annotated[
        str, typer.Argument(help="The hash tag to find the followers")
    ],
    list_id: Annotated[
        str, typer.Argument(help="The id of the list to add the followers")
    ],
    domain: Annotated[
        str, typer.Argument(help="Mastodon Server")
    ] = "mastodon.social",
):
    ms = MastodonSocial(token=token, domain=domain)
    users = ms.get_users_from_hashtags(hashtag)
    ms.add_user_to_list(list_id, users)


@app.command()
def follow_from_hashtag(
    token: Annotated[str, typer.Argument(help="Token for Mastodon")],
    hashtag: Annotated[
        str, typer.Argument(help="The hash tag to find the followers")
    ],
    domain: Annotated[
        str, typer.Argument(help="Mastodon Server")
    ] = "mastodon.social",
):
    ms = MastodonSocial(token=token, domain=domain)
    ms.run_hashtag_follow(hashtag=hashtag)


if __name__ == "__main__":
    app()
