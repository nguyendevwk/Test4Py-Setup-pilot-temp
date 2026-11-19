import pytest
from youtube_dl.downloader.f4m import build_fragments_list

def test_build_fragments_list_normal():
    boot_info = {
        'segments': [{'segment_run': [(1, 2), (2, 1)]}],
        'fragments': [{'fragments': [{'first': 0}]}],
        'live': False
    }
    result = build_fragments_list(boot_info)
    # Expected: segment 1 with fragments 0,1; segment 2 with fragment 2
    assert result == [(1, 0), (1, 1), (2, 2)]

def test_build_fragments_list_live_abnormal_count():
    boot_info = {
        'segments': [{'segment_run': [(1, 4294967295), (2, 1)]}],
        'fragments': [{'fragments': [{'first': 10}]}],
        'live': True
    }
    result = build_fragments_list(boot_info)
    # For live, abnormal count is replaced by 2, and only last two fragments are kept
    # fragments_counter starts at 10, so fragments 10,11 for segment 1, then 12 for segment 2
    # After trimming, we keep fragments 11 and 12
    assert result == [(1, 11), (2, 12)]

def test_build_fragments_list_live_normal_count():
    boot_info = {
        'segments': [{'segment_run': [(1, 3), (2, 2)]}],
        'fragments': [{'fragments': [{'first': 5}]}],
        'live': True
    }
    result = build_fragments_list(boot_info)
    # fragments_counter starts at 5, so fragments 5,6,7 for segment 1, 8,9 for segment 2
    # For live, keep last two fragments: 8 and 9
    assert result == [(2, 8), (2, 9)]
