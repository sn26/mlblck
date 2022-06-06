

class DatasetPreprocessor: 

    preprocessor = None
  
    
    @staticmethod
    def set_preprocessor(preprocessor ): 
        DatasetPreprocessor.preprocessor = preprocessor

    #Le pasamos el dataset y tendrá que devolvernos el conjunto de valores X, Y que vamos a utilizar
    @staticmethod
    def preprocess_dataset(dataset ): 
        return DatasetPreprocessor.preprocessor.preprocess(dataset) 