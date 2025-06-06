from google.cloud import bigquery

class BigQueryUtils:
    def __init__(self, project_id):
        self.client = bigquery.Client(project=project_id)

    def run_query(self, query):
        query_job = self.client.query(query)
        return query_job.result()

    def insert_rows_json(self, table_id, rows_to_insert):
        errors = self.client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            raise Exception(f"Errors occurred while inserting rows: {errors}")

    def fetch_data(self, query):
        query_job = self.client.query(query)
        return query_job.result().to_dataframe()

    def create_table(self, table_id, schema):
        table = bigquery.Table(table_id, schema=schema)
        table = self.client.create_table(table)
        return table

    def delete_table(self, table_id):
        self.client.delete_table(table_id, not_found_ok=True)

    def update_table_schema(self, table_id, new_schema):
        table = self.client.get_table(table_id)
        table.schema = new_schema
        self.client.update_table(table, ["schema"])

    def query(self, query):
        return [dict(row) for row in self.client.query(query).result()]

    def query_with_params(self, query, params):
        job_config = bigquery.QueryJobConfig(query_parameters=[
            bigquery.ScalarQueryParameter(p['name'], p['parameterType']['type'], p['parameterValue']['value'])
            for p in params
        ])
        return [dict(row) for row in self.client.query(query, job_config=job_config).result()]