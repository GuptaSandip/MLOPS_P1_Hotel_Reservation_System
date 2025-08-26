from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_funcation import read_yaml
from config.paths_config import * 


if __name__ == "__main__":
    # 1. Data Ingestion
    data_ingestion = DataIngestion(read_yaml(config_path)) # passing config path
    data_ingestion.run()

    # 2. Data Processing 
    processor = DataProcessor(train_file_path,test_file_path,processed_dir,config_path)
    processor.process()    

    # 3. Model Training 
    trainer = ModelTraining(processed_train_data_path,processed_test_data_path,model_output_path)
    trainer.run()
