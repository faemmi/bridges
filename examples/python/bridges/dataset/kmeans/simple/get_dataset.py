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
import time

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.metrics import accuracy_score

import mantik.engine
import mantik.types

__file_loc__ = pathlib.Path(__file__).parent

print("Using mantik...\n")
start_time = time.time()

n_clusters = 3
meta = dict(n_clusters=n_clusters)

my_ref = "mq/kmeans_trained_on_blobs"

print((__file_loc__ / "../../../").resolve())

with mantik.engine.Client("localhost", 8087) as client:
    dataset = client._add_algorithm(
        (__file_loc__ / "../../../dataset/kmeans/simple").as_posix(),
        named_mantik_id="mantik/dataset.kmeans",
    )
    simple_dataset = client._add_algorithm(
        (__file_loc__ / "../../../dataset/kmeans/simple/datasets/simple").as_posix()
    )
    transform = client._add_algorithm(
        (__file_loc__ / "../../../algorithm/pandas/simple").as_posix()
    )
    simple_transform = client._add_algorithm(
        (__file_loc__ / "../../../algorithm/pandas/simple/algorithms/transform").as_posix()
    )
    simple_learn = client._add_algorithm(
        __file_loc__.as_posix(),
        named_mantik_id="mantik/sklearn.simple",
    )
    kmeans = client._add_algorithm(
        (__file_loc__ / "algorithms/kmeans").as_posix()
    )
    with client.enter_session():
        breakpoint()
        result = client.apply(simple_transform, simple_dataset)
        breakpoint()
        trained_pipe, stats = client.train([kmeans], train_bundle, meta=meta, action_name="Training")
        kmeans_trained = client.tag(trained_pipe, my_ref).save()
        train_result = client.apply(trained_pipe, train_bundle).fetch(action_name="Fetching Train Results")
        test_result = client.apply(trained_pipe, test_bundle).fetch(action_name="Fetching Train Results")

end_time = time.time()

# TODO (mq): bundle to pandas.DataFrame
centers_trained = np.sort(np.array(stats.bundle.value[0][0]).reshape(n_clusters, -1), axis=0)
train_prediction = pairwise_distances_argmin(train_data, centers_trained)
test_prediction = pairwise_distances_argmin(test_data, centers_trained)

print("Labeled centers: ", centers)
print("Trained centers: ", centers_trained)
print("Inertia: ", stats.bundle.value[0][1])
print("Iterations: ", stats.bundle.value[0][2])
print("Accuracy score on training data: ", accuracy_score(train_label, train_prediction))
print("Accuracy score on test data: ", accuracy_score(test_label, test_prediction))
print("Running kmeans via mantik took", end_time - start_time)

print("\n\n\n")
print("Using sklearn directly...\n")
start_time = time.time()
# ===============================================================
from sklearn.cluster import KMeans

model = KMeans(n_clusters=n_clusters).fit(train_data)
centers_trained = np.sort(model.cluster_centers_, axis=0)
# ===============================================================
end_time = time.time()

train_prediction = pairwise_distances_argmin(train_data, centers_trained)
test_prediction = pairwise_distances_argmin(test_data, centers_trained)

print("Labeled centers: ", centers)
print("Trained centers: ", centers_trained)
print("Inertia: ", model.inertia_)
print("Iterations: ", model.n_iter_)
print("Accuracy score on training data: ", accuracy_score(train_label, train_prediction))
print("Accuracy score on test data: ", accuracy_score(test_label, test_prediction))
print("Running kmeans directly took", end_time - start_time)
# ===============================================================
