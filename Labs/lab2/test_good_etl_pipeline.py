"""
Comprehensive test suite for ETL Pipeline
Demonstrates high code coverage and best testing practices
"""

import pytest
import pandas as pd
import os
from unittest.mock import Mock, patch, MagicMock
from good_etl_pipeline import (
    DataExtractor,
    DataTransformer,
    DataValidator,
    DataLoader,
    MetricsCalculator,
    ETLPipeline,
    PipelineConfig,
    DataCategory
)


@pytest.fixture
def sample_dataframe():
    """Create sample DataFrame for testing"""
    return pd.DataFrame({
        'price': [10.0, 20.0, 30.0],
        'quantity': [2, 3, 1],
        'product_name': ['Widget A', 'Widget B', 'Widget C']
    })


@pytest.fixture
def sample_dataframe_with_discount():
    """Create sample DataFrame with discount column"""
    return pd.DataFrame({
        'price': [10.0, 20.0, 30.0],
        'quantity': [2, 3, 1],
        'discount': [0.05, 0.15, 0.20]
    })


@pytest.fixture
def sample_dataframe_negative_values():
    """Create sample DataFrame with negative values"""
    return pd.DataFrame({
        'price': [10.0, -5.0, 30.0],
        'quantity': [2, -1, 1]
    })


@pytest.fixture
def pipeline_config():
    """Create test pipeline configuration"""
    return PipelineConfig(
        api_endpoint='https://test-api.example.com',
        database_url='postgresql://test:test@localhost/testdb',
        output_directory='./test_output'
    )


@pytest.fixture
def data_extractor(pipeline_config):
    """Create DataExtractor instance"""
    return DataExtractor(pipeline_config)


@pytest.fixture
def data_transformer():
    """Create DataTransformer instance"""
    return DataTransformer()


@pytest.fixture
def data_validator():
    """Create DataValidator instance"""
    return DataValidator()


@pytest.fixture
def data_loader(pipeline_config):
    """Create DataLoader instance"""
    return DataLoader(pipeline_config)


class TestPipelineConfig:
    """Test suite for PipelineConfig"""

    def test_config_creation(self, pipeline_config):
        """Test configuration object creation"""
        assert pipeline_config.api_endpoint == 'https://test-api.example.com'
        assert pipeline_config.database_url == 'postgresql://test:test@localhost/testdb'
        assert pipeline_config.output_directory == './test_output'

    @patch.dict(os.environ, {
        'API_ENDPOINT': 'https://env-api.com',
        'DATABASE_URL': 'postgresql://env:env@localhost/envdb',
        'OUTPUT_DIR': './env_output'
    })
    def test_config_from_env(self):
        """Test configuration loading from environment"""
        config = PipelineConfig.from_env()
        assert config.api_endpoint == 'https://env-api.com'
        assert config.database_url == 'postgresql://env:env@localhost/envdb'
        assert config.output_directory == './env_output'


