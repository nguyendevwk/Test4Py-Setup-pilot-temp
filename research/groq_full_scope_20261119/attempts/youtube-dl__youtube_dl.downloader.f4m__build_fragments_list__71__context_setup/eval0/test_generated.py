import pytest
from youtube_dl.downloader.f4m import build_fragments_list

def test_normal_non_live_segments():
    boot_info = {
        'segments': [
            {
                'segment_run': [
                    ('seg1', 2),
                    ('seg2', 1),
                ]
            }
        ],
        'fragments': [
            {
                'fragments': [
                    {'first': 0}
                ]
            }
        ],
        'live': False
    }
    result = build_fragments_list(boot_info)
    # Expected: seg1 with frag 0 and 1, seg2 with frag 2
    assert result == [('seg1', 0), ('seg1', 1), ('seg2', 2)]

def test_live_truncation_and_abnormal_count():
    boot_info = {
        'segments': [
            {
                'segment_run': [
                    ('segA', 4294967295),  # abnormal count
                    ('segB', 3),
                ]
            }
        ],
        'fragments': [
            {
                'fragments': [
                    {'first': 10}
                ]
            }
        ],
        'live': True
    }
    result = build_fragments_list(boot_info)
    # For live, only last two fragments should be kept
    # Normal count is replaced by 2 for abnormal value
    # Fragment numbers: 10,11,12,13,14,15 -> last two are 14,15
    assert result == [('segB', 14), ('segB', 15)]

def test_fragment_counter_start_and_multiple_segments():
    boot_info = {
        'segments': [
            {
                'segment_run': [
                    ('segX', 1),
                    ('segY', 2),
                ]
            }
        ],
        'fragments': [
            {
                'fragments': [
                    {'first': 5}
                ]
            }
        ],
        'live': False
    }
    result = build_fragments_list(boot_info)
    # Fragment numbers should start at 5 and increment
    assert result == [('segX', 5), ('segY', 6), ('segY', 7)]
