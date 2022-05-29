import os
from glob import glob
from PIL import Image


class LogImgGenerator: 

    data_types = {
        "buffer_of": [], 
        "bwget": [], 
        "normal": [], 
        "traversal": []
    }

    #Function that index all files from one path.
    @staticmethod
    def get_attack_type_from_all_files_from_given_directory( list_files ):
        '''
        Función para indexar los arcchivos
            - Cargamos en tres variables la carpeta origen, las subcarpetas intermedias y los archivos.
            - Recorremos los subdirectorios desde el origen.
            - Leemos los archivos de uno en uno e indexamos el contenido.
        ''' 
        for root, subdirectories, files in os.walk(list_files):
            for subdirectory in subdirectories:
                print(os.path.join(root, subdirectory))
            for file in files:
                LogImgGenerator.read_one_file(os.path.join(root, file) )

    #Funcion que nos permite sacar el tipo del fichero
    @staticmethod 
    def type_selection( file ): 
        if( "buffer" in file ): 
            return "buffer_of"
        if( "bwget" in file ): 
            return "bwget"
        if ("traversal" in file ): 
            return "traversal"
        if( "normal" in file ): 
            return "normal" 
        return None

    
    #Function that append all info from the files indexed 
    @staticmethod
    def read_one_file( file): 
        #print("Comenzamos")    
        # Abrimos el archivo para leer las líneas
        fl =  LogImgGenerator.type_selection( file ) 
        with open(file) as infile:
            print("Leyendo el fichero:\t" + file)
            contador = 0
            for linea in infile:
                #Para cada línea creamos una imagen y la guardamos
                #Recogemos todas las líneas y les asociamos un dato que será el que se usará para la validación [y]
                LogImgGenerator.data_types[fl].append( ImgTooler.load_image_data( linea )) 
                #print( "[" + linea + ",\n "+  sender.send( linea) + " ]") #ENVIAMOS LA IMAGEN AL SERVIDOR Y MOSTRAMOS EL RESULTADO POR PANTALLA
            infile.close()
        return Log.LogImgGenerator.data_types #Devolvemos el diccionario con los datos    
        


    