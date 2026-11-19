import pytest
from youtube_dl.downloader.f4m import build_fragments_list

def test_build_fragments_list_normal():
    # Normal case: one segment run with two fragments
    boot_info = {
        'segments': [{'segment_run': [('seg1', 2)]}],
        'fragments': [{'fragments': [{'first': 0}]}],
        'live': False
    }
    result = build_fragments_list(boot_info)
    # Expected: two tuples with segment 'seg1' and fragment numbers 0 and 1
    assert result == [('seg1', 0), ('seg1', 1)]

def test_build_fragments_list_live_boundary():
    # Live stream with abnormal fragment count 4294967295 should be capped to 2
    boot_info = {
        'segments': [{'segment_run': [('seg_live', 4294967295)]}],
        'fragments': [{'fragments': [{'first': 10}]}],
        'live': True
    }
    result = build_fragments_list(boot_info)
    # Expected: two tuples with segment 'seg_live' and fragment numbers 10 and 11
    assert result == [('seg_live', 10), ('seg_live', 11)]

def test_build_fragments_list_live_last_two():
    # Live stream with normal fragment count; only last two fragments should be kept
    boot_info = {
        'segments': [{'segment_run': [('seg_live', 4)]}],
        'fragments': [{'fragments': [{'first': 5}]}],
        'live': True
    }
    result = build_fragments_list(boot_info)
    # Expected: last two fragments: numbers 8 and 9
    assert result == [('seg_live', 8), ('seg_live', 9)]
