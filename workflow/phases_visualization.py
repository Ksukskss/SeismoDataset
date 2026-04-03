'''Визуализация лучей с помощью модели iasp91 для землетрясения 2025-07-29'''

import obspy
from obspy.clients.fdsn import Client
from obspy.taup import TauPyModel
import matplotlib.pyplot as plt


client = Client("EarthScope")
catalog = client.get_events(starttime = '2025-05-01', minmagnitude = 8.5)
print('Поиск станций')
t = catalog[0].origins[0].time
# Загрузится почти мгновенно
inv = client.get_stations(network='G', station='*', starttime= t, level='station')

print("найдено станций: ", len(inv[0]))

depth = catalog[0].origins[0].depth / 1000

phases =["P", "S", "PP", "PKIKP", "SKS"]
dist = []
for i in range(len(inv[0])):
    distance = (obspy.geodetics.locations2degrees(inv[0][i].latitude, inv[0][i].longitude, catalog[0].origins[0].latitude, catalog[0].origins[0].longitude))
    azimuth = (obspy.geodetics.gps2dist_azimuth(inv[0][i].latitude, inv[0][i].longitude, catalog[0].origins[0].latitude, catalog[0].origins[0].longitude)[1])
    if azimuth > 180:
        distance = -distance
        
    dist.append(distance)


model = TauPyModel(model="iasp91")
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
for i in dist:
    arrivals = model.get_ray_paths(
        source_depth_in_km=depth, 
        distance_in_degree=i,
        phase_list=phases,
        )
    arrivals.plot_rays(plot_type="spherical", ax=ax, legend=False, show= False)
plt.show()



