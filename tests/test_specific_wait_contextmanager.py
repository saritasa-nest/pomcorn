from pomcorn import Page


def test_specific_wait_context_manager(fake_page: Page):
    """Test that specific_wait context manager changes works correctly.

    It changes the wait timeout only inside the context manager
    and restores it after exiting the context manager.

    """
    original_timeout = fake_page.wait._timeout
    new_timeout = original_timeout * 2

    with fake_page.specific_wait(new_timeout):
        assert fake_page.wait._timeout == new_timeout

    assert fake_page.wait._timeout == original_timeout
