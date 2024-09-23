from omegaconf_cloud_resolvers.resolvers.aux import try_infer_and_cast, try_cast_to_dict


def test_cast_string_1():
    assert try_infer_and_cast("qwerty") == "qwerty"


def test_cast_string_3():
    assert try_infer_and_cast("123.abc") == "123.abc"


def test_cast_int():
    try_infer_and_cast("1")


def test_cast_int_unstrip():
    value = try_infer_and_cast("  12  ")
    assert value == 12
    assert isinstance(value, int)


def test_cast_float():
    value = try_infer_and_cast("1.0")
    assert value == 1.0
    assert isinstance(value, float)


def test_case_bool_true():
    value = try_infer_and_cast("True")
    assert value
    assert isinstance(value, bool)


def test_case_bool_false():
    value = try_infer_and_cast("false ")
    assert not value
    assert isinstance(value, bool)


def test_cast_float_scientific():
    value = try_infer_and_cast("1E3")
    assert value == 1e3
    assert isinstance(value, float)


def test_cast_dict():
    dstr = "{'a': 1, 'b': True, 'c': 1.0, 'd' : {'dd': 'qwerty'}, 1: 1}"
    d = {"a": 1, "b": True, "c": 1.0, "d": {"dd": "qwerty"}, 1: 1}
    d_cast = try_cast_to_dict(dstr)
    assert d_cast == d
