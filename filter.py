import json
import re


def load_data(path, name_of_data):
    with open(path) as json_data:
        data = json.load(json_data)

        acc_ids_before = []
        acc_ids_after = []

        profiles = {}
        for name, profile in data.items():
            if len(profile['image_urls']) > 0:
                matches = re.findall('https://images-ssl.gotinder.com/.+/', profile['image_urls'][0])

                if len(matches) == 1:
                    acc_id = matches[0][32:-1]

                    acc_ids_before.append(acc_id)

                    if acc_id not in acc_ids_after:
                        acc_ids_after.append(acc_id)
                        profiles[acc_id] = profile

        with open(path[:-5] + '_filtered.json', 'w') as f:
            json.dump(profiles, f)

        print(f'{name_of_data}: uncleaned: {len(data.items())} -> cleaned: {len(acc_ids_before)} -> duplicates filtered: {len(set(acc_ids_after))}')

        return acc_ids_after


if __name__ == "__main__":
    ids_man2man = load_data('/Users/alexanderfuchs/Desktop/WS_24_25/TinderBotz/data_man2man/geomatches/geomatches.json', 'man2man')
    ids_man2woman = load_data('/Users/alexanderfuchs/Desktop/WS_24_25/TinderBotz/data_man2woman/geomatches/geomatches.json', 'man2woman')
    ids_woman2woman = load_data('/Users/alexanderfuchs/Desktop/WS_24_25/TinderBotz/data_woman2woman/geomatches/geomatches.json', 'woman2woman')
    ids_woman2man = load_data('/Users/alexanderfuchs/Desktop/WS_24_25/TinderBotz/data_woman2man/geomatches/geomatches.json', 'woman2man')

    print(f'')

    print(f'unique man in man2man (compared to woman2man): {(len(set(ids_man2man + ids_woman2man)) - len(ids_woman2man)) / len(ids_man2man)}')
    print(f'unique man in woman2man (compared to man2man): {(len(set(ids_woman2man + ids_man2man)) - len(ids_man2man)) / len(ids_woman2man)}')
    print(f'unique woman in woman2woman (compared to man2woman): {(len(set(ids_woman2woman + ids_man2woman)) - len(ids_man2woman)) / len(ids_woman2woman)}')
    print(f'unique woman in man2woman (compared to woman2woman): {(len(set(ids_man2woman + ids_woman2woman)) - len(ids_woman2woman)) / len(ids_man2woman)}')
