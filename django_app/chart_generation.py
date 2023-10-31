import django_pandas.io as pd
import plotly.express as px


def category_total_watched_chart(df):
    """Bar chart by total amount of watched videos by category"""

    # Group by category and count. Only category name and count columns
    df = df.groupby('video__category__name').size().to_frame('nr_of_watched_videos').reset_index()

    # Plotly bar chart
    fig = px.bar(
        df,
        x='video__category__name',
        y='nr_of_watched_videos',
        color='video__category__name',
        labels={
            'video__category__name': 'Category',
            'nr_of_watched_videos': 'Number of watched videos'
        },
        title='Total watched videos by category',
    )

    return fig
