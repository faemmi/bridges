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

with mantik.engine.Client("localhost", 8087) as client:
    dataset = client.add_artifact(
        __file_loc__.as_posix(),
        named_mantik_id="mantik/dataset.kmeans",
    )
    simple_dataset = client.add_artifact((__file_loc__ / "datasets/simple").as_posix())
    with client.enter_session():
        result = client.get(simple_dataset, action_name="Get simple kmeans dataset")
        print(result.bundle.value)
