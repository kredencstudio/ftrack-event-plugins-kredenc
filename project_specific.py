import sys
import os
import logging
import ftrack
import utils


def callback(event):
    '''Event callback printing all new or updated entities.'''

    if 'PROJECT_ID' not in event['data']['parents']:
        return


# Subscribe to events with the update topic.
ftrack.setup()
ftrack.EVENT_HUB.subscribe('topic=ftrack.update', callback)
ftrack.EVENT_HUB.wait()
