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
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
from sklearn.metrics.pairwise import pairwise_distances_argmin

import mantik.engine
import mantik.types


def get(meta: mantik.types.MetaVariables) -> mantik.types.Bundle:
    result = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return mantik.types.Bundle(value=result)

    centers = np.sort(np.array([[1, 1], [0, 0], [-1, -1]]), axis=0)
    data, _ = make_blobs(n_samples=100, n_features=2, centers=centers, cluster_std=0.95)
    label = pairwise_distances_argmin(data, centers)

    train_data, test_data, train_label, test_label = train_test_split(data, label)

    ds = """
    {
        "columns":
        {
            "coordinates":
            {
                "type": "tensor",
                "shape": [2],
                "componentType": "float64"
            }
        }
    }
    """
    data_type = mantik.types.DataType.from_json(ds)
    # TODO (mq): This reshaping is unintuitive
    train_bundle = mantik.types.Bundle(data_type, train_data.reshape(-1, 1, 2).tolist())
    test_bundle = mantik.types.Bundle(data_type, test_data.reshape(-1, 1, 2).tolist())

    data_type = meta.get("data_type")
    if data_type == "training":
        return train_bundle
    elif data_type == "prediction":
        return test_bundle
