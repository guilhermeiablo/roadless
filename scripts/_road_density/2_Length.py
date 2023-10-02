import geopandas as gpd
import numpy as np
import shapely

allcontinents = ['Georgia_OSM','NewCaledonia_OSM','NorthKorea_OSM','SouthKorea_OSM', 'JapanOSM','China_OSM','USA_West','USA_Midwest','USA_South','USA_Northeast','Europe_Western','Europe_Northern','Europe_Eastern','Europe_Central','Europe_UK','AfricaCenter','AfricaEast','AfricaNorth','AfricaSouth','AfricaWest','AmericaCenter','AsiaCenter','AsiaNorth','AsiaSouth','AsiaSouthEast','Canada','CaribbeanIslands','Europe','MiddleEast','Oceania','SouthAmerica','USA']
cell_size = ['10','50']
continents = ['Japan_OSM']


for continent in continents:
	raw_roads = gpd.read_file(r'/Volumes/GUILHERME/_microsoft_roads/'+continent+'.gpkg')
	print('Read data for '+continent)
	for size in cell_size:
		grid = gpd.read_file(r'/Volumes/GUILHERME/_microsoft_roads/'+size+'km_grid_raw.gpkg')
		print('Read grid data for '+size+'km')
		grid = grid[['geometry']]
		cell = grid

		raw_roads = raw_roads.to_crs(cell.crs)
		cell['grid_id'] = cell.index

		overlayed = raw_roads.to_crs(cell.crs).overlay(cell, how='intersection')
		overlayed['length'] = overlayed.geometry.length
		print('Finished overlay')

		dissolve = overlayed[['length','grid_id','geometry']].dissolve(by="grid_id", aggfunc="sum")
		print('Finished dissolve')
		cell_length = cell.merge(dissolve[['length']], on='grid_id')
		print('Finished merge')
		cell_length = cell_length.dropna()
		cell_length['area'] = cell_length.geometry.area
		cell_length['road_density'] = (cell_length['length']/cell_length['area'])*1000000

		cell_length.to_file(continent+'_'+size+'km_RoadDensity.gpkg')
		print('Wrote results to '+continent+'_'+size+'km_RoadDensity.gpkg')

