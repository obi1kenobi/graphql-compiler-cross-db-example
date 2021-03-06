ALTER DATABASE TIMEZONE UTC
ALTER DATABASE VALIDATION True

CREATE CLASS Entity EXTENDS V ABSTRACT
CREATE PROPERTY Entity.uuid String
ALTER PROPERTY Entity.uuid MANDATORY True
CREATE INDEX Entity.uuid UNIQUE_HASH_INDEX
CREATE PROPERTY Entity.name String
ALTER PROPERTY Entity.name MANDATORY True
CREATE INDEX Entity.name NOTUNIQUE

CREATE CLASS GeographicArea EXTENDS Entity ABSTRACT

# Geographical regions, such as "Southern Europe" or "Asia".
CREATE CLASS Region EXTENDS GeographicArea

CREATE CLASS Country EXTENDS GeographicArea
# Most countries have ISO 3166-1 alpha2 and alpha3 codes.
# When the code exists, it is unique.
CREATE PROPERTY Country.alpha2 String
CREATE INDEX Country.alpha2 UNIQUE METADATA {ignoreNullValues: true}
CREATE PROPERTY Country.alpha3 String
CREATE INDEX Country.alpha3 UNIQUE METADATA {ignoreNullValues: true}

# An edge that points from a parent GeographicArea to a child (sub) GeographicArea,
# enforcing that any two areas may be connected by at most one such edge.
CREATE CLASS GeographicArea_SubArea EXTENDS E
CREATE PROPERTY GeographicArea_SubArea.out LINK GeographicArea
CREATE PROPERTY GeographicArea_SubArea.in LINK GeographicArea
CREATE INDEX GeographicArea_SubArea_Unique ON GeographicArea_SubArea (in, out) UNIQUE_HASH_INDEX
