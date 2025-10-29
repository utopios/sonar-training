"""
ETL Pipeline Module - Refactored Version
Demonstrates best practices for data processing pipelines
"""

import pandas as pd
import logging
import os
import json
from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataCategory(Enum):
    """Enum for data categorization"""
    HIGH = "high"
    LOW = "low"


@dataclass
class PipelineConfig:
    """Configuration class for ETL pipeline"""
    api_endpoint: str
    database_url: str
    output_directory: str

    @classmethod
    def from_env(cls) -> 'PipelineConfig':
        """Load configuration from environment variables"""
        return cls(
            api_endpoint=os.getenv('API_ENDPOINT', 'https://api.example.com'),
            database_url=os.getenv('DATABASE_URL', ''),
            output_directory=os.getenv('OUTPUT_DIR', './output')
        )


class DataExtractor:
    """Handle data extraction from various sources"""

    def __init__(self, config: PipelineConfig):
        self.config = config

    def extract_from_csv(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Extract data from CSV file

        Args:
            file_path: Path to CSV file

        Returns:
            DataFrame or None if extraction fails
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None

            df = pd.read_csv(file_path)
            logger.info(f"Successfully extracted {len(df)} rows from {file_path}")
            return df

        except pd.errors.EmptyDataError:
            logger.error(f"Empty CSV file: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            return None

    def extract_from_api(self, endpoint: str, api_key: str) -> Optional[pd.DataFrame]:
        """
        Extract data from API endpoint

        Args:
            endpoint: API endpoint path
            api_key: API authentication key

        Returns:
            DataFrame or None if extraction fails
        """
        try:
            import requests

            url = f"{self.config.api_endpoint}/{endpoint}"
            headers = {'Authorization': f'Bearer {api_key}'}

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            df = pd.DataFrame(data)

            logger.info(f"Successfully extracted {len(df)} rows from API")
            return df

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error processing API response: {str(e)}")
            return None


class DataTransformer:
    """Handle data transformation operations"""

    REQUIRED_COLUMNS = ['price', 'quantity']
    HIGH_VALUE_THRESHOLD = 1000
    PREMIUM_PRICE_THRESHOLD = 50
    HIGH_DISCOUNT_THRESHOLD = 0.1

    def _validate_dataframe(self, df: pd.DataFrame) -> bool:
        """
        Validate DataFrame has required columns

        Args:
            df: DataFrame to validate

        Returns:
            True if valid, False otherwise
        """
        if df is None or df.empty:
            logger.warning("Empty or None DataFrame provided")
            return False

        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            return False

        return True

    def _calculate_totals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate total values for each row"""
        df['total'] = df['price'] * df['quantity']
        return df

    def _categorize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Categorize data based on total value"""
        total_sum = df['total'].sum()
        df['category'] = (
            DataCategory.HIGH.value
            if total_sum > self.HIGH_VALUE_THRESHOLD
            else DataCategory.LOW.value
        )
        return df

    def _flag_premium(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flag premium items based on average price"""
        avg_price = df['price'].mean()
        df['premium'] = avg_price > self.PREMIUM_PRICE_THRESHOLD
        return df

    def _flag_discounted(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flag items with high discount if discount column exists"""
        if 'discount' in df.columns:
            avg_discount = df['discount'].mean()
            df['discounted'] = avg_discount > self.HIGH_DISCOUNT_THRESHOLD
        return df

    def transform(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Apply all transformations to DataFrame

        Args:
            df: Input DataFrame

        Returns:
            Transformed DataFrame or None if validation fails
        """
        if not self._validate_dataframe(df):
            return None

        try:
            df_copy = df.copy()
            df_copy = self._calculate_totals(df_copy)
            df_copy = self._categorize_data(df_copy)
            df_copy = self._flag_premium(df_copy)
            df_copy = self._flag_discounted(df_copy)

            logger.info("Data transformation completed successfully")
            return df_copy

        except Exception as e:
            logger.error(f"Error during transformation: {str(e)}")
            return None


class DataValidator:
    """Handle data validation and cleaning"""

    def validate_and_clean(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Validate and clean data

        Args:
            df: Input DataFrame

        Returns:
            Cleaned DataFrame or None if validation fails
        """
        if df is None or df.empty:
            logger.warning("Empty or None DataFrame provided for validation")
            return None

        try:
            df_copy = df.copy()

            # Clean negative prices
            if 'price' in df_copy.columns:
                negative_prices = (df_copy['price'] < 0).sum()
                if negative_prices > 0:
                    logger.warning(f"Found {negative_prices} negative prices, setting to 0")
                    df_copy.loc[df_copy['price'] < 0, 'price'] = 0

            # Clean negative quantities
            if 'quantity' in df_copy.columns:
                negative_qty = (df_copy['quantity'] < 0).sum()
                if negative_qty > 0:
                    logger.warning(f"Found {negative_qty} negative quantities, setting to 0")
                    df_copy.loc[df_copy['quantity'] < 0, 'quantity'] = 0

            logger.info("Data validation completed successfully")
            return df_copy

        except Exception as e:
            logger.error(f"Error during validation: {str(e)}")
            return None


class DataLoader:
    """Handle data loading to various destinations"""

    def __init__(self, config: PipelineConfig):
        self.config = config

    def save_to_csv(self, df: pd.DataFrame, filename: str) -> bool:
        """
        Save DataFrame to CSV file

        Args:
            df: DataFrame to save
            filename: Output filename

        Returns:
            True if successful, False otherwise
        """
        if df is None or df.empty:
            logger.warning("Cannot save empty DataFrame")
            return False

        try:
            os.makedirs(self.config.output_directory, exist_ok=True)
            output_path = os.path.join(self.config.output_directory, filename)

            df.to_csv(output_path, index=False)
            logger.info(f"Data saved to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            return False

    def save_to_database(self, df: pd.DataFrame, table_name: str) -> bool:
        """
        Save DataFrame to database using parameterized queries

        Args:
            df: DataFrame to save
            table_name: Target table name

        Returns:
            True if successful, False otherwise
        """
        if df is None or df.empty:
            logger.warning("Cannot save empty DataFrame to database")
            return False

        try:
            import psycopg2

            if not self.config.database_url:
                logger.error("Database URL not configured")
                return False

            conn = psycopg2.connect(self.config.database_url)
            cursor = conn.cursor()

            # Use parameterized query to prevent SQL injection
            query = f"INSERT INTO {table_name} (price, quantity, total) VALUES (%s, %s, %s)"

            for _, row in df.iterrows():
                cursor.execute(query, (row['price'], row['quantity'], row['total']))

            conn.commit()
            cursor.close()
            conn.close()

            logger.info(f"Successfully saved {len(df)} rows to database")
            return True

        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
            return False


class MetricsCalculator:
    """Calculate business metrics from data"""

    @staticmethod
    def calculate(df: pd.DataFrame) -> Optional[Dict[str, float]]:
        """
        Calculate key business metrics

        Args:
            df: DataFrame with sales data

        Returns:
            Dictionary of metrics or None if calculation fails
        """
        if df is None or df.empty:
            logger.warning("Cannot calculate metrics for empty DataFrame")
            return None

        try:
            metrics = {
                'total_revenue': df['total'].sum() if 'total' in df.columns else 0,
                'total_items': df['quantity'].sum() if 'quantity' in df.columns else 0,
                'avg_price': df['price'].mean() if 'price' in df.columns else 0,
                'record_count': len(df)
            }

            logger.info(f"Calculated metrics: {metrics}")
            return metrics

        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return None


class ETLPipeline:
    """Main ETL Pipeline orchestrator"""

    def __init__(self, config: Optional[PipelineConfig] = None):
        """
        Initialize ETL Pipeline

        Args:
            config: Pipeline configuration (loads from env if not provided)
        """
        self.config = config or PipelineConfig.from_env()
        self.extractor = DataExtractor(self.config)
        self.transformer = DataTransformer()
        self.validator = DataValidator()
        self.loader = DataLoader(self.config)
        self.metrics_calculator = MetricsCalculator()

    def run(self, source_file: str, output_file: str) -> bool:
        """
        Execute complete ETL pipeline

        Args:
            source_file: Input CSV file path
            output_file: Output CSV filename

        Returns:
            True if pipeline completed successfully
        """
        logger.info("Starting ETL pipeline")

        # Extract
        data = self.extractor.extract_from_csv(source_file)
        if data is None:
            logger.error("Extraction failed")
            return False

        # Transform
        transformed_data = self.transformer.transform(data)
        if transformed_data is None:
            logger.error("Transformation failed")
            return False

        # Validate
        validated_data = self.validator.validate_and_clean(transformed_data)
        if validated_data is None:
            logger.error("Validation failed")
            return False

        # Load
        success = self.loader.save_to_csv(validated_data, output_file)
        if not success:
            logger.error("Loading failed")
            return False

        # Calculate metrics
        metrics = self.metrics_calculator.calculate(validated_data)
        if metrics:
            logger.info(f"Pipeline completed. Metrics: {metrics}")

        logger.info("ETL pipeline completed successfully")
        return True


def main():
    """Main execution function"""
    pipeline = ETLPipeline()
    success = pipeline.run(
        source_file="sales_data.csv",
        output_file="output.csv"
    )

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
