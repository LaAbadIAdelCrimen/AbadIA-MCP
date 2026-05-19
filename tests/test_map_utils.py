import pytest
import os
import json
import server.config

# The goal is to verify map_utils while handling its dependencies
from server.map_utils import load_map, save_map, draw_map_ascii

def test_load_save_map_integration(tmp_path, mocker):
    # Set the config before any other logic runs in the function
    tmp_dir = str(tmp_path)
    mocker.patch("server.map_utils.STORE_PATH", tmp_dir)
    
    map_data = [[ [{"h": 10}] ]]
    save_map("test_io", map_data)
    
    # Verify file existence manually first to isolate failure
    expected_path = os.path.join(tmp_dir, "test_io.json")
    assert os.path.exists(expected_path)
    
    loaded = load_map("test_io")
    assert loaded == map_data

def test_load_map_not_found(tmp_path, mocker):
    mocker.patch("server.map_utils.STORE_PATH", str(tmp_path))
    assert load_map("void") == []

def test_draw_map_ascii_rendering():
    map_data = [[
        [{"h": 5}, {"h": 18}],
        [{"h": 14}, {"h": 5, "c": 1}]
    ]]
    output = draw_map_ascii(map_data, floor=0, center_x=1, center_y=1, cells=1)
    assert "." in output
    assert "P" in output
    assert "#" in output
    assert "C" in output
    assert "not available" in draw_map_ascii(map_data, floor=5)

def test_draw_map_out_of_bounds_and_null():
    map_data = [[
        [None, {"h": 5}],
        [{"h": 5}, {"h": 5}]
    ]]
    output = draw_map_ascii(map_data, floor=0, center_x=0, center_y=0, cells=2)
    assert "-" in output
    assert "+" in output
    output = draw_map_ascii(map_data, floor=0, center_x=0, center_y=0, cells=1)
    assert "+" in output

def test_draw_map_objects():
    map_data = [[ [ {"h": 5, "o": 1} ] ]]
    output = draw_map_ascii(map_data, floor=0, center_x=0, center_y=0, cells=1)
    assert "O" in output
