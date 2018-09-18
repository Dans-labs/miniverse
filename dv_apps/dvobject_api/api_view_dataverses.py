from dv_apps.metrics.stats_view_base import StatsViewSwagger
from dv_apps.metrics.stats_result import StatsResult
from dv_apps.dataverses.models import Dataverse
from dv_apps.dataverses.serializer import DataverseSerializer

#from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
# limit the API rates
#from ratelimit.decorators import ratelimit

class DataverseByIdView(StatsViewSwagger):
    """View a Dataverse By Id"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/dataverses/by-id/{dv_id}'
    summary = ('Retrieve published Dataverse object in JSON format.')
    description = ('Retrieve Dataverse object in JSON format.')
    description_200 = 'Retrieve Dataverse object in JSON format.'
    param_names = StatsViewSwagger.PARAM_DVOBJECT_ID\
                + StatsViewSwagger.PARAM_DV_API_KEY\
                + StatsViewSwagger.PRETTY_JSON_PARAM\
                #+ StatsViewSwagger.PUBLISH_PARAMS
    #tags = [StatsViewSwagger.TAG_TEST_API]
    tags = [StatsViewSwagger.TAG_TEST_API]
    result_name = StatsViewSwagger.RESULT_NAME_DATAVERSE

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""

        #dv_id = request.GET.get('id', None)
        dv_id = self.kwargs.get('dv_id', None)
        if dv_id is None:
            return StatsResult.build_error_result("No Dataverse id specified", 400)

        try:
            selected_dv = Dataverse.objects.select_related('dvobject').get(\
                dvobject__id=dv_id,\
                dvobject__publicationdate__isnull=False)
        except Dataverse.DoesNotExist:
            return StatsResult.build_error_result('No published Dataverse with id: %s' % dv_id, 404)

        dataverse_as_json = DataverseSerializer(selected_dv).as_json()

        return StatsResult.build_success_result(dataverse_as_json)


class DataverseByAliasView(StatsViewSwagger):
    """View a Dataverse By Alias"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/dataverses/by-alias/{alias}'
    summary = ('Retrieve published Dataverse object in JSON format.')
    description = ('Retrieve Dataverse object in JSON format.')
    description_200 = 'Retrieve Dataverse object in JSON format.'
    param_names = StatsViewSwagger.PARAM_DATAVERSE_ALIAS\
                + StatsViewSwagger.PARAM_DV_API_KEY\
                + StatsViewSwagger.PRETTY_JSON_PARAM\
                #+ StatsViewSwagger.PUBLISH_PARAMS
    #tags = [StatsViewSwagger.TAG_TEST_API]
    tags = [StatsViewSwagger.TAG_TEST_API]
    result_name = StatsViewSwagger.RESULT_NAME_DATAVERSE

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""

        #dv_id = request.GET.get('id', None)
        alias = self.kwargs.get('alias', None)
        if alias is None:
            return StatsResult.build_error_result("No Dataverse 'alias' specified", 400)

        try:
            selected_dv = Dataverse.objects.select_related('dvobject').get(\
                alias=alias,\
                dvobject__publicationdate__isnull=False)
        except Dataverse.DoesNotExist:
            return StatsResult.build_error_result('No published Dataverse with alias: %s' % alias, 404)

        dataverse_as_json = DataverseSerializer(selected_dv).as_json()

        return StatsResult.build_success_result(dataverse_as_json)