class TestDataExtractor:
    """Test suite for DataExtractor"""

    def test_extract_from_csv_success(self, data_extractor, tmp_path):
        """Test successful CSV extraction"""
        csv_file = tmp_path / "test.csv"
        test_data = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        test_data.to_csv(csv_file, index=False)

        result = data_extractor.extract_from_csv(str(csv_file))

        assert result is not None
        assert len(result) == 2
        assert 'col1' in result.columns

    def test_extract_from_csv_file_not_found(self, data_extractor):
        """Test extraction with non-existent file"""
        result = data_extractor.extract_from_csv('nonexistent.csv')
        assert result is None

    def test_extract_from_csv_empty_file(self, data_extractor, tmp_path):
        """Test extraction from empty CSV file"""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")

        result = data_extractor.extract_from_csv(str(csv_file))
        assert result is None

    @patch('good_etl_pipeline.requests.get')
    def test_extract_from_api_success(self, mock_get, data_extractor):
        """Test successful API extraction"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 1, 'value': 100},
            {'id': 2, 'value': 200}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = data_extractor.extract_from_api('endpoint', 'test-key')

        assert result is not None
        assert len(result) == 2

    @patch('good_etl_pipeline.requests.get')
    def test_extract_from_api_failure(self, mock_get, data_extractor):
        """Test API extraction failure"""
        mock_get.side_effect = Exception("API Error")

        result = data_extractor.extract_from_api('endpoint', 'test-key')
        assert result is None


class TestDataTransformer:
    """Test suite for DataTransformer"""

    def test_transform_success(self, data_transformer, sample_dataframe):
        """Test successful data transformation"""
        result = data_transformer.transform(sample_dataframe)

        assert result is not None
        assert 'total' in result.columns
        assert 'category' in result.columns
        assert 'premium' in result.columns
        assert result['total'][0] == 20.0

    def test_transform_empty_dataframe(self, data_transformer):
        """Test transformation with empty DataFrame"""
        empty_df = pd.DataFrame()
        result = data_transformer.transform(empty_df)
        assert result is None

    def test_transform_none_input(self, data_transformer):
        """Test transformation with None input"""
        result = data_transformer.transform(None)
        assert result is None

    def test_transform_missing_columns(self, data_transformer):
        """Test transformation with missing required columns"""
        invalid_df = pd.DataFrame({'name': ['A', 'B']})
        result = data_transformer.transform(invalid_df)
        assert result is None

    def test_high_value_category(self, data_transformer):
        """Test high value category assignment"""
        df = pd.DataFrame({
            'price': [100.0, 200.0],
            'quantity': [10, 10]
        })

        result = data_transformer.transform(df)

        assert result is not None
        assert result['category'][0] == DataCategory.HIGH.value

    def test_low_value_category(self, data_transformer):
        """Test low value category assignment"""
        df = pd.DataFrame({
            'price': [1.0, 2.0],
            'quantity': [1, 1]
        })

        result = data_transformer.transform(df)

        assert result is not None
        assert result['category'][0] == DataCategory.LOW.value

    def test_premium_flag_true(self, data_transformer):
        """Test premium flag for high-priced items"""
        df = pd.DataFrame({
            'price': [60.0, 70.0],
            'quantity': [1, 1]
        })

        result = data_transformer.transform(df)

        assert result is not None
        assert result['premium'][0] is True

    def test_premium_flag_false(self, data_transformer):
        """Test premium flag for low-priced items"""
        df = pd.DataFrame({
            'price': [10.0, 20.0],
            'quantity': [1, 1]
        })

        result = data_transformer.transform(df)

        assert result is not None
        assert result['premium'][0] is False

    def test_discounted_flag_with_discount(self, data_transformer, sample_dataframe_with_discount):
        """Test discounted flag calculation"""
        result = data_transformer.transform(sample_dataframe_with_discount)

        assert result is not None
        assert 'discounted' in result.columns
        assert result['discounted'][0] is True

    def test_no_discounted_flag_without_discount(self, data_transformer, sample_dataframe):
        """Test no discounted flag when discount column missing"""
        result = data_transformer.transform(sample_dataframe)

        assert result is not None
        assert 'discounted' not in result.columns


class TestDataValidator:
    """Test suite for DataValidator"""

    def test_validate_success(self, data_validator, sample_dataframe):
        """Test successful validation"""
        result = data_validator.validate_and_clean(sample_dataframe)

        assert result is not None
        assert len(result) == len(sample_dataframe)

    def test_validate_empty_dataframe(self, data_validator):
        """Test validation with empty DataFrame"""
        empty_df = pd.DataFrame()
        result = data_validator.validate_and_clean(empty_df)
        assert result is None

    def test_validate_none_input(self, data_validator):
        """Test validation with None input"""
        result = data_validator.validate_and_clean(None)
        assert result is None

    def test_clean_negative_prices(self, data_validator, sample_dataframe_negative_values):
        """Test cleaning negative prices"""
        result = data_validator.validate_and_clean(sample_dataframe_negative_values)

        assert result is not None
        assert (result['price'] >= 0).all()

    def test_clean_negative_quantities(self, data_validator, sample_dataframe_negative_values):
        """Test cleaning negative quantities"""
        result = data_validator.validate_and_clean(sample_dataframe_negative_values)

        assert result is not None
        assert (result['quantity'] >= 0).all()


class TestDataLoader:
    """Test suite for DataLoader"""

    def test_save_to_csv_success(self, data_loader, sample_dataframe, tmp_path):
        """Test successful CSV save"""
        data_loader.config.output_directory = str(tmp_path)

        result = data_loader.save_to_csv(sample_dataframe, 'output.csv')

        assert result is True
        assert os.path.exists(tmp_path / 'output.csv')

    def test_save_to_csv_empty_dataframe(self, data_loader):
        """Test CSV save with empty DataFrame"""
        empty_df = pd.DataFrame()
        result = data_loader.save_to_csv(empty_df, 'output.csv')
        assert result is False

    def test_save_to_csv_none_input(self, data_loader):
        """Test CSV save with None input"""
        result = data_loader.save_to_csv(None, 'output.csv')
        assert result is False

    @patch('good_etl_pipeline.psycopg2.connect')
    def test_save_to_database_success(self, mock_connect, data_loader, sample_dataframe):
        """Test successful database save"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Add required columns
        df_with_total = sample_dataframe.copy()
        df_with_total['total'] = df_with_total['price'] * df_with_total['quantity']

        result = data_loader.save_to_database(df_with_total, 'sales')

        assert result is True
        assert mock_cursor.execute.call_count == len(df_with_total)

    def test_save_to_database_empty_dataframe(self, data_loader):
        """Test database save with empty DataFrame"""
        empty_df = pd.DataFrame()
        result = data_loader.save_to_database(empty_df, 'sales')
        assert result is False

    def test_save_to_database_no_url(self, pipeline_config, sample_dataframe):
        """Test database save without URL configured"""
        config = PipelineConfig(
            api_endpoint='https://test.com',
            database_url='',
            output_directory='./output'
        )
        loader = DataLoader(config)

        result = loader.save_to_database(sample_dataframe, 'sales')
        assert result is False


