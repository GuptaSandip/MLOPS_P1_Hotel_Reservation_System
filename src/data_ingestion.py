# C:\Users\sandip\Downloads\totemic-gravity-463311-h0-992cfc0cf87a.json --> kEY 

import os 
import pandas  as pd 
from google.cloud import storage 
from sklearn.model_selection import train_test_split 
from src.logger import get_logger
from src.custom_exception import CustomException 
from config.paths_config import *
from utils.common_funcation import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name  = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        # artifacts\raw\data 
        os.makedirs(raw_dir,exist_ok=True)
        
        logger.info(f"Data Ingestion started with {self.bucket_name} and file name is {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client() 
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(raw_file_path)

            logger.info(f"Raw file is succesfully downloaded to {raw_file_path}")
        
        except Exception as e:
            logger.error("Error while downloading the csv file")
            raise CustomException("Failed to download the csv file",e)
        
    def split_data(self):
        try:
            logger.info("Starting the splitting process")

            data = pd.read_csv(raw_file_path)

            train_data, test_data = train_test_split(data, test_size= 1 - self.train_test_ratio, random_state=42)

            train_data.to_csv(train_file_path)
            test_data.to_csv(test_file_path)

            logger.info(f"Train Data saved to {train_file_path}")
            logger.info(f"Test Data saved to {test_file_path}")
    
        except Exception as e:
            logger.error("Error while splitting data")
            raise CustomException("Failed to split data into training and test set",e)
        
    
    # run method --> combining multiple step in method 
    def run(self):
        try:
            logger.info("Strating data ingestion process")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data Ingestion completed successfully")

        except CustomException as ce:
            logger.error(f"CustomException : {str(ce)}")

        finally:
            logger.info("Data Ingestion Completed")


if __name__ == "__main__":
    # object name 

    data_ingestion = DataIngestion(read_yaml(config_path)) # passing config path
    data_ingestion.run()