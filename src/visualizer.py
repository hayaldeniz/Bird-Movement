import folium
from folium.plugins import PolyLineTextPath
import matplotlib.pyplot as plt

class BirdTrackerVisualizer:
    def __init__(self, df, default_zoom=4, colormap=plt.cm.Set1):
        self.df = df.copy()
        self.default_zoom = default_zoom
        self.colormap = colormap
        self.unique_birds = self.df["bird_name"].unique()

    def start_end_markers(self, bird_name):
        df = self.df.copy()
        if bird_name != "all":
            df = df[df["bird_name"] == bird_name].sort_values("date_time")
            start_lat, start_lon = df.iloc[0][["latitude", "longitude"]]
            end_lat, end_lon = df.iloc[-1][["latitude", "longitude"]]

            m = folium.Map(location=[start_lat, start_lon], zoom_start=self.default_zoom)

            folium.Marker([start_lat, start_lon], tooltip=f"{bird_name} started here").add_to(m)
            folium.Marker([end_lat, end_lon], tooltip=f"{bird_name} ended here").add_to(m)

            return m
        else:
            print("Start-end visualization only implemented for single bird")
            return None

    def trajectory(self, bird_name):
        df = self.df.copy()
        if bird_name != "all":
            df = df[df["bird_name"] == bird_name].sort_values("date_time")
            coords = df[["latitude", "longitude"]].values.tolist()
            m = folium.Map(location=[coords[0][0], coords[0][1]], zoom_start=self.default_zoom)

            line = folium.PolyLine(coords).add_to(m)
            PolyLineTextPath(line, " ➤ ", repeat=True, offset=7,
                             attributes={'fill': 'blue', 'font-weight': 'bold', 'font-size': '12'}).add_to(m)
            return m
        else:
            m = folium.Map(location=[self.df['latitude'].mean(), self.df['longitude'].mean()],
                           zoom_start=self.default_zoom)
            colors = self.colormap(range(len(self.unique_birds)))
            for bird, color in zip(self.unique_birds, colors):
                r, g, b, _ = color
                rgb = f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"
                coords = self.df.loc[self.df["bird_name"]==bird, ["latitude","longitude"]].values.tolist()
                folium.PolyLine(coords, color=rgb, tooltip=bird).add_to(m)
            return m
