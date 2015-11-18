import ftrack
import utils

import pprint


def callback(event):
    """ This plugin creates a thumbnail from the first available thumbnail in the entity's parents.
    """
    # update created task thumbnail with first parent thumbnail
    for entity in event['data'].get('entities', []):
        if entity['entityType'] == 'task' and entity['action'] == 'add':
            try:
                task = ftrack.Task(id=entity['entityId'])
            except:
                continue

            if not task.get('thumbid'):

                thumbnail = utils.getThumbnailRecursive(task)
                if thumbnail:
                    task.setThumbnail(thumbnail)
                    parent = task.getParent()
                    log.info('Updating thumbnail for task %s/%s' % (parent.getName(), task.getName()))

        # Update task thumbnail from published version
        if entity['entityType'] == 'assetversion' and entity['action'] == 'encoded':

            pprint.pprint(entity)
            try:
                version = ftrack.AssetVersion(id=entity.get('entityId'))
                task = ftrack.Task(version.get('taskid'))
                thumbid = version.get('thumbid')
            except:
                continue

            if thumbid:
                task.setThumbnail(ftrack.Attachment(id=thumbid))
                parent = task.getParent()
                parent.setThumbnail(ftrack.Attachment(id=thumbid))

                log.info('Updating thumbnail for task and shot %s/%s' % (parent.getName(), task.getName()))




# Subscribe to events with the update topic.
ftrack.setup()
ftrack.EVENT_HUB.subscribe('topic=ftrack.update', callback)
ftrack.EVENT_HUB.wait()
