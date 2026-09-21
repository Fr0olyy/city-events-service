"""Тесты функций модуля storage."""
import os
import tempfile

from storage import load_json, save_json


def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.json")
        data = {"1": {"id": 1, "name": "Тест"}}
        save_json(path, data)
        loaded = load_json(path, {})
        assert loaded == data


def test_load_missing_file_returns_default():
    assert load_json("no_such_file.json", {}) == {}


def test_load_corrupted_file_returns_default():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "bad.json")
        with open(path, "w", encoding="utf-8") as file:
            file.write("{not valid json")
        assert load_json(path, []) == []
