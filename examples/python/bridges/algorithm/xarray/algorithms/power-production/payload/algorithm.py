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


def apply(bundle: mantik.types.Bundle, meta: mantik.types.MetaVariables) -> mantik.types.Bundle:
    dates, production = utils.unpack_bundle(bundle)

    datetimes = utils.convert_isoformat_dates_to_datetime(dates)
    time_of_day = utils.get_time_of_day(datetimes)
    time_of_year = utils.get_time_of_year(datetimes)

    result = utils.convert_to_columns(
        dates[:10], production[:10], time_of_day[:10], time_of_year[:10]
    )

    return mantik.types.Bundle(value=result)