class TestMetricsCalculator:
    """Test suite for MetricsCalculator"""

    def test_calculate_metrics_success(self, sample_dataframe):
        """Test successful metrics calculation"""
        df_with_total = sample_dataframe.copy()
        df_with_total['total'] = df_with_total['price'] * df_with_total['quantity']

        metrics = MetricsCalculator.calculate(df_with_total)

        assert metrics is not None
        assert 'total_revenue' in metrics
        assert 'total_items' in metrics
        assert 'avg_price' in metrics
        assert metrics['total_items'] == 6

    def test_calculate_metrics_empty_dataframe(self):
        """Test metrics calculation with empty DataFrame"""
        empty_df = pd.DataFrame()
        metrics = MetricsCalculator.calculate(empty_df)
        assert metrics is None

    def test_calculate_metrics_none_input(self):
        """Test metrics calculation with None input"""
        metrics = MetricsCalculator.calculate(None)
        assert metrics is None


class TestETLPipeline:
    """Integration test suite for complete ETL Pipeline"""

    @patch('good_etl_pipeline.DataExtractor.extract_from_csv')
    @patch('good_etl_pipeline.DataLoader.save_to_csv')
    def test_pipeline_run_success(self, mock_save, mock_extract, sample_dataframe, pipeline_config):
        """Test complete pipeline execution"""
        mock_extract.return_value = sample_dataframe
        mock_save.return_value = True

        pipeline = ETLPipeline(pipeline_config)
        result = pipeline.run('input.csv', 'output.csv')

        assert result is True
        mock_extract.assert_called_once_with('input.csv')
        mock_save.assert_called_once()

    @patch('good_etl_pipeline.DataExtractor.extract_from_csv')
    def test_pipeline_run_extraction_failure(self, mock_extract, pipeline_config):
        """Test pipeline with extraction failure"""
        mock_extract.return_value = None

        pipeline = ETLPipeline(pipeline_config)
        result = pipeline.run('input.csv', 'output.csv')

        assert result is False

    @patch('good_etl_pipeline.DataExtractor.extract_from_csv')
    @patch('good_etl_pipeline.DataTransformer.transform')
    def test_pipeline_run_transformation_failure(self, mock_transform, mock_extract,
                                                   sample_dataframe, pipeline_config):
        """Test pipeline with transformation failure"""
        mock_extract.return_value = sample_dataframe
        mock_transform.return_value = None

        pipeline = ETLPipeline(pipeline_config)
        result = pipeline.run('input.csv', 'output.csv')

        assert result is False

    @patch('good_etl_pipeline.DataExtractor.extract_from_csv')
    @patch('good_etl_pipeline.DataLoader.save_to_csv')
    def test_pipeline_run_load_failure(self, mock_save, mock_extract,
                                        sample_dataframe, pipeline_config):
        """Test pipeline with load failure"""
        mock_extract.return_value = sample_dataframe
        mock_save.return_value = False

        pipeline = ETLPipeline(pipeline_config)
        result = pipeline.run('input.csv', 'output.csv')

        assert result is False

    def test_pipeline_default_config(self):
        """Test pipeline with default configuration"""
        pipeline = ETLPipeline()
        assert pipeline.config is not None
        assert pipeline.extractor is not None
        assert pipeline.transformer is not None
        assert pipeline.validator is not None
        assert pipeline.loader is not None
