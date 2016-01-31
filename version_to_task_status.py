import sys
import os
import ftrack
import utils


def callback(event):
    """ This plugin sets the task status from the version status update.
    """

    for entity in event['data'].get('entities', []):

        # Filter non-assetversions
        if entity.get('entityType') == 'assetversion' and entity['action'] == 'update':
            version = ftrack.AssetVersion(id=entity.get('entityId'))
            version_status = version.getStatus()
            task_status = version_status
            try:
                # task = ftrack.Task(version.get('taskid'))
                task = version.getTask()
            except:
                return

            # task_status = utils.GetStatusByName(version_status.get('name').lower())

            # Filter to versions with status change to "render complete"
            if version_status.get('name').lower() == 'reviewed':
                task_status = utils.GetStatusByName('change requested')

            if version_status.get('name').lower() == 'approved':
                task_status = utils.GetStatusByName('complete')

            if version_status.get('name').lower() == 'client review':
                task_status = utils.GetStatusByName('pending review')


            # Proceed if the task status was set
            if task_status:
                # Get path to task
                path = task.get('name')
                for p in task.getParents():
                    path = p.get('name') + '/' + path

                # Setting task status
                try:
                    task.setStatus(task_status)
                except Exception as e:
                    print '%s status couldnt be set: %s' % (path, e)
                else:
                    print '%s updated to "%s"' % (path, task_status.get('name'))


# Subscribe to events with the update topic.
ftrack.setup()
ftrack.EVENT_HUB.subscribe('topic=ftrack.update', callback)
ftrack.EVENT_HUB.wait()
