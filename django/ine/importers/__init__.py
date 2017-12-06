# -*- coding: utf-8 -*-

import logging
from .mapas_municipales import MapasMunicipales
from .padron_municipal import PadronMunicipal


log = logging.getLogger(__name__)


class ImportersFactory:
    all = [MapasMunicipales, PadronMunicipal, ]

    def ids(self):
        return [it.id for it in self.all]

    def get_importer(self, resource, downloadlog):
        for it in self.all:
            if it.id == resource.importer:
                return it(downloadlog)
        raise ValueError("No importer found for resource '{}' (importer '{}')".format(resource, resource.importer))

importers_factory = ImportersFactory()


def get_importer(resource, downloadlog):
    return importers_factory.get_importer(resource, downloadlog)
