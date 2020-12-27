class Config:

    path = None

    sources = ["koha_api", "db"]

    source = None

    config = {
        "koha_api": {
            "url": None
        },
        "db": {
            "host": None,
            "user": None,
            "password": None,
            "port": None,
            "schema": None
        },
        "target": {
            "account_id": None,
            "url_status": None,
            "url_add": None,
            "key": None,
            "secret": None,
            "block": None,
        }
    }

    def get_instance(self):
        pass
