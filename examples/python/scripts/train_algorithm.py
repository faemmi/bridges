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

"""Run the production bridge via mantik."""

import pathlib

import mantik.engine
import mantik.types

__file_loc__ = pathlib.Path(__file__)

print("Using mantik...\n")

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
train_bundle = mantik.types.Bundle(data_type, [])

meta = dict()

my_ref = "power-production-forecast"

with mantik.engine.Client("localhost", 8087) as client:
    simple_learn = client._add_algorithm(__file_loc__ / "bridges/sklearn/production", named_mantik_id = "mantik/sklearn.production")
    gradientboosting = client._add_algorithm(__file_loc__ / "bridges/sklearn/production/algorithms/gradientboosting")
    with client.enter_session():
        trained_pipe, stats = client.train([gradientboosting], train_bundle, meta=meta, action_name="Training")
        kmeans_trained = client.tag(trained_pipe, my_ref).save()
        train_result = client.apply(trained_pipe, train_bundle).fetch(action_name="Predict power production")
        result = train_result.bundle
print(f"Result: {result.value}")
