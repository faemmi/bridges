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

"""Run sklearn.cluster.KMeans via mantik."""

import pathlib

import mantik

__file_loc__ = pathlib.Path(__file__).parent

with mantik.engine.EngineClient("localhost", 8087) as client:
    dataset = client.add_artifact(
        (__file_loc__/ "../../../dataset/kmeans/simple").as_posix(),
        named_mantik_id="mantik/dataset.kmeans",
    )
    simple_dataset = client.add_artifact(
        (__file_loc__ / "../../../dataset/kmeans/simple/datasets/simple").as_posix(),
    )
    pandas = client.add_artifact(
        __file_loc__.as_posix(),
        named_mantik_id="mantik/pandas.simple",
    )
    transform = client.add_artifact(
        (__file_loc__ / "algorithms/transform").as_posix(),
        named_mantik_id="mantik/pandas.simple.transform"
    )
    transform2 = client.add_artifact(
        (__file_loc__ / "algorithms/transform2").as_posix(),
        named_mantik_id="mantik/pandas.simple.transform"
    )
    with client.enter_session():
        result = client.apply([transform, transform2], data=simple_dataset)
        print(result.bundle.value)

