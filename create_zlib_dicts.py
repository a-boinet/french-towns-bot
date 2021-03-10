import pathlib

from tqdm import tqdm
from utils.utils import generate_distrib_dict, get_list_from_file


if __name__ == "__main__":
    liste_regions = [
        "Auvergne-Rhône-Alpes",
        "Bourgogne-Franche-Comté",
        "Bretagne",
        "Centre-Val de Loire",
        "Corse",
        "Grand Est",
        "Guadeloupe",
        "Guyane",
        "Hauts-de-France",
        "Ile-de-France",
        "La Réunion",
        "Martinique",
        "Mayotte",
        "Normandie",
        "Nouvelle-Aquitaine",
        "Occitanie",
        "Pays de la Loire",
        "Provence-Alpes-Côte d'Azur",
    ]

    regions_dict = {}

    for region in liste_regions:
        data = get_list_from_file(
            f"{pathlib.Path(__file__).parent.absolute()}/resources/regions_france/"
            + region.replace("'", "-")
            + ".txt"
        )
        data.pop()
        print(len(data), region)
        regions_dict[region] = data

    print("\nStarting dict generation\n")

    for region in tqdm(regions_dict.keys()):
        print(f"Generation dict for {region}")
        substitute_name = region.replace("'", "-")
        generate_distrib_dict(
            name_list=regions_dict[region],
            file_path=f"{pathlib.Path(__file__).parent.absolute()}/resources/regions_france_dict/distrib_dict_{substitute_name}.zlib",
        )
