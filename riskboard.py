
region_values = {
    'North America' : 5,
    'South America' : 2,
    'Europe'        : 5,
    'Africa'        : 3,
    'Asia'          : 7,
    'Australia'     : 2
}

region_memberships = {
    'North America' : ['Alaska',
                       'Alberta',
                       'Central America',
                       'Eastern United States',
                       'Greenland',
                       'Northwest Territory',
                       'Ontario',
                       'Quebec',
                       'Western United States'],
    'South America' : ['Argentina',
                       'Brazil',
                       'Peru',
                       'Venezuela'],
    'Europe'        : ['British Isles',
                       'Iceland',
                       'Northern Europe',
                       'Scandinavia',
                       'Southern Europe',
                       'Ukraine',
                       'Western Europe'],
    'Africa'        : ['Congo',
                       'East Africa',
                       'Egypt',
                       'Madagascar',
                       'North Africa',
                       'South Africa'],
    'Asia'          : ['Afghanistan',
                       'China',
                       'India',
                       'Irkutsk',
                       'Japan',
                       'Kamchatka',
                       'Middle East',
                       'Mongolia',
                       'Siam',
                       'Siberia',
                       'Ural',
                       'Yakutsk'],
    'Australia'     : ['Eastern Australia',
                       'Indonesia',
                       'New Guinea',
                       'Western Australia']
}

territory_adjacency = {
    'Alaska'                : ['Alberta', 'Northwest Territory', 'Kamchatka'],
    'Alberta'               : ['Alaska', 'Northwest Territory', 'Ontario', 'Western United States'],
    'Central America'       : ['Western United States', 'Eastern United States', 'Venezuela'],
    'Eastern United States' : ['Central America', 'Western United States', 'Ontario', 'Quebec'],
    'Greenland'             : ['Quebec', 'Ontario', 'Northwest Territory', 'Iceland'],
    'Northwest Territory'   : ['Alaska', 'Greenland', 'Ontario', 'Alberta'],
    'Ontario'               : ['Alberta', 'Northwest Territory', 'Greenland',
                               'Quebec', 'Eastern United States', 'Western United States'],
    'Quebec'                : ['Eastern United States', 'Ontario', 'Greenland'],
    'Western United States' : ['Alberta', 'Ontario', 'Eastern United States', 'Central America'],

    'Argentina' : ['Peru', 'Brazil'],
    'Brazil'    : ['Argentina', 'Peru', 'Venezuela', 'North Africa'],
    'Peru'      : ['Venezuela', 'Brazil', 'Argentina'],
    'Venezuela' : ['Central America', 'Brazil', 'Peru'],

    'British Isles'   : ['Iceland', 'Scandinavia', 'Northern Europe', 'Western Europe'],
    'Iceland'         : ['Greenland', 'British Isles', 'Scandinavia'],
    'Northern Europe' : ['British Isles', 'Scandinavia', 'Ukraine', 'Southern Europe', 'Western Europe'],
    'Scandinavia'     : ['Iceland', 'Ukraine', 'Northern Europe', 'British Isles'],
    'Southern Europe' : ['Western Europe', 'Northern Europe', 'Ukraine', 'Middle East', 'Egypt', 'North Africa'],
    'Ukraine'         : ['Northern Europe', 'Scandinavia', 'Ural', 'Afghanistan', 'Middle East', 'Southern Europe'],
    'Western Europe'  : ['British Isles', 'Northern Europe', 'Southern Europe', 'North Africa'],

    'Congo'        : ['North Africa', 'East Africa', 'South Africa'],
    'East Africa'  : ['Congo', 'North Africa', 'Egypt', 'Middle East', 'Madagascar', 'South Africa'],
    'Egypt'        : ['North Africa', 'Southern Europe', 'Middle East', 'East Africa'],
    'Madagascar'   : ['South Africa', 'East Africa'],
    'North Africa' : ['Brazil', 'Western Europe', 'Southern Europe', 'Egypt', 'East Africa', 'Congo'],
    'South Africa' : ['Congo', 'East Africa', 'Madagascar'],

    'Afghanistan' : ['Middle East', 'Ukraine', 'Ural', 'China', 'India'],
    'China'       : ['Afghanistan', 'Ural', 'Siberia', 'Mongolia', 'Siam', 'India'],
    'India'       : ['Middle East', 'Afghanistan', 'China', 'Siam'],
    'Irkutsk'     : ['Siberia', 'Yakutsk', 'Kamchatka', 'Mongolia'],
    'Japan'       : ['Mongolia', 'Kamchatka'],
    'Kamchatka'   : ['Japan', 'Mongolia', 'Irkutsk', 'Yakutsk', 'Alaska'],
    'Middle East' : ['East Africa', 'Egypt', 'Southern Europe', 'Ukraine', 'Afghanistan', 'India'],
    'Mongolia'    : ['China', 'Siberia', 'Irkutsk', 'Kamchatka', 'Japan'],
    'Siam'        : ['India', 'China', 'Indonesia'],
    'Siberia'     : ['Ural', 'Yakutsk', 'Irkutsk', 'Mongolia', 'China'],
    'Ural'        : ['Ukraine', 'Siberia', 'China', 'Afghanistan'],
    'Yakutsk'     : ['Siberia', 'Kamchatka', 'Irkutsk'],

    'Eastern Australia' : ['Western Australia', 'New Guinea'],
    'Indonesia'         : ['Siam', 'New Guinea', 'Western Australia'],
    'New Guinea'        : ['Eastern Australia', 'Western Australia', 'Indonesia'],
    'Western Australia' : ['Indonesia', 'New Guinea', 'Eastern Australia']
}
