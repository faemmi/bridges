#
# This file is part of the Mantik Project.
# Copyright (c) 2020-2021 Mantik UG (Haftungsbeschränkt)
# Authors: See AUTHORS file
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.
#
# Additionally, the following linking exception is granted:
#
# If you modify this Program, or any covered work, by linking or
# combining it with other code, such other code is not for that reason
# alone subject to any of the requirements of the GNU Affero GPL
# version 3.
#
# You can be released from the requirements of the license by purchasing
# a commercial license.
#
import os
import logging

import mantik

from algorithm_wrapper import AlgorithmWrapper
from dataset_wrapper import DataSetWrapper

logger = logging.getLogger(__name__)

PORT = os.getenv("MANTIK_MNP_PORT", default=8502)


def provide_wrapper(mantikheader: mantik.types.MantikHeader):
    logger.debug("Received mantikheader %s", mantikheader)
    if mantikheader.kind == "dataset":
        bridge_provider = DataSetWrapper(mantikheader)
    elif mantikheader.kind == "algorithm":
        bridge_provider = AlgorithmWrapper(mantikheader)
    else:
        raise RuntimeError("Bridge does not support bridge kind %s", mantikheader.kind)
    logger.debug("Returning bridge provider %s", bridge_provider)
    return bridge_provider


mantik.bridge.start_mnp_bridge(provide_wrapper, "sklearn bridge", port=PORT)
