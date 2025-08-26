import os 
import pandas as pd 
import joblib 
from sklearn.model_selection import RandomizedSearchCV 
import lightgbm as lgb 
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from src.logger import get_logger 
from src.custom_exception import CustomException 
from config.paths_config import * 
from config.model_params import * 
from utils.common_funcation import read_yaml,load_data
from scipy.stats import randint 

import mlflow 
import mlflow.sklearn

logger = get_logger(__name__)


class ModelTraining:

    def __init__(self,train_path,test_path,model_output_path):
        self.train_path = train_path 
        self.test_path = test_path 
        self.model_output_path = model_output_path 

        self.params_dist = LIGHTGM_PARMS 
        self.random_search_params = RANDOM_SEARCH_PARMS 

    # Load and split data method 
    def load_and_split_data(self):
        try:
            logger.info(f"Loading training data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading testing data from {self.test_path}")
            test_df = load_data(self.test_path)

            #Splitting data 
            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']

            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']

            logger.info("Data splitted successfully for model training")

            return X_train,y_train,X_test,y_test
        
        except Exception as e:
            logger.error(f"Error while loading data {e}")
            raise CustomException("Failed to load data", e)
        
    def train_lgbm(self,X_train,y_train):
        try:
            logger.info("Intializing the model")

            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Starting Hyperparameter tunning")

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs= self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                random_state= self.random_search_params["random_state"],
                scoring = self.random_search_params["scoring"]
            )

            logger.info("Starting model training with hyperparameter")

            random_search.fit(X_train,y_train)

            logger.info("Hyper-parameter tunning completed")

            best_params = random_search.best_params_

            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best Parameters are : {best_params}")

            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error Occure while building Model {e}")
            raise CustomException("Model Training Failed",e)
        

    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Model Evaluation")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"Accuracy Score : {accuracy}")
            logger.info(f"precision Score : {precision}")
            logger.info(f"recall Score : {recall}")
            logger.info(f"f1 Score : {f1}")

            return {
                "accuracy" : accuracy,
                "precision" : precision,
                "recall" : recall,
                "f1" : f1
            }

        except Exception as e:
            logger.error(f"Error Occure while Evaluating Model {e}")
            raise CustomException("Model Evaluation Failed",e)
        

## Save the model
    def save_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok=True)
            logger.info("Saving the Model")
            joblib.dump(model,self.model_output_path)

            logger.info(f"Model saved to {self.model_output_path}")

        except Exception as e:
            logger.error(f"Error Occure while saving Model {e}")
            raise CustomException("Failed to save model",e)   

    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting Model Training pipeline")

                logger.info("Starting MLflow Experimentation")

                logger.info("Logging Training and Testing Dataset to MLflow")

                mlflow.log_artifact(self.train_path, artifact_path="datasets")

                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                # setp1
                X_train,y_train,X_test,y_test = self.load_and_split_data()

                # step 2
                best_lgbm_model = self.train_lgbm(X_train,y_train) 

                # step 3
                metrics = self.evaluate_model(best_lgbm_model, X_test,y_test)

                # step 4
                self.save_model(best_lgbm_model)

                logger.info("Logging the model into mlflow")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging params and metrics into mlflow")
                mlflow.log_params(best_lgbm_model.get_params())

                mlflow.log_metrics(metrics)

                logger.info("Model Training Successfully Completed")

        except Exception as e:
            logger.error(f"Error Occure while training model pipeline {e}")
            raise CustomException("Failed to train model pipeline",e)   
        

if __name__ == "__main__":
    trainer = ModelTraining(processed_train_data_path,processed_test_data_path,model_output_path)
    trainer.run()





        
            