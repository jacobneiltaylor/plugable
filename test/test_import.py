def test_plugable_import():
    import plugable.class_registry  # noqa: F401
    import plugable.plugable_meta  # noqa: F401
    import plugable  # noqa: F401
