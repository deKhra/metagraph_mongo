# -*- coding: utf-8 -*-

import config
from metagraph.processor import *

class Loader:

    """
    Класс для загрузки ситуаций и проверки загрузки
    """

    example_vertex_name_1 = "Пример 1"
    example_vertex_name_2 = "Пример 2"

    @staticmethod
    def load():
        """
        Загрузка в модель тестовых данных
        """
        metagraphModelConfig = MetagraphModelConfig('test_db', 'test_collection')
        proc = MetagraphModelProcessor(metagraphModelConfig)
        proc.drop_db()
        Loader.load_examples(proc)

    @staticmethod
    def load_examples(proc: MetagraphModelProcessor):
        privet = proc.create_vertex('Приветствие')
        privet_call = proc.create_vertex('Добрый день, ИО')
        privet.add_vertices(privet_call)

        predl = proc.create_vertex('Предложение')
        predl_call_1 = proc.create_vertex('Вас приветствует компания CompanyName.')
        predl_call_2 = proc.create_vertex('Меня зовут Arthas Звоню оповестить Вас об изменениях в тарифных планах')
        predl_call_3 = proc.create_vertex('Сейчас для всех абонентов сотовой связи, '
                                          'которые оплачивают свыше 600 рублей, мы предоставляем домашний интернет '
                                          'бесплатно, при условии, что дом подключен к сети CompanyName')
        predl_call_4 = proc.create_vertex(' У меня указан адрес Вашего проживания «Улица, дом» Адрес верный?')
        predl.add_vertices(predl_call_1, predl_call_2, predl_call_3, predl_call_4)
        predl_edge_1 = proc.create_edge("1", predl_call_1, predl_call_2)
        predl_edge_2 = proc.create_edge("1", predl_call_2, predl_call_3)
        predl_edge_3 = proc.create_edge("1", predl_call_3, predl_call_4)
        predl.add_edges(predl_edge_1, predl_edge_2, predl_edge_3)

        predl_accept = proc.create_vertex('у нас есть для вас ахууенный тариф')
        predl_decl = proc.create_vertex('Назовите, пожалуйста, актуальный адрес – улицу и номер дома.')
        poka_call = proc.create_vertex('До свидания, ИО')

        poka = proc.create_vertex('Прощание')
        poka.add_vertices(poka_call)

        otvet_priv = proc.create_edge('Добрый день.', privet_call, predl_call_1)
        otvet_da = proc.create_edge('Дa', predl_call_4, predl_accept)
        otvet_net = proc.create_edge('Нет', predl_call_4, predl_decl)
        poka_edge_1 = proc.create_edge('Пока', predl_accept, poka_call)
        poka_edge = proc.create_edge('Пока', predl_decl, poka_call)

        situation_1 = proc.create_vertex('Тестовый скрипт')
        situation_1.add_vertices(privet, predl, predl_accept, predl_decl, poka)
        situation_1.add_edges(otvet_da, otvet_net, otvet_priv, poka_edge, poka_edge_1)
        situation_1.save()

    @staticmethod
    def check_load():
        """
        проверка загрузки данных
        """
        level = 0
        separator = "*" * 100
        metagraphModelConfig = MetagraphModelConfig('test_db', 'test_collection')
        proc = MetagraphModelProcessor(metagraphModelConfig)
        proc.first_vertex_by_name('Тестовый скрипт').print_recursive(level)


if __name__ == '__main__':
    Loader.load()
    Loader.check_load()