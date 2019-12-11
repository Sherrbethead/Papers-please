"""
Data and methods for bulletin and papers generation.
"""

from string import ascii_uppercase, digits
from datetime import date
from random import choice, choices, shuffle

from names import get_full_name
from faker import Faker

documents = (
    'passport',
    'certificate_of_vaccination',
    'access_permit',
    'grant_of_asylum',
    'diplomatic_authorization'
)
countries = (
    'Arstotzka',
    'Antegria',
    'Impor',
    'Kolechia',
    'Obristan',
    'Republia',
    'United Federation'
)
vaccinations = (
    'cholera',
    'hepatitis A',
    'hepatitis B',
    'HPV',
    'measles',
    'polio',
    'rubella',
    'tuberculosis',
    'tetanus',
    'typhus'
)
purposes = (
    'vacation',
    'visit',
    'work'
)


def get_comma_sep(lst):
    """Convert list to string with comma separation."""
    return ', '.join(lst)


def get_comma_split(name):
    """Convert string with comma separation to set of unique data."""
    return set(name.split(', '))


def make_choice(func):
    """
    Decorate function which return list (or tuple) and amount value.
    Return list with a given (or less than given) amount of unique items.
    """
    def wrapper(*args, **kwargs):
        obj, val = func(*args, **kwargs)
        return list(set(choices(obj, k=val)))
    return wrapper


def make_shuffle(lst, n):
    """Randomly mix entered list."""
    lst_to_mix = list(range(n))
    shuffle(lst_to_mix)
    return [lst[i] for i in lst_to_mix]


@make_choice
def add_countries(value):
    """
    Add random foreign countries from tuple of countries in a given amount.
    """
    return countries[1:], value


@make_choice
def add_vaccinations(value):
    """
    Add random vaccinations from tuple of vaccination in a given amount.
    """
    return vaccinations, value


def add_name_and_sex():
    """Add random name and related gender."""
    gender_dict = {
        'female': 'F',
        'male': 'M'
    }
    gender = choice(list(gender_dict))

    name = get_full_name(gender)
    return get_comma_sep(reversed(name.split())), gender_dict.get(gender)


def add_id_number():
    """Add random ID number which consists of two parts."""

    def parts():
        return ''.join(choice(ascii_uppercase + digits) for _ in range(5))

    return f'{parts()}-{parts()}'


def add_date(start, end):
    """Add random date and convert it to YY.MM.DD format."""
    random_date = Faker().date_between(start_date=start, end_date=end)
    return date.strftime(random_date, '%Y.%m.%d')
