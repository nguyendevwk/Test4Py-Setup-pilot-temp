import importlib
import sys
from pathlib import Path

import pytest

# Import the target function
from httpie.utils import get_site_paths


def test_get_site_paths_non_frozen(tmp_path: Path):
    """
    When the application is not frozen, get_site_paths should yield a single
    path constructed by as_site with the original path.
    """
    # Ensure the compatibility module reports not frozen
    compat = importlib.import_module("httpie.compat")
    original_is_frozen = compat.is_frozen
    compat.is_frozen = False

    try:
        # Call the function with a temporary path
        result = list(get_site_paths(tmp_path))

        # There should be exactly one path yielded
        assert len(result) == 1
        # The yielded path should be the same as the input path
        assert result[0] == tmp_path
    finally:
        # Restore original state
        compat.is_frozen = original_is_frozen


def test_get_site_paths_frozen_version_range(tmp_path: Path):
    """
    When the application is frozen, get_site_paths should yield a path for
    each supported Python minor version between MIN_SUPPORTED_PY_VERSION and
    MAX_SUPPORTED_PY_VERSION inclusive.
    """
    compat = importlib.import_module("httpie.compat")
    original_is_frozen = compat.is_frozen
    original_min = compat.MIN_SUPPORTED_PY_VERSION
    original_max = compat.MAX_SUPPORTED_PY_VERSION

    # Set up a controlled environment
    compat.is_frozen = True
    compat.MIN_SUPPORTED_PY_VERSION = [3, 8]
    compat.MAX_SUPPORTED_PY_VERSION = [3, 10]

    try:
        result = list(get_site_paths(tmp_path))
        # Expect three paths: 3.8, 3.9, 3.10
        expected_versions = ["3.8", "3.9", "3.10"]
        assert len(result) == len(expected_versions)

        # Each yielded path should end with the corresponding version string
        for path, ver in zip(result, expected_versions):
            assert path.name.endswith(ver)
    finally:
        # Restore original state
        compat.is_frozen = original_is_frozen
        compat.MIN_SUPPORTED_PY_VERSION = original_min
        compat.MAX_SUPPORTED_PY_VERSION = original_max


def test_get_site_paths_frozen_single_version(tmp_path: Path):
    """
    When the application is frozen and the supported version range is a single
    version, get_site_paths should yield exactly one path with that version.
    """
    compat = importlib.import_module("httpie.compat")
    original_is_frozen = compat.is_frozen
    original_min = compat.MIN_SUPPORTED_PY_VERSION
    original_max = compat.MAX_SUPPORTED_PY_VERSION

    compat.is_frozen = True
    compat.MIN_SUPPORTED_PY_VERSION = [3, 9]
    compat.MAX_SUPPORTED_PY_VERSION = [3, 9]

    try:
        result = list(get_site_paths(tmp_path))
        assert len(result) == 1
        # The single yielded path should end with '3.9'
        assert result[0].name.endswith("3.9")
    finally:
        compat.is_frozen = original_is_frozen
        compat.MIN_SUPPORTED_PY_VERSION = original_min
        compat.MAX_SUPPORTED_PY_VERSION = original_max
