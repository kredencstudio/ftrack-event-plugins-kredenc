import sys
import os
import ftrack
import utils


def callback(event):
    """ This plugin sets the task status from the version status update.
    """

    for entity in event['data'].get('entities', []):

        # Filter non-assetversions
        if entity['entityType'] == 'assetversion' and entity['action'] == 'add':
            version = ftrack.AssetVersion(id=entity.get('entityId'))
            task = ftrack.Task(version.get('taskid'))
            current_task_status = task.getStatus().getName()
            version.getAsset().getType().getName()
            version.getAsset().getName()

            if current_task_status.lower() == 'blocking':
                comment = version.getComment()
                comment = 'BLOCKING: ' + comment
                version.set('comment', value=comment)



# Subscribe to events with the update topic.
ftrack.setup()
ftrack.EVENT_HUB.subscribe('topic=ftrack.update', callback)
ftrack.EVENT_HUB.wait()
