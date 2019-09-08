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
CREATE VERTEX Region SET name = 'World', uuid = 'c542cfe3-1829-45dd-a636-98ba2f9860b7'

CREATE CLASS Country EXTENDS GeographicArea
# Most countries have ISO 3166-1 alpha2 and alpha3 codes.
# When the code exists, it is unique.
CREATE PROPERTY Country.alpha2 String
CREATE INDEX Country.alpha2 UNIQUE METADATA {ignoreNullValues: true}
CREATE PROPERTY Country.alpha3 String
CREATE INDEX Country.alpha3 UNIQUE METADATA {ignoreNullValues: true}
