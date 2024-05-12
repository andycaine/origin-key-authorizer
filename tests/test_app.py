import oka.app


oka.app.origin_key = 'foo'


def _event(origin_key):
    return {
        'requestContext': {
            'http': {
                'path': '/testing'
            },
            'domainName': 'example.com'
        },
        'headers': {'x-custom-origin-key': origin_key}
    }


def test_matching_origin_key():
    assert oka.app.handler(_event('foo'), {}) == {
        'isAuthorized': True,
        'context': {}
    }


def test_non_matching_origin_key():
    assert oka.app.handler(_event('bar'), {}) == {
        'isAuthorized': False,
        'context': {}
    }


def test_no_origin_key_header():
    event = _event('')
    del event['headers']['x-custom-origin-key']
    assert oka.app.handler(event, {}) == {
        'isAuthorized': False,
        'context': {}
    }
