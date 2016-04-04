import ftrack
import utils
import pprint


def callback(event):
    """ This plugin creates a thumbnail from the first available thumbnail in the entity's parents.
    """
    # update created task thumbnail with first parent thumbnail
    for entity in event['data'].get('entities', []):
        if entity.get('entityType') == 'task' and entity['action'] == 'add':
            task = None
            try:
                task = ftrack.Task(id=entity.get('entityId'))
            except:
                return

            parent = task.getParent()
            if parent.get('thumbid') and not task.get('thumbid'):
                task.set('thumbid', value=parent.get('thumbid'))
                print 'Updated thumbnail on %s/%s' % (parent.getName(),
                                                      task.getName())

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
                task.set('thumbid', value=thumbid)

                parent = task.getParent()
                parent.set('thumbid', value=thumbid)

                print 'Updating thumbnail for task and shot %s' % (task.getName())




# Subscribe to events with the update topic.
ftrack.setup()
ftrack.EVENT_HUB.subscribe('topic=ftrack.update', callback)
ftrack.EVENT_HUB.wait()
