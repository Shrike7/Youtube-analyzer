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
    """What videos have you watched the most over and over again?
    Top 10"""

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


def videos_by_channels_chart(df):
    """Watched videos by YouTube channels
    Top 10"""

    # Copy df because we will change it
    df = df.copy()

    # Group by channel and count. Only channel name and count columns
    df = df.groupby('video__chanel__name').size().to_frame('nr_of_watched_videos').reset_index()

    # Order by count
    df = df.sort_values('nr_of_watched_videos', ascending=False)

    # Take only top 10
    df = df.head(10)

    # Rotated bar chart
    fig = px.bar(
        df,
        y='video__chanel__name',
        x='nr_of_watched_videos',
        labels={
            'video__chanel__name': 'Channel',
            'nr_of_watched_videos': 'Number of watched videos'
        },
        orientation='h',
        title='Watched videos by YouTube channels',
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed")
    )

    return fig


def day_of_week_trend_chart(df):
    """Weak-wise comparison of total number of watched videos"""

    # Copy df because we will change it
    df = df.copy()

    # Group by day of week and count. Only day of week and count columns
    df['time'] = df['time'].dt.weekday
    df = df.groupby(df['time']).size().to_frame('nr_of_watched_videos').reset_index()

    # Create a mapping dictionary for weekday names
    weekday_mapping = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }

    # Replace weekday number with weekday name
    df['time'] = df['time'].map(weekday_mapping)

    # Plotly bar chart
    fig = px.bar(
        df,
        x='time',
        y='nr_of_watched_videos',
        labels={
            'time': 'Day of week',
            'nr_of_watched_videos': 'Number of watched videos'
        },
        title='Weak-wise comparison of total number of watched videos',
    )

    return fig


def is_weekend_category_trend_chart(df):
    """Category trend for weekend and weekdays"""

    # Copy df because we will change it
    df = df.copy()

    # Convert time to day of week
    df['time'] = df['time'].dt.weekday

    # Add column to check if day is weekend
    df['is_weekend'] = df['time'].isin([5, 6])

    # Group by category, is_weekend and count. Only category name, is_weekend and count columns
    df = df.groupby(['video__category__name', 'is_weekend']).size().to_frame('nr_of_watched_videos').reset_index()

    # Change is_weekend False to Weekday and True to Weekend
    df['is_weekend'] = df['is_weekend'].map({False: 'Weekday', True: 'Weekend'})

    # Plotly bar chart
    fig = px.bar(
        df,
        x='is_weekend',
        y='nr_of_watched_videos',
        color='video__category__name',
        labels={
            'video__category__name': 'Category',
            'nr_of_watched_videos': 'Number of watched videos',
            'is_weekend': 'Is weekend'
        },
        barmode='group',
        text='video__category__name',

        title='Category trend for weekend and weekdays',
    )

    return fig
