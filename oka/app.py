import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

origin_key = os.environ.get('CUSTOM_ORIGIN_KEY')


def handler(event, context):
    key = event.get('headers', {}).get('x-custom-origin-key', '')
    if key == origin_key:
        return {
            'isAuthorized': True,
            'context': {}
        }
    else:
        rc = event['requestContext']
        uri = rc['domainName'] + rc['http']['path']
        logger.info("CIS_AUTH_FAIL: Attempt to reach endpoint"
                    f" {uri} without origin key")
        return {
            'isAuthorized': False,
            'context': {}
        }
