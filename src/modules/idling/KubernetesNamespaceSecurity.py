import os, json, sys
from modules.common.Logging import ErrorManager
from modules.idling.KubernetesConfig import KubernetesConfig
from modules.ResponseModel.ResponseModel import ResponseModel

class KubernetesNamespaceSecurity():
    def __init__(self):
        self.__system_namespaces = [
            "kube-node-lease",
            "kube-public",
            "kube-system",
            "local-path-storage"
            ]
        
    def check_namespace_list(self,value):
        """Check if the value given contains kube-system namespace.

        Args:
            value (list,str,dict): The data that we need to 
            check if namespace kube system appear.

        Returns:
            _type_: _description_
        """
        if isinstance(value,list):
            return [i for i in value if i not in self.__system_namespaces]
        elif isinstance(value,str):
            return value if value not in self.__system_namespaces else None
        elif isinstance(value,dict):
            for namespace in self.__system_namespaces:
                return self.search_dict_keyword(value,namespace)
            
    def search_dict_keyword(self,data, keyword):
        """
        Recursively searches for a keyword within a nested dictionary or list.

        Args:
            data (dict or list): The dictionary or list to search.
            keyword (str): The keyword to search for.

        Returns:
            list: A list of key-value pairs that contain the keyword.
        """
        result = []
        self.__origin_data = data
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    result.extend(self.search_dict_keyword(value, keyword))
                elif isinstance(value, str) and keyword in value:
                    return value
                    #result.append((key, value))

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    result.extend(self.search_dict_keyword(item, keyword))
        
        return result


