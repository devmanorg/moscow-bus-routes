from routes_fetcher import get_ordered_route_segments


def test_get_ordered_route_segments_with_empty_source_list():
    source_route_segments = []
    ordered_route_segments = get_ordered_route_segments(source_route_segments)

    assert ordered_route_segments == []


def test_get_ordered_route_segments_with_ordered_source_list_with_one_trajectory():
    source_route_segments = [
        [[1, 1], [0, 0]],
        [[2, 3], [1, 1]],
        [[4, 4], [2, 3]],
        [[3, 1], [4, 4]],
        [[0, 0], [3, 1]],
    ]
    ordered_route_segments = get_ordered_route_segments(source_route_segments)

    assert ordered_route_segments == [
        [[1, 1], [0, 0]],
        [[2, 3], [1, 1]],
        [[4, 4], [2, 3]],
        [[3, 1], [4, 4]],
        [[0, 0], [3, 1]],
    ]


def test_get_ordered_route_segments_with_unordered_source_list_with_one_trajectory():
    source_route_segments = [
        [[1, 1], [0, 0]],
        [[4, 4], [2, 3]],
        [[0, 0], [3, 1]],
        [[3, 1], [4, 4]],
        [[2, 3], [1, 1]],
    ]
    ordered_route_segments = get_ordered_route_segments(source_route_segments)

    assert ordered_route_segments == [
        [[1, 1], [0, 0]],
        [[2, 3], [1, 1]],
        [[4, 4], [2, 3]],
        [[3, 1], [4, 4]],
        [[0, 0], [3, 1]],
    ]


def test_get_ordered_route_segments_with_ordered_source_list_with_two_trajectories():
    source_route_segments = [
        [[1, 1], [0, 0]],
        [[2, 3], [1, 1]],
        [[4, 4], [2, 3]],
        [[4, 2], [6, 3]],
        [[7, 1], [4, 2]],
        [[2, 0], [7, 1]],
    ]
    ordered_route_segments = get_ordered_route_segments(source_route_segments)

    assert ordered_route_segments == [
        [[1, 1], [0, 0]],
        [[2, 3], [1, 1]],
        [[4, 4], [2, 3]],
        [[4, 2], [6, 3]],
        [[7, 1], [4, 2]],
        [[2, 0], [7, 1]],
    ]


def test_get_ordered_route_segments_with_unordered_source_list_with_two_trajectories():
    source_route_segments = [
        [[1, 1], [0, 0]],
        [[4, 2], [6, 3]],
        [[2, 3], [1, 1]],
        [[2, 0], [7, 1]],
        [[7, 1], [4, 2]],
        [[4, 4], [2, 3]],
    ]
    ordered_route_segments = get_ordered_route_segments(source_route_segments)

    assert ordered_route_segments == [
        [[1, 1], [0, 0]],
        [[2, 3], [1, 1]],
        [[4, 4], [2, 3]],
        [[4, 2], [6, 3]],
        [[7, 1], [4, 2]],
        [[2, 0], [7, 1]],
    ]
