from dual_universe.src.DUCharacters import DUCharacters
from src.utils import ClientManager


class Main:

    pass


if __name__ == "__main__":
    # TODO: Database initial setup
    # TODO: Initial File creation
    client = ClientManager()
    client.start_application()
    character = DUCharacters()
    character.login()
    ...
