from ..models.mongo import File, Video, Subtitle
from django.test import TestCase


class TestMongoModelsRelations(TestCase):
    """Test relations between mongo models."""

    def setUp(self):
        """Set up test data."""
        self.file = File(user_id=1, user_profile_id=1)
        self.subtitle = Subtitle(name='test_subtitle', url='test_url')
        self.video = Video(
            status=False, host=self.file, header='test_header',
            title='test_title', titleUrl='test_titleUrl',
            subtitles=[self.subtitle], time='2033-01-01 00:00:00+00:00',
            products=['test_product'], activityControls=['test_activityControls']
        )

        self.file.save()
        self.video.save()

    def test_video_host_is_file(self):
        """Test if Video host relate to File."""
        self.assertEqual(self.video.host, self.file)

    def test_video_subtitles_is_subtitle(self):
        """Test if Video subtitles relate to Subtitle."""
        self.assertEqual(self.video.subtitles[0], self.subtitle)

    def test_filter_videos_by_host_and_status(self):
        """Test if Video objects found by host and status."""
        videos = Video.objects.filter(host=self.file, status=False)
        self.assertEqual(videos.first(), self.video)
