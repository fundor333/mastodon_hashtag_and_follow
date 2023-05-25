import click
import requests


class MastodonSocial:
    def __init__(self, token: str, domain: str) -> None:
        self.token = token
        self.domain = domain

    def follow(self, account_id: str) -> None:
        url = f"https://{self.domain}/api/v1/accounts/{account_id}/follow"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print("Success")

    def get_users_from_hashtags(self, hashtag: str) -> None:
        url = f"https://{self.domain}/api/v1/timelines/tag/{hashtag}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return list({user["account"]["id"] for user in response.json()})
        else:
            raise Exception("Error")

    def run_hashtag(self, hashtag: str) -> None:
        users = self.get_users_from_hashtags(hashtag)
        for user in users:
            self.follow(user)


@click.command()
@click.option("--token", help="Token for Mastodon")
@click.option("--domain", default="mastodon.social", help="Mastodon server")
@click.option(
    "--hashtag", default=1, help="The hash tag to find the followers"
)
def run(token, domain, hashtag):
    ms = MastodonSocial(token=token, domain=domain)
    ms.run_hashtag(hashtag=hashtag)


if __name__ == "__main__":
    run()
