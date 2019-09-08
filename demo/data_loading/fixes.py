def fix_alpha2_value(alpha2):
    """Return a fixed two-letter uppercase alpha2, or None if unfixable."""
    if alpha2 is None:
        return None

    fixed_alpha2 = alpha2.strip()
    if not fixed_alpha2.isalpha():
        return None

    fixed_alpha2 = fixed_alpha2.upper()
    assert len(fixed_alpha2) == 2
    return fixed_alpha2


def fix_alpha3_value(alpha3):
    """Return a fixed three-letter uppercase alpha2, or None if unfixable."""
    if alpha3 is None:
        return None

    fixed_alpha3 = alpha3.strip()
    if not fixed_alpha3.isalpha():
        return None

    fixed_alpha3 = fixed_alpha3.upper()
    assert len(fixed_alpha3) == 3
    return fixed_alpha3


def fix_iata_or_icao_code(code):
    if code is None:
        return code

    code = code.strip()
    if code and code.isalnum():
        return code
    else:
        return None


def fix_string_value(value):
    if value is None:
        return None

    value = value.strip()
    if not value:
        return None

    return value


# Add explicit overrides for bad data in airlines and airport country names.
hardcoded_alpha2_values = {
    'ALASKA': 'US',
    'ALASKA PACIFIC': 'US',
    'APPALACHIAN': 'US',
    'ATLANTIC NICARAGUA': 'NI',
    'ATLANTIS CANADA': 'CA',
    'AVEMEX': 'MX',
    'AVIANCA': 'CO',
    'Bolivia': 'BO',
    'Brunei': 'BN',
    'Burma': 'MM',
    'Canadian Territories': 'CA',
    'Cape Verde': 'CV',
    'Congo (Brazzaville)': 'CD',
    'Congo (Kinshasa)': 'CD',
    "Cote d'Ivoire": 'CI',
    'Czech Republic': 'CZ',
    'Democratic Republic of Congo': 'CD',
    'East Timor': 'TP',
    'Falkland Islands': 'FK',
    'Hong Kong': 'HK',
    'Hong Kong SAR of China': 'HK',
    'Iran': 'IR',
    'Ivory Coast': 'CI',
    'Johnston Atoll': 'UM',
    'Lao Peoples Democratic Republic': 'LA',
    'Laos': 'LA',
    'Macao': 'MO',
    'Macau': 'MO',
    'Macedonia': 'MK',
    'Micronesia': 'FM',
    'Midway Islands': 'UM',
    'Moldova': 'MD',
    'Netherland': 'NL',
    'North Korea': 'KP',
    'Republic of the Congo': 'CD',
    'Russia': 'RU',
    'Russia]]': 'RU',
    'SWISSBIRD': 'CH',
    'Somali Republic': 'SO',
    'South Korea': 'KR',
    'Svalbard': 'SJ',
    'Swaziland': 'SZ',
    'Syria': 'SY',
    'Tanzania': 'TZ',
    'UNited Kingdom': 'GB',
    'United Kingdom': 'GB',
    'United States': 'US',
    'Venezuela': 'VE',
    'Vietnam': 'VN',
    'Virgin Islands': 'VI',
    'Wake Island': 'UM',
    'Wallis and Futuna': 'WF',
}
