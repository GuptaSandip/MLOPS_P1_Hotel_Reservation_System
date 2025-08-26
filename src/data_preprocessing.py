import os 
import pandas as pd
import numpy as np 
from src.logger import get_logger
from src.custom_exception import CustomException 
from config.paths_config import * 
from utils.common_funcation import read_yaml,load_data
from sklearn.ensemble import RandomForestClassifier 
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:

    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        # creating processed dir in artifacts 
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    
    def preprocessed_data(self,df):
        try:
            logger.info("Starting data processing steps")

            logger.info("Dropping the cloumns")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'] , inplace=True)

            df.drop_duplicates(inplace=True)

            # split cat and num

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config['data_processing']['numerical_columns']

            # Lebel Encoding 
            logger.info("Applying Label Encoding")

            label_encoder = LabelEncoder()

            mappings={}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])

                mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}

            logger.info("Label Mapping are:")
            for col,mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            # Skweness handling 

            logger.info("Doing skewness Handling")
            #data_processing
            skew_thresold = self.config["data_processing"]["skewness_thresold"]
            skewness = df[num_cols].apply(lambda x : x.skew())

            # apply log transformation 

            for column in skewness[skewness > skew_thresold].index:
                df[column] = np.log1p(df[column])
            return df 
        
        except Exception as e:
            logger.error(f"Error during preprocess step {e}")
            raise CustomException("Error while preprocess data",e)
        
    
    # Handle Imbalance Data 

    def balance_data(self,df):
        try:
            logger.info("Handling Imbalance Data")
            X = df.drop(columns = 'booking_status')
            y = df['booking_status']

            smote = SMOTE(random_state=42)

            X_resample , y_resample = smote.fit_resample(X,y)
            
            balanced_df = pd.DataFrame(X_resample , columns=X.columns)
            balanced_df["booking_status"] = y_resample 

            logger.info("Data Imbalance Hanlde Succesfully")
            return balanced_df
        except Exception as e:
            logger.error(f"Error during balancing the data  {e}")
            raise CustomException("Error while Balanacing data",e)
        
    
    # feature selection 
    def feature_selection(self,df):
        try:
            logger.info("Starting Feature Selection Step.")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            model =  RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame({
                'feature':X.columns,
                'importance':feature_importance
            })

            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            num_features_to_select = self.config["data_processing"]["no_of_features"]

            top_10_features = top_features_importance_df["feature"].head(num_features_to_select).values

            logger.info(f"features selected : {top_10_features}")

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature Selection Completed Succesfully")

            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during Feature Selection  {e}")
            raise CustomException("Error while Feature selection",e)    
        
        # saving data into csv 
    def save_data(self,df,file_path):
        try:
            logger.info("Saving our Data in processed folder")

            df.to_csv(file_path, index = False)

            logger.info(f"Data Saved Succesfully to {file_path}")

        except Exception as e:
            logger.error(f"Error during saving data  {e}")
            raise CustomException("Error while saving data",e)    
        
    def process(self):
        try:
            logger.info("Loading the Data from RAW Dir")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocessed_data(train_df)
            test_df = self.preprocessed_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df,processed_train_data_path)
            self.save_data(test_df,processed_test_data_path)

            logger.info("Data Processing Completed Succesfully")

        except Exception as e:
            logger.error(f"Error during preprocessing pipeline {e}")
            raise CustomException("Error while data preprocessing pipeline",e)         



if __name__ == "__main__":
    processor = DataProcessor(train_file_path,test_file_path,processed_dir,config_path)

    processor.process()

