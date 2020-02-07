from typing import Union

from django.contrib.auth.models import User

from vote.models import Vote


class VoteService:
    """
    Класс для работы с оценками
    """

    @staticmethod
    def create_or_update(model, pk: int, status: str, user: User) -> bool:
        """
        Создание оценки либо смена статуса оценки(смена лайка на дизлайк)
        :param model: класс Модели (Comment или Material) из vote.models
        :param pk: pk объекта модели для которой хотим поставить оценку
        :param status: тип оценки Vote.LIKE или Vote.DISLIKE
        :param user: Пользователь который ставит оценку
        :return: True если прошло успешно
        """

        if not model.objects.filter(pk=pk).exists():
            return False  # или можно поднимать ошибку наверх

        obj = model.objects.filter(pk=pk).first()
        vote = obj.votes.filter(author=user).first()
        if not vote:
            vote = Vote.objects.create(author=user, status=status)
            obj.votes.add(vote)
        else:
            vote.status = status
            vote.save()

        return True

    @staticmethod
    def delete(model, pk: int, user: User) -> None:
        """
        Удаление оценки
        :param model: класс Модели (Comment или Material) из vote.models
        :param pk: pk объекта модели для которой хотим удалить оценку
        :param user: пользователь который ставил оценку
        :return:
        """

        obj = model.objects.filter(pk=pk).first()
        if not obj:
            return None

        obj.votes.filter(author=user).delete()

    @staticmethod
    def get_count_by_status(model, pk: int, status: str) -> Union[int, None]:
        """
        Получить количество оценок для сущности по переданному status (количество лайков или дизлайков)
        :param model: класс Модели (Comment или Material) из vote.models
        :param pk: pk объекта модели для которой хотим получить оценки
        :param status: тип оценки Vote.LIKE или Vote.DISLIKE
        :return: Количество оценок или None если сущность не найдена
        """

        obj = model.objects.filter(pk=pk).first()
        if not obj:
            return None

        return obj.votes.filter(status=status).count()

    @staticmethod
    def get_all_count(model, pk: int) -> Union[int, None]:
        """
        Получить количество всех оценок для сущности
        :param model: класс Модели (Comment или Material) из vote.models
        :param pk: pk объекта модели для которой хотим получить оценки
        :return: Количество оценок или None если сущность не найдена
        """

        obj = model.objects.filter(pk=pk).first()
        if not obj:
            return None

        return obj.votes.all().count()
