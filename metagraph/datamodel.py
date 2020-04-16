# -*- coding: utf-8 -*-

from mongoengine import *
from asq.initiators import *
from metagraph.data_helper import DataHelper

"""
Метаграфовая модель данных, реализованная в mongodb с использованием mongoengine
"""

class VertexGeneric(Document):
    meta = {'allow_inheritance': True}
    name = StringField()

class Edge(VertexGeneric):
    s = ReferenceField(VertexGeneric)
    d = ReferenceField(VertexGeneric)

    def __str__(self):
        return 'Связь: ' + self.name + ' (' + self.s.name + ' -> ' + self.d.name + ')'


class Vertex(VertexGeneric):
    _Vertices = ListField(ReferenceField(VertexGeneric))
    _Edges = ListField(ReferenceField(Edge))
    _Parents = ListField(ReferenceField(VertexGeneric))

    def __str__(self):
        return 'Вершина: ' + self.name

    def add_vertices(self, *verts):
        for v in verts:
            self._Vertices.append(v)
            v.add_parent(self)
        self.save()

    def first_subvertex_by_name(self, name_param):
        for v in self._Vertices:
            if v.name == name_param:
                return v
        return None

    def add_edges(self, *edges):
        for e in edges:
            self._Edges.append(e)
        self.save()

    def add_parent(self, vertex):
        self._Parents.append(vertex)
        self.save()

    def print_recursive(self, level: int):
        """
        Рекурсивная печать информации о вершине, вложеннных вершинах, атрибутах, связях
        """
        DataHelper.PrintWithLevel(str(self), level)

        if len(self._Vertices) > 0:
            DataHelper.PrintWithLevel("Вложенные вершины: ", level + 1)
            for v in self._Vertices:
                v.print_recursive(level + 2)

        if len(self._Edges) > 0:
            DataHelper.PrintWithLevel("Вложенные связи: ", level + 1)
            for edge in self._Edges:
                DataHelper.PrintWithLevel(str(edge), level + 2)