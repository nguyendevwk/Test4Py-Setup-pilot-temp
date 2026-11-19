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
    # Expected fragments: seg1 with 0,1; seg2 with 2
    assert result == [('seg1', 0), ('seg1', 1), ('seg2', 2)]

def test_live_abnormal_fragment_count():
    boot_info = {
        'segments': [
            {
                'segment_run': [
                    ('segA', 4294967295),  # abnormal count
                    ('segB', 1),
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
    # For live streams, abnormal count is replaced by 2 and only last two fragments kept
    # fragments_counter starts at 10, so we get 10,11 for segA, then 12 for segB
    # but live truncates to last two: (segB,12) and (segB,13)?? Wait compute:
    # segA: 2 fragments -> 10,11
    # segB: 1 fragment -> 12
    # total 3, last two are (segA,11) and (segB,12)
    assert result == [('segA', 11), ('segB', 12)]

def test_live_with_multiple_segments_and_normal_count():
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
        'live': True
    }
    result = build_fragments_list(boot_info)
    # fragments_counter: 5,6,7
    # live truncates to last two: (segY,6) and (segY,7)
    assert result == [('segY', 6), ('segY', 7)]
