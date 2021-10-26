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
import mantik
import utils
from sklearn.ensemble import GradientBoostingRegressor


def train(bundle: mantik.types.Bundle, meta: mantik.types.MetaVariables) -> mantik.types.Bundle:
    _, production, time_of_day, time_of_year = utils.unpack_bundle(bundle)

    x = utils.prepare_x_values(time_of_day, time_of_year)

    model = GradientBoostingRegressor(**meta).fit(x, production)
    utils.save_model(model)

    score = model.score(x, production)

    result = utils.convert_to_columns([score])
    return mantik.types.Bundle(value=result)


def try_init():
    utils.load_model()


def apply(model, bundle: mantik.types.Bundle) -> mantik.types.Bundle:
    dates, _, time_of_day, time_of_year = utils.unpack_bundle(bundle)

    x = utils.prepare_x_values(time_of_day, time_of_year)
    prediction = model.predict(x)

    # Data fetching in Python does not yet support streaming, hence not all
    # data can be retrieved.
    result = utils.convert_to_columns(dates[:10], prediction[:10])
    return mantik.types.Bundle(value=result)
