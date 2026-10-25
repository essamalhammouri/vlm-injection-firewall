from collections import Counter

from vlmfw.splits import assign_split, make_split_table

RATIOS = {"train": 0.70, "val": 0.15, "test": 0.15}


def test_assignment_is_deterministic():
    assert assign_split("000000000139", RATIOS, 1337) == assign_split("000000000139", RATIOS, 1337)


def test_assignment_depends_on_seed():
    ids = [str(i) for i in range(200)]
    a = [assign_split(i, RATIOS, 1) for i in ids]
    b = [assign_split(i, RATIOS, 2) for i in ids]
    assert a != b


def test_ratios_are_respected():
    counts = Counter(assign_split(str(i), RATIOS, 1337) for i in range(10_000))
    for name, share in RATIOS.items():
        assert abs(counts[name] / 10_000 - share) < 0.02, name


def test_split_table_one_row_per_photo_no_duplicates(tmp_path):
    for name in ["a.jpg", "b.jpg", "c.png", "notes.txt"]:
        (tmp_path / name).write_bytes(b"x")
    table = make_split_table(tmp_path, RATIOS, 1337)
    assert list(table["source_id"]) == ["a", "b", "c"]  # txt ignored, sorted
    assert table["source_id"].is_unique
    assert set(table["split"]) <= set(RATIOS)


def test_adding_photos_does_not_move_existing_ones(tmp_path):
    (tmp_path / "a.jpg").write_bytes(b"x")
    before = make_split_table(tmp_path, RATIOS, 1337).set_index("source_id")["split"]
    (tmp_path / "b.jpg").write_bytes(b"x")
    after = make_split_table(tmp_path, RATIOS, 1337).set_index("source_id")["split"]
    assert before["a"] == after["a"]
