from uuid import uuid4

from demo.data_loading.data_fetching import get_countries_data
from demo.data_loading.fixes import fix_alpha2_value, fix_alpha3_value, fix_string_value
from demo.server.config import get_pyorient_client


def load_countries_and_regions(countries_df):
    graph = get_pyorient_client()

    country_cls = graph.registry['Country']
    region_cls = graph.registry['Region']
    subarea_cls = graph.registry['GeographicArea_SubArea']

    area_name_and_type_to_vertex = dict()

    # Create all countries.
    for _, country_item in countries_df.iterrows():
        name = fix_string_value(country_item['CLDR display name'])
        uuid = str(uuid4())
        alpha2 = fix_alpha2_value(country_item['ISO3166-1-Alpha-2'])
        alpha3 = fix_alpha3_value(country_item['ISO3166-1-Alpha-3'])

        props = {
            'name': name,
            'uuid': uuid,
            'alpha2': alpha2,
            'alpha3': alpha3,
        }
        vertex = graph.create_vertex(country_cls, **props)
        area_name_and_type_to_vertex[(name, 'Country')] = vertex

    # Create all non-country regions.
    for _, country_item in countries_df.iterrows():
        for region_column in ('Intermediate Region Name', 'Sub-region Name', 'Region Name'):
            name = fix_string_value(country_item[region_column])
            if name is None or (name, 'Region') in area_name_and_type_to_vertex:
                # Don't create regions with no name, or regions that were already added.
                continue

            uuid = str(uuid4())

            props = {
                'name': name,
                'uuid': uuid,
            }
            vertex = graph.create_vertex(region_cls, **props)
            area_name_and_type_to_vertex[(name, 'Region')] = vertex

    # Create all relationships between countries/regions.
    created_edges = set()
    for _, country_item in countries_df.iterrows():
        hierarchy_order = (
            ('CLDR display name', 'Country'),
            ('Intermediate Region Name', 'Region'),
            ('Sub-region Name', 'Region'),
            ('Region Name', 'Region'),
        )
        regions_in_order = [
            (region_name, kind)
            for region_name, kind in (
                (fix_string_value(country_item[column_name]), kind)
                for column_name, kind in hierarchy_order
            )
            if region_name is not None
        ]

        for index, (parent_region_name, parent_region_kind) in enumerate(regions_in_order):
            if index == 0:
                continue

            child_region_name, child_region_kind = regions_in_order[index - 1]

            uniqueness_key = (
                parent_region_name,
                parent_region_kind,
                child_region_name,
                child_region_kind,
            )
            if uniqueness_key not in created_edges:
                graph.create_edge(
                    subarea_cls,
                    area_name_and_type_to_vertex[(parent_region_name, parent_region_kind)],
                    area_name_and_type_to_vertex[(child_region_name, child_region_kind)])
                created_edges.add(uniqueness_key)

    # Link all currently parent-less regions to the World region.
    all_region_names = set(area_name_and_type_to_vertex.keys())
    all_regions_with_parents = {
        (child_region_name, child_region_kind)
        for _, _, child_region_name, child_region_kind in created_edges
    }
    all_regions_without_parents = all_region_names - all_regions_with_parents

    world_vertex = graph.create_vertex(region_cls, name='World', uuid=str(uuid4()))
    for region_name, region_kind in all_regions_without_parents:
        graph.create_edge(
            subarea_cls,
            world_vertex,
            area_name_and_type_to_vertex[(region_name, region_kind)])


def orientdb_load_all():
    countries_df = get_countries_data()
    load_countries_and_regions(countries_df)


if __name__ == '__main__':
    orientdb_load_all()
