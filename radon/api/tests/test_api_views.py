from radon.api import views


def test_APIUsersLoginView_response_serializer(tp):
    view = tp.get_instance(views.APIUsersLoginView)
    ser = view.get_response_serializer()
    assert 2 == 1
