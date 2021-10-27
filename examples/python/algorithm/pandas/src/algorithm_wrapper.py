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


# Wraps the supplied algorithm
class AlgorithmWrapper(mantik.bridge.Algorithm):
    def __init__(self, mantikheader: mantik.types.MantikHeader):
        # TODO: I am pretty sure there is a nicer way to do so
        import sys

        sys.path.append(mantikheader.payload_dir)
        import algorithm

        self.apply_func = algorithm.apply
        self.mantikheader = mantikheader

    def apply(self, data: mantik.types.Bundle):
        return self.apply_func(data, self.mantikheader.meta_variables)
