import pytest
from youtube_dl.downloader.f4m import build_fragments_list

def test_normal_fragments_list():
    boot_info = {
        'segments': [{'segment_run': [('seg1', 3), ('seg2', 2)]}],
        'fragments': [{'fragments': [{'first': 10}]}],
        'live': False
    }
    result = build_fragments_list(boot_info)
    expected = [
        ('seg1', 10), ('seg1', 11), ('seg1', 12),
        ('seg2', 13), ('seg2', 14)
    ]
    assert result == expected

def test_live_boundary_fragments_count():
    boot_info = {
        'segments': [{'segment_run': [('seg1', 4294967295)]}],
        'fragments': [{'fragments': [{'first': 5}]}],
        'live': True
    }
    result = build_fragments_list(boot_info)
    # For live streams, fragments_count is forced to 2 and only last two are kept
    assert result == [('seg1', 6), ('seg1', 7)]

def test_non_live_large_fragments_count():
    boot_info = {
        'segments': [{'segment_run': [('seg1', 4294967295)]}],
        'fragments': [{'fragments': [{'first': 0}]}],
        'live': False
    }
    result = build_fragments_list(boot_info)
    # Non‑live streams keep the original large count
    assert len(result) == 4294967295
    assert result[0] == ('seg1', 0)
    assert result[-1] == ('seg1', 4294967294)
