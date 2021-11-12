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
import pathlib

import mantik

__file_loc__ = pathlib.Path(__file__).parent

with mantik.engine.Client("localhost", 8087) as client:
    climetlab_bridge = client.add_artifact(__file_loc__.as_posix())
    power_production_dataset = client.add_artifact(
        (__file_loc__ / "datasets/power-production").as_posix()
    )
    with client.enter_session():
        result = client.get(power_production_dataset)
        print(result.bundle.value)
