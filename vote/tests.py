from django.contrib.auth.models import User
from django.test import TestCase
from vote.models import News, Material, Comment, Vote
from vote.service import VoteService

#TODO Дописать фейк id


class VoteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test@test.com")
        news = News.objects.create(type=Material.NEWS,
                                   title="ШОК!",
                                   text="В индийской многоэтажке из кранов вместо воды полился алкоголь!!",
                                   author=self.user)
        Comment.objects.create(text="Наканецта", material=news, author=self.user)

    def test_creating(self):
        """
        Тестирование создания оценки для двух разных сущностей
        :return:
        """
        VoteService.create_or_update(Comment, 1, Vote.LIKE, self.user)
        VoteService.create_or_update(News, 1, Vote.LIKE, self.user)
        self.assertEqual(Comment.objects.get(pk=1).votes.all().count(), 1)
        self.assertEqual(News.objects.get(pk=1).votes.all().count(), 1)

    def test_updating(self):
        """
        Тестирование обновления оценки
        :return:
        """

        # Создание оценки
        VoteService.create_or_update(Comment, 1, Vote.LIKE, self.user)
        self.assertEqual(Comment.objects.get(pk=1).votes.all().count(), 1)

        # Тест обновления оценки
        VoteService.create_or_update(Comment, 1, Vote.DISLIKE, self.user)
        self.assertEqual(Comment.objects.get(pk=1).votes.first().status, Vote.DISLIKE)

    def test_deleting(self):
        """
        Тестирование удаления оценки
        :return:
        """

        # Создание оценки
        VoteService.create_or_update(Comment, 1, Vote.LIKE, self.user)
        self.assertEqual(Comment.objects.get(pk=1).votes.all().count(), 1)

        # Тест удаления оценки
        VoteService.delete(Comment, 1, self.user)
        self.assertEqual(Comment.objects.get(pk=1).votes.all().count(), 0)

    def test_getting_count(self):
        """
        Тестирование получения количества оценок
        :return:
        """
        for username in ["test1@test.com", "test2@test.com", "test3@test.com"]:
            user = User.objects.create(username=username)
            VoteService.create_or_update(News, 1, Vote.LIKE, user)

        for username in ["test4@test.com", "test5@test.com", "test6@test.com"]:
            user = User.objects.create(username=username)
            VoteService.create_or_update(News, 1, Vote.DISLIKE, user)

        self.assertEqual(VoteService.get_all_count(News, 1), 6)
        self.assertEqual(VoteService.get_count_by_status(News, 1, Vote.DISLIKE), 3)
        self.assertEqual(VoteService.get_count_by_status(News, 1, Vote.LIKE), 3)

    def test_passing_wrong_instance(self):
        """
        Тест возвращаемых значений при неверных параметрах pk
        :return:
        """

        self.assertEqual(VoteService.create_or_update(Comment, 222, Vote.LIKE, self.user), False)
        self.assertEqual(VoteService.delete(Comment, 222, self.user), None)
        self.assertEqual(VoteService.get_count_by_status(Comment, 222, Vote.DISLIKE), None)
        self.assertEqual(VoteService.get_all_count(Comment, 222), None)
