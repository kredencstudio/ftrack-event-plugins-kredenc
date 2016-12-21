import ftrack
import utils


def callback(event):
    """ This plugin sets the task status from the version status update.
    """

    for entity in event['data'].get('entities', []):

        # Filter non-assetversions
        if entity.get('entityType') == 'assetversion' and entity['action'] == 'add':
            version = ftrack.AssetVersion(id=entity.get('entityId'))

            asset_type = version.getAsset().getType().getShort()


            file_status = utils.get_status_by_name('file')

            # Setting task status
            try:
                if asset_type in ['cam', 'cache']:
                    version.setStatus(file_status)
            except Exception as e:
                print '%s status couldnt be set: %s' % (version.getName(), e)
            else:
                print '%s updated to "%s"' % (version.getName(), file_status.get('name'))


# Subscribe to events with the update topic.
ftrack.setup()
ftrack.EVENT_HUB.subscribe('topic=ftrack.update', callback)
ftrack.EVENT_HUB.wait()
