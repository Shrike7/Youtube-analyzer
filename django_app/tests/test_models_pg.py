from ..models.postgres import (WatchRecord, Video,
                               Category, Channel, UserProfile)
from django.test import TestCase
from django.contrib.auth.models import User


class TestPostgresModelsRelations(TestCase):
    """Test models relations."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='test_user',
                                             password='12345')
        self.user_profile = UserProfile.objects.create(user_id=self.user)
        self.category = Category.objects.create(name='test_category')
        self.channel = Channel.objects.create(custom_id='test_channel',
                                            name='test_channel')
        self.video = Video.objects.create(custom_id='test_video',
                                          name='test_video',
                                          channel=self.channel,
                                          category=self.category)
        self.watch_record = WatchRecord.objects.create(
            time='2033-01-01 00:00:00+00:00',
            user_profile=self.user_profile,
            video=self.video
        )

    def test_user_profile_userid_is_user(self):
        """Test UserProfile user_id is related to User."""
        self.assertEqual(self.user_profile.user_id, self.user)

    def test_watch_record_foreign_keys_relations(self):
        """Test WatchRecord user_profile relate to UserProfile and video relate to Video."""
        self.assertEqual(self.watch_record.user_profile, self.user_profile)
        self.assertEqual(self.watch_record.video, self.video)

    def test_video_foreign_keys_relations(self):
        """Test Video channel relate to Channel and category relate to Category."""
        self.assertEqual(self.video.channel, self.channel)
        self.assertEqual(self.video.category, self.category)

    def test_watch_record_uniqueness(self):
        """Test WatchRecord uniqueness."""
        time = self.watch_record.time
        user_profile = self.watch_record.user_profile
        video = self.watch_record.video

        with self.assertRaises(Exception):
            WatchRecord.objects.create(
                time=time,
                user_profile=user_profile,
                video=video
            )

    def test_watch_record_same_but_different_time(self):
        """WatchRecord must be created if same record exists but with different time."""
        time = '2034-01-01 00:00:00+00:00'
        user_profile = self.watch_record.user_profile
        video = self.watch_record.video

        try:
            WatchRecord.objects.create(
                time=time,
                user_profile=user_profile,
                video=video
            )
        except Exception:
            self.fail('WatchRecord with same user_profile and video but different time should be created.')

    def test_watch_record_join_with_video_channel_category(self):
        """Test WatchRecord join with Video, Channel and Category.
        Check if joined data is correct."""
        watch_records = WatchRecord.objects.filter(user_profile=self.user_profile)

        watch_records = watch_records.select_related('video')
        watch_records = watch_records.select_related('video__channel')
        watch_records = watch_records.select_related('video__category')

        # Check if joined data is correct
        self.assertEqual(watch_records[0].video, self.video)
        self.assertEqual(watch_records[0].video.channel, self.channel)
        self.assertEqual(watch_records[0].video.category, self.category)

