"""
Data Pipeline for ACE Intelligence System
Team: Jujutsu Query
Project: Adaptive Enforcement Intelligence System

This module handles data loading, processing, and merging of MTA datasets
for the ACE Intelligence System project.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Union
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MTADataPipeline:
    """
    Data pipeline class for loading and merging MTA datasets
    """
    
    def __init__(self, data_directory: str = "data"):
        """
        Initialize the data pipeline
        
        Args:
            data_directory (str): Path to the directory containing MTA CSV files
        """
        self.data_directory = Path(data_directory)
        self.master_df = None
        
    def load_bus_speeds_data(self, pattern: str = "MTA_Bus_Speeds*.csv") -> pd.DataFrame:
        """
        Load MTA Bus Speeds CSV files
        
        Args:
            pattern (str): File pattern to match bus speeds files
            
        Returns:
            pd.DataFrame: Combined bus speeds data
        """
        logger.info(f"Loading bus speeds data with pattern: {pattern}")
        
        # Find all matching files
        files = list(self.data_directory.glob(pattern))
        
        if not files:
            logger.warning(f"No files found matching pattern: {pattern}")
            return pd.DataFrame()
        
        # Load and combine all CSV files
        dataframes = []
        for file_path in files:
            try:
                logger.info(f"Loading file: {file_path}")
                df = pd.read_csv(file_path)
                
                # Parse date columns - adjust column names as needed based on actual data
                date_columns = ['date', 'Date', 'DATE', 'timestamp', 'Timestamp']
                for col in date_columns:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        logger.info(f"Parsed date column: {col}")
                
                dataframes.append(df)
                
            except Exception as e:
                logger.error(f"Error loading file {file_path}: {e}")
                
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            logger.info(f"Successfully loaded {len(combined_df)} records from {len(files)} bus speeds files")
            return combined_df
        else:
            return pd.DataFrame()
    
    def load_ace_enforcement_data(self, pattern: str = "MTA_Bus_Automated_Camera_Enforcement*.csv") -> pd.DataFrame:
        """
        Load MTA Bus Automated Camera Enforcement CSV files
        
        Args:
            pattern (str): File pattern to match ACE enforcement files
            
        Returns:
            pd.DataFrame: Combined ACE enforcement data
        """
        logger.info(f"Loading ACE enforcement data with pattern: {pattern}")
        
        # Find all matching files
        files = list(self.data_directory.glob(pattern))
        
        if not files:
            logger.warning(f"No files found matching pattern: {pattern}")
            return pd.DataFrame()
        
        # Load and combine all CSV files
        dataframes = []
        for file_path in files:
            try:
                logger.info(f"Loading file: {file_path}")
                df = pd.read_csv(file_path)
                
                # Parse date columns - adjust column names as needed based on actual data
                date_columns = ['violation_date', 'date', 'Date', 'DATE', 'timestamp', 'Timestamp']
                for col in date_columns:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        logger.info(f"Parsed date column: {col}")
                
                dataframes.append(df)
                
            except Exception as e:
                logger.error(f"Error loading file {file_path}: {e}")
                
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            logger.info(f"Successfully loaded {len(combined_df)} records from {len(files)} ACE enforcement files")
            return combined_df
        else:
            return pd.DataFrame()
    
    def create_master_dataframe(self) -> Optional[pd.DataFrame]:
        """
        Create a master DataFrame by merging bus speeds and ACE enforcement data
        
        Returns:
            pd.DataFrame: Master DataFrame with merged data
        """
        logger.info("Creating master DataFrame...")
        
        # Load both datasets
        bus_speeds_df = self.load_bus_speeds_data()
        ace_enforcement_df = self.load_ace_enforcement_data()
        
        if bus_speeds_df.empty and ace_enforcement_df.empty:
            logger.error("No data loaded from either dataset")
            return None
        
        # TODO: Implement merging logic based on actual data structure
        # Common merge keys might include:
        # - Route/Bus Route ID
        # - Date/Time period
        # - Geographic location (borough, zone, coordinates)
        # - Direction/Stop information
        
        """
        Example merging strategies to implement:
        
        1. Route-based temporal merge:
           - Merge on route_id + date/time period
           - This allows analysis of enforcement impact on specific routes
        
        2. Geographic merge:
           - Merge on geographic zones/coordinates
           - Useful for spatial analysis of enforcement effectiveness
        
        3. Time-window merge:
           - Merge ACE violations with bus speeds in surrounding time windows
           - Helps analyze immediate and delayed effects of enforcement
        
        Sample merge code (to be customized based on actual column names):
        
        # Route and date-based merge
        if not bus_speeds_df.empty and not ace_enforcement_df.empty:
            # Ensure both dataframes have similar date columns
            # Group by route and date for aggregation if needed
            
            master_df = pd.merge(
                bus_speeds_df,
                ace_enforcement_df,
                left_on=['route_id', 'date'],
                right_on=['route_id', 'violation_date'],
                how='outer',
                suffixes=('_speed', '_enforcement')
            )
            
            # Add derived features
            master_df['enforcement_density'] = master_df.groupby(['route_id', 'date'])['violation_count'].transform('sum')
            master_df['avg_speed_improvement'] = master_df['speed_after'] - master_df['speed_before']
            
        """
        
        # For now, store both datasets separately in the master structure
        # This allows flexibility for different analysis approaches
        self.master_df = {
            'bus_speeds': bus_speeds_df,
            'ace_enforcement': ace_enforcement_df,
            'merge_status': 'separate_datasets'
        }
        
        logger.info("Master DataFrame structure created with separate datasets")
        logger.info(f"Bus speeds records: {len(bus_speeds_df)}")
        logger.info(f"ACE enforcement records: {len(ace_enforcement_df)}")
        
        return self.master_df
    
    def get_data_summary(self) -> Dict:
        """
        Get a summary of loaded data
        
        Returns:
            Dict: Summary statistics and information about the loaded data
        """
        if self.master_df is None:
            return {"status": "No data loaded"}
        
        summary = {
            "bus_speeds": {
                "records": len(self.master_df['bus_speeds']),
                "columns": list(self.master_df['bus_speeds'].columns) if not self.master_df['bus_speeds'].empty else [],
                "date_range": self._get_date_range(self.master_df['bus_speeds'])
            },
            "ace_enforcement": {
                "records": len(self.master_df['ace_enforcement']),
                "columns": list(self.master_df['ace_enforcement'].columns) if not self.master_df['ace_enforcement'].empty else [],
                "date_range": self._get_date_range(self.master_df['ace_enforcement'])
            },
            "merge_status": self.master_df.get('merge_status', 'unknown')
        }
        
        return summary
    
    def _get_date_range(self, df: pd.DataFrame) -> Dict:
        """
        Get the date range for a DataFrame
        
        Args:
            df (pd.DataFrame): DataFrame to analyze
            
        Returns:
            Dict: Date range information
        """
        if df.empty:
            return {"min_date": None, "max_date": None}
        
        # Look for date columns
        date_columns = df.select_dtypes(include=['datetime64']).columns
        
        if len(date_columns) == 0:
            return {"min_date": None, "max_date": None}
        
        # Use the first date column found
        date_col = date_columns[0]
        return {
            "min_date": df[date_col].min(),
            "max_date": df[date_col].max(),
            "date_column": date_col
        }


def main():
    """
    Main function to demonstrate the data pipeline usage
    """
    # Initialize the pipeline
    pipeline = MTADataPipeline()
    
    # Create master DataFrame
    master_data = pipeline.create_master_dataframe()
    
    # Get summary
    summary = pipeline.get_data_summary()
    print("Data Summary:")
    print("-" * 40)
    for dataset, info in summary.items():
        if isinstance(info, dict):
            print(f"{dataset.upper()}:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            print()


if __name__ == "__main__":
    main()