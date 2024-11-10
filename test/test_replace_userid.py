import pytest
from fetch_weekly import replace_userid_in_text

@pytest.fixture
def text():
    return "Hello <@U07U90DGGFR>, how are you <@U07U8GZNN1M>? Have you met <@U07U90DGGFR>?"

def test_replace_userid_in_text(text):
    assert replace_userid_in_text(text) == "Hello <@LinaBot>, how are you <@Lina>? Have you met <@LinaBot>?"
