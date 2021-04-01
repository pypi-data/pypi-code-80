import prediction_module as pm
import pandas as pd
import plotly.express as px

# Loads data
pm.Load_db_vis()
df = pm.Load_db_vis.save_as_df2('Beracasa')
df['name'] = ['Beracasa']*len(df)

# Concat dataframes
for i in range(1, len(pm.Load_db_vis.name)):
    df_temp = pm.Load_db_vis.save_as_df2(pm.Load_db_vis.name[i])
    df_temp['name'] = [pm.Load_db_vis.name[i]]*len(df_temp)
    df = pd.concat((df, df_temp))

df = df.sort_values(['dateObserved'])

fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="intensity",
                        color='intensity', range_color=[0, 1500],
                        color_continuous_scale=px.colors.diverging.Temps,
                        size_max=20, zoom=12, animation_frame="dateObserved",
                        hover_name="name")
fig.update_layout(mapbox_style="carto-positron",
                  title="""Montpellier's bike passing each day""")

# Show anim in a server
fig.show()

fig.write_html("./Prediction_velo/index.html")
