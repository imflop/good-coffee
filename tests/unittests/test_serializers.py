from good_coffee.lib.serializers.keyboard import Button, Keyboard


def test_keyboard():
    k = Keyboard(keyboard=[[Button(text="text")]])
    assert len(k.keyboard) == 1
