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

from mantik.types import MantikHeader
import json


def test_parse():
    sample = """
metaVariables:
  - name: width
    type: int32
    value: 100
type:
  input:
    columns:
      x:
        type: tensor
        componentType: float32
        shape: ["${width}"]
  output: float32 
    """

    mf = MantikHeader.parse(sample, ".")
    assert mf.payload_dir == "./payload"
    assert mf.type.input.representation == json.loads(
        '{"columns": {"x":{"type":"tensor","componentType":"float32","shape":[100]}}}'
    )
    assert mf.type.output.representation == json.loads('"float32"')
    assert mf.kind == "algorithm"
    assert mf.name == "unnamed"
    assert mf.meta_variables.get("width") == 100
