#!/usr/bin/env python
"""Contains the definition for CharacterGenerator"""

import os
import random

_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_TRAITS_CSV = os.path.join(_BASE_DIR, 'traits.csv')
DEFAULT_FIRST_NAMES_CSV = os.path.join(_BASE_DIR, 'baby-names.csv')
DEFAULT_CHARACTERISTICS_CSV = os.path.join(_BASE_DIR, 'physical.csv')

class CharacterGenerator:
    """Generates a Monster of the Week bystander"""
    def __init__(self, traits_csv=DEFAULT_TRAITS_CSV,
                 first_names_csv=DEFAULT_FIRST_NAMES_CSV,
                 characteristics_csv=DEFAULT_CHARACTERISTICS_CSV):
        self.traits = {}
        self.traits_by_tag = {}
        self.names = []
        self.characteristics = {}
        self.characteristics_by_tag = {}

        self.default_trait_distribution = {
            "positive": 1,
            "negative": 1,
            "neutral": 1,
            "random": 1,
        }

        self.default_characteristic_distribution = {
            "eye colour": 1,
            "skin colour": 1,
            "body type": 1,
            "others": 3,
        }

        self.bystander_types = [
            ('Busybody', 'interfere in other people\'s plans'),
            ('Detective', 'rule out explanations'),
            ('Gossip', 'pass on rumours'),
            ('Helper', 'join the hunt'),
            ('Innocent', 'do the right thing'),
            ('Official', 'be suspicious'),
            ('Skeptic', 'deny supernatural explanations'),
            ('Victim', 'put themselves in danger'),
            ('Witness', 'reveal information'),
        ]

        if traits_csv is not None:
            self.add_traits_from_csv_file(traits_csv)

        if first_names_csv is not None:
            self.add_first_names_from_csv_file(first_names_csv)

        if characteristics_csv is not None:
            self.add_characteristics_from_csv_file(characteristics_csv)


    def add_traits_from_csv_file(self, csv_filename):
        """Adds character traits from a csv file"""
        with open(csv_filename) as file_handle:
            for line in file_handle:
                elements = line.strip('\n').split(',')
                trait = elements[0]
                tags = elements[1:]
                self.add_trait(trait, tags)

    def add_first_names_from_csv_file(self, csv_filename,
                                      year_range=None):
        """Selects names from a csv file, within a certain year range"""
        if year_range is None:
            year_range = [1920, 2020]
        with open(csv_filename) as file_handle:
            data = file_handle.read().splitlines()[1:]
            for line in data:
                year, name, _, _ = line.split(',')
                year = int(year)
                name = name.replace('"', '')
                if year_range[0] <= year <= year_range[1]:
                    if name not in self.names:
                        self.names.append(name)

    def add_characteristics_from_csv_file(self, csv_filename):
        """Adds physical characteristics from a csv file"""
        with open(csv_filename) as file_handle:
            for line in file_handle:
                elements = line.strip('\n').split(',')
                characteristic = elements[0]
                tags = elements[1:]
                self.add_characteristic(characteristic, tags)

    def add_trait(self, trait, tags=None):
        """Adds or updates a trait"""
        if tags is None:
            tags = []

        if trait not in self.traits:
            self.traits[trait] = tags
        else:
            self.traits[trait] += tags

        for tag in tags:
            if tag not in self.traits_by_tag:
                self.traits_by_tag[tag] = [trait]
            else:
                self.traits_by_tag[tag].append(trait)

    def add_characteristic(self, characteristic, tags=None):
        """Adds or updates a characteristic"""
        if tags is None:
            tags = []

        if characteristic not in self.characteristics:
            self.characteristics[characteristic] = tags
        else:
            self.characteristics[characteristic] += tags

        for tag in tags:
            if tag not in self.characteristics_by_tag:
                self.characteristics_by_tag[tag] = [characteristic]
            else:
                self.characteristics_by_tag[tag].append(characteristic)


    def get_traits(self, trait_distribution=None):
        """Returns traits according to a supplied distribution"""
        if trait_distribution is None:
            trait_distribution = self.default_trait_distribution

        traits = []
        for tag, count in trait_distribution.items():
            if tag == 'random':
                all_traits = list(self.traits.keys())
                traits += random.choices(all_traits, k=count)
            else:
                traits += random.choices(self.traits_by_tag[tag], k=count)

        return traits

    def get_characteristics(self, characteristic_distribution=None):
        """Returns traits according to a supplied distribution"""
        if characteristic_distribution is None:
            characteristic_distribution = self.default_characteristic_distribution

        characteristics = []

        other_keys = ["eye colour", "skin colour", "body type"]

        for tag, count in characteristic_distribution.items():
            if tag == 'others':
                others = [tag for tag in self.characteristics_by_tag.keys()
                          if tag not in other_keys]

                tags = random.choices(others, k=count)
                for tag in tags:
                    char = random.choice(self.characteristics_by_tag[tag])
                    characteristics.append((char, tag))
            else:
                tag_characteristics = self.characteristics_by_tag[tag]
                for characteristic in random.choices(tag_characteristics,
                                                     k=count):
                    characteristics.append((characteristic, tag))

        output = {}
        for key, value in characteristics:
            if value not in output:
                output[value] = [key]
            else:
                output[value].append(key)

        for key in output.keys():
            output[key] = ', '.join(output[key])

        return output

    def build_character(self, trait_distribution=None,
                        characteristic_distribution=None):
        """builds a random character"""
        bystander_type = random.choice(self.bystander_types)
        return {
            'name': random.choice(self.names),
            'type': bystander_type[0],
            'motivation': bystander_type[1],
            'traits': self.get_traits(trait_distribution),
            'characteristics': self.get_characteristics(characteristic_distribution),
        }

    def __iter__(self):
        while True:
            yield self.build_character()


if __name__ == '__main__':
    generator = CharacterGenerator()
    it = iter(generator)

    for i in range(4):
        print(next(it))
