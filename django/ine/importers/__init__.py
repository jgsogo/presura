# -*- coding: utf-8 -*-

import logging
from .mapas_municipales import MapasMunicipales


log = logging.getLogger(__name__)


def get_importer(resource, downloadlog):
    all = [MapasMunicipales,]
    for it in all:
        if it.id == resource.importer:
            return it(downloadlog)
    raise ValueError("No importer found for resource '{}' (importer '{}')".format(resource, resource.importer))
