import json

from django.shortcuts import render
from django.http import Http404

from django.conf import settings

from dv_apps.datasets.models import Dataset, DatasetVersion, VERSION_STATE_RELEASED
from dv_apps.datasets.util import get_latest_dataset_version
from dv_apps.dataverses.models import Dataverse
from dv_apps.dataverses.serializer import DataverseSerializer
from django.views.decorators.cache import cache_page

from dv_apps.datasets.serializer import DatasetSerializer

@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_dataset_by_persistent_id(request):

    persistent_id = request.GET.get('persistentId', None)
    if persistent_id is None:
        raise Http404('persistentId not found: %s' % persistent_id)

    ds = Dataset.get_dataset_by_persistent_id(persistent_id)
    if ds is None:
        raise Http404('persistentId not found: %s' % persistent_id)

    dsv = get_latest_dataset_version(ds.dvobject.id)

    if dsv is None:
        raise Http404('dataset_id not found')

    return view_dataset_by_version(request, dsv.id)

@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_single_dataset(request, dataset_id):
    """Dataset view test.  Given dataset id, get latest version"""

    dsv = get_latest_dataset_version(dataset_id)

    if dsv is None:
        raise Http404('dataset_id not found')

    return view_dataset_by_version(request, dsv.id)


def view_get_slack_dataset_info(dataset_id, **kwargs):

    citation_only = kwargs.get('citation', False)

    dsv = get_latest_dataset_version(dataset_id)
    if dsv is None:
        return "Sorry, no Dataset found for id: %s" % dataset_id

    dataset_dict = DatasetSerializer(dsv).as_json()

    ref_url = '%s/dataset.xhtml?id=%s' % (\
                    settings.DATAVERSE_INSTALLATION_URL,
                    dataset_id)

    if citation_only:
        citation_block = dataset_dict.get('metadata_blocks', {}).get('citation')

        return """%s\n\nreference: %s""" %\
            (json.dumps(citation_block, indent=4), ref_url)



    return """%s\n\nreference: %s""" %\
        (json.dumps(dataset_dict, indent=4), ref_url)



"""
http://127.0.0.1:8000/miniverse/dvobjects/api/v1/datasets/by-persistent-id?persistentID=doi:10.7910/DVN/26935

http://127.0.0.1:8000/miniverse/dvobjects/api/v1/datasets/by-id/53121

http://127.0.0.1:8000/miniverse/dvobjects/api/v1/datasets/by-version-id/79678
"""

@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_dataset_by_version(request, dataset_version_id):
    """Dataset view test.  Given dataset version id, render HTML"""

    try:
        dsv = DatasetVersion.objects.select_related('dataset')\
            .get(pk=dataset_version_id,
                versionstate=VERSION_STATE_RELEASED)
    except DatasetVersion.DoesNotExist:
        raise Http404

    dataset_dict = DatasetSerializer(dsv).as_json()
    citation_block=dataset_dict.get('metadata_blocks', {}).get('citation')

    dataverse_id = dataset_dict['ownerInfo']['id']
    try:
        dataverse = Dataverse.objects.select_related('dvobject')\
                .get(dvobject__id=dataverse_id)
    except Dataverse.DoesNotExist:
        raise Http404('No Dataverse with id: %s' % dataverse_id)

    dataverse_dict = DataverseSerializer(dataverse).as_json()

    metadata_blocks = dataset_dict.get('metadata_blocks', None)
    metadata_blocks_as_json = json.dumps(metadata_blocks, indent=4)

    lu = dict(ds=dataset_dict,
            dv=dataverse_dict,
            citation_block=citation_block,
            metadata_blocks_as_json=metadata_blocks_as_json)

    return render(request, 'dvobject_api/dataset_view.html', lu)
