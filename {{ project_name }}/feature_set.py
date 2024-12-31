from feature_store_dsl.types.feature import BatchEventFeature, Window, WindowType, Feature
from feature_store_dsl.types.aggregation import AggregationOperation
from feature_store_dsl.types.source import ExternalTable, EntityIdColumns, Table
from feature_store_dsl.io.sources.PostgresSource import PostgresSource
from feature_store_dsl.types.entity import BaseEntity, DataType, Entity
from feature_store_dsl.types.feature_set import FeatureSet
from feature_store_dsl.io.sinks.PostgresSink import PostgresSink
from openapi_client import ApiClient, Configuration


source = PostgresSource(
    jdbc_url="jdbc:postgresql://localhost:5432/mydb",
    user="admin",
    password="secret",
    tables=""
)

sink = PostgresSink(
    jdbc_url="jdbc:postgresql://localhost:5432/mydb",
    user="admin",
    password="secret",
    schema="public"
)

entity = BaseEntity(
    name="user_id_updated_re_re",
    output_column="id",
    data_type=DataType.STRING
)
config = Configuration(host='http://localhost:8083')
api_client = ApiClient(config)
# entity.register(api_client=api_client)

table = ExternalTable(
    source=source,
    entity_id_columns=[EntityIdColumns(
        entity=entity,
        entity_key_column="purchase_price"
    )],
    table_time_semantics=None,
    name="checkouts_updated",
    description=""
)

table.register(api_client)

window = Window(window_type=WindowType.DAY_WINDOW, window_size=7)

feature = BatchEventFeature(
    name="testing_feature",
    description="this is description",
    aggregation=AggregationOperation.COUNT,
    aggregation_expression="refund_amt",
    window=window,
    table=table
)

feature.register(api_client=api_client)


feature_set = FeatureSet(
    name="sample_feature_set",
    features=[feature],
    description="",
    table=table,
    sinks=[sink]
)

# feature_set.compile()

# feature_set.run()
