import ftrack
import utils

def callback(event):
    """ This plugin triggers when a task's status is updated to any DONE state.
    It searches for the next task via the sorting order in System settings>Types,
    and sets the next task to "Not started" if the next task is set to "Not ready".
    """

    for entity in event['data'].get('entities', []):

        # Filter to only tasks
        if entity.get('entityType') == 'task' and entity['action'] == 'update':

            # Find task if it exists
            task = None
            try:
                task = ftrack.Task(id=entity.get('entityId'))
            except:
                return

            # Filter to tasks only
            if task and task.get('objecttypename') == 'Task':

                # Setting next task to NOT STARTED, if on NOT READY
                if task.getStatus().get('state') == 'DONE':
                    next_task = utils.GetNextTask(task)
                    if next_task:
                        if next_task.getStatus().get('state') == 'NOT_STARTED':
                            if next_task.getStatus().get('name').lower() == 'not ready'.lower():

                                # Get path to next task
                                path = next_task.get('name')
                                for p in task.getParents():
                                    path = p.get('name') + '/' + path

                                # Setting next task status
                                try:
                                    next_task.setStatus(utils.GetStatusByName('ready'))
                                    print '%s updated to "Ready"' % path
                                except Exception as e:
                                    print '%s status couldnt be set: %s' % (path, e)
                                else:
                                    print '%s updated to "Ready"' % path


# Subscribe to events with the update topic.
ftrack.setup()
ftrack.EVENT_HUB.subscribe('topic=ftrack.update', callback)
ftrack.EVENT_HUB.wait()
