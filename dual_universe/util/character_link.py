from time import sleep

from dual_universe.src.DUCharacters import DUCharacters
from dual_universe.src.querysets import CharacterQuerySet


def character_link():
    all_active_characters = (
        CharacterQuerySet.get_active_characters()
    )  # Get the characters dictionary
    # loop over all the accounts
    for character in all_active_characters:
        has_gametime = DUCharacters().login(character)

        if not has_gametime:
            continue
        sleep(30)

        DUCharacters().logout()


if __name__ == "__main__":
    character_link()
