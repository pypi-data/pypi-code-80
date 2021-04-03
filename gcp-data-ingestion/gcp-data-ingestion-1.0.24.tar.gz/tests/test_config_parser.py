from ingestion.config.parser import ConfigurationParser


class TestConfiguration:

    def test(self):
        config_str = """
        global_params:
          target_dataset_id: 'raw'
          bucket_name: "ecommerce-data-ingestion"
        feeds:
          - feed_id: 'makt'
            source_system: 'sap'
            feed_type: 'incremental'
            file_path_prefix: 'sap/product/makt/'
            field_delimiter: ","
            target_table_name: 'makt'
            file_encoding: 'utf-8'
            source_columns: [
              'CLIENT', 'MATERIAL', 'LANGUAGE','DESCRIPTION1', 'DESCRIPTION2'
            ]
            default_value_for_missing_columns: {
              'CLIENT':'700'
            }
        
        """
        parser = ConfigurationParser(config_str)
        assert len(parser.model.feeds) == 1

        first_feed = parser.model.feeds[0]
        assert parser.model.global_params['bucket_name'] == "ecommerce-data-ingestion"
        assert type(first_feed.default_value_for_missing_columns) == dict
        assert first_feed.source_system == 'sap'
        mcv = first_feed.default_value_for_missing_columns
        for k, v in mcv.items():
            print(k, v)
