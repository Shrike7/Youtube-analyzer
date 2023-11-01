import django_pandas.io as pd
import plotly.express as px


def category_trend_chart(df):
    """Watched videos by categories for all period"""

    # Copy df because we will change it
    df = df.copy()

    # Floor time to day
    df['time'] = df['time'].dt.floor('d')

    # Group by category and time and count. Only category name, time and count columns
    df = df.groupby(['video__category__name', 'time']).size().to_frame('nr_of_watched_videos').reset_index()

    fig = px.line(
        df,
        x='time',
        y='nr_of_watched_videos',
        color='video__category__name',
        labels={
            'video__category__name': 'Category',
            'nr_of_watched_videos': 'Number of watched videos',
            'time': 'Days'
        },
        title='Watched videos by categories for all period',
    )

    return fig


def category_total_watched_chart(df):
    """Bar chart by total amount of watched videos by category"""

    # Copy df because we will change it
    df = df.copy()

    # Group by category and count. Only category name and count columns
    df = df.groupby('video__category__name').size().to_frame('nr_of_watched_videos').reset_index()

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
