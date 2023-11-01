import django_pandas.io as pd
import plotly.express as px
import plotly.graph_objects as go


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


def day_hours_trend_chart(df):
    """What hourse of the day are most videos watched"""

    # Copy df because we will change it
    df = df.copy()

    # Take only hours from time
    df['time'] = df['time'].dt.strftime('%H')

    # Group by hour and count. Only hour and count columns
    df = df.groupby('time').size().to_frame('nr_of_watched_videos').reset_index()

    # Plotly bar chart
    fig = px.bar(
        df,
        x='time',
        y='nr_of_watched_videos',
        labels={
            'time': 'Hour',
            'nr_of_watched_videos': 'Number of watched videos'
        },
        title='What hourse of the day are most videos watched',
    )

    return fig


def watched_again_top_chart(df):
    """What videos have you watched the most over and over again?"""

    # Copy df because we will change it
    df = df.copy()

    # Group by video and count. Only video name and count columns
    df = df.groupby('video__name').size().to_frame('nr_of_watched_videos').reset_index()

    # Order by count
    df = df.sort_values('nr_of_watched_videos', ascending=False)

    # Take only top 10
    df = df.head(10)

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=['Video name', 'Number of watched videos'],
                ),
                cells=dict(
                    values=[df['video__name'], df['nr_of_watched_videos']],
                )
            )
        ]
    )

    return fig
