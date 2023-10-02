import geopandas as gpd

midwest = gpd.read_file(r'/Volumes/GUILHERME/_microsoft_roads/_regions/USA_South.gpkg')

roads = gpd.read_file(r'/Users/guilhermeiablonovski/Desktop/USA.gpkg', mask=midwest)

roads.to_file(r'/Users/guilhermeiablonovski/Desktop/USA_South.gpkg')