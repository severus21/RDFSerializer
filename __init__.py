import itertools

from django.urls import reverse
from django.db.models import Model

from rdflib.namespace import Namespace, RDF
from rdflib import URIRef, Literal, BNode, Graph

SCHEMA = Namespace('http://schema.org/')


class RDFSimpleField:
    def __init__(self, relation, attr_str):
        self.attr_str = attr_str
        self.relation = relation

    def serialize(self, model_node, model):
        attr = getattr(model, self.attr_str)

        if attr:
            yield (model_node, self.relation, Literal(attr))
        else:
            return []
            raise Exception("{} not valid on model {}".format(self.attr_str,
                                                              model.id))


class RDFManyField(RDFSimpleField):
    def __init__(self, relation, attr_str, converter):
        self.attr_str = attr_str
        self.relation = relation
        self.converter = converter

    def serialize(self, model_node, model):
        objects = getattr(model, self.attr_str).all()

        for _obj in objects:
            yield (model_node, self.relation, Literal(self.converter(_obj)))


class RDFBinder(RDFSimpleField):
    def __init__(self, relation, attr_str, attr_serializer):
        self.attr_str = attr_str
        self.relation = relation
        self.attr_serializer = attr_serializer

    def bind(self, model_node, related_node):
        raise NotImplementedError("Should have implemented this")

    def serialize(self, model_node, model):
        tmp = getattr(model, self.attr_str)
        if not tmp:
            return

        related_serializer = self.attr_serializer()

        if not isinstance(tmp, Model):
            related_models = tmp.all()
        else:
            related_models = [tmp]

        for related_model in related_models:
            for tmp in related_serializer._triples(related_model):
                yield tmp

            yield self.bind(model_node, related_serializer.node(related_model))


class RDFLeftBinder(RDFBinder):
    def __init__(self, relation, attr_str, attr_serializer):
        RDFBinder.__init__(self, relation, attr_str, attr_serializer)

    def bind(self, model_node, related_node):
        return (model_node, self.relation, related_node)


class RDFRightBinder(RDFBinder):
    def __init__(self, relation, attr_str, attr_serializer):
        RDFBinder.__init__(self, relation, attr_str, attr_serializer)

    def bind(self, model_node, related_node):
        return (related_node, self.relation, model_node)


class RDFManyLinker(RDFBinder):
    """ Link together many to many children """
    def __init__(self, relation, attr_str, attr_serializer):
        self.attr_str = attr_str
        self.relation = relation
        self.attr_serializer = attr_serializer

    def serialize(self, _, model):
        tmps = getattr(model, self.attr_str)
        if not tmps:
            return

        related_serializer = self.attr_serializer()
        for _tmp1 in tmps.all():
            for _tmp2 in tmps.all():
                if _tmp1 != _tmp2:
                    n1 = related_serializer.node(_tmp1)
                    n2 = related_serializer.node(_tmp2)
                    yield (n1, self.relation, n2)
                    yield (n2, self.relation, n1)


class RDFSerialiser:
    pass


class RDFModelSerialiser(RDFSerialiser):
    _type = None
    model = None
    uri = None

    def __init__(self, graph=None):
        self.graph = graph if graph else Graph()

        self.work_done = False

    def node(self, model):
        if self.uri:
            return URIRef(reverse(self.uri, args=[model.id]))
        return BNode()

    def _triples(self, model):
        pub_node = self.node(model)

        yield (pub_node, RDF.type, self._type)
        for field in self.entries:
            for triple in field.serialize(pub_node, model):
                yield triple

    def triples(self):
        if self.work_done:
            return

        for model in self.model.objects.all():
            for triple in self._triples(model):
                self.graph.add(triple)

    def serialize(self, format='xml', models=None):
        if models is None:
            self.triples()
        else:
            for model in models:
                for triple in self._triples(model):
                    self.graph.add(triple)

        return self.graph.serialize(format=format).decode()


class RDFModelExpander(RDFModelSerialiser):
    def __init__(self, graph=None):
        super().__init__(graph)

    def _triples(self, models):
        return
        yield

    def triples(self):
        return

    def serialize(self):
        return ""
