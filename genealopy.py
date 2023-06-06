import pandas as pd
import datetime
import random
import hashlib
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import unidecode
from typing import Union

class Genealogy:

    def __init__(self):        
        self.__individuals__ = pd.DataFrame({
            "id": [],
            "first_name": [],
            "last_name": [],
            "sex": [],
            "birth_date": [],
            "death_date": [],
            "families_as_husband_indices": [],
            "families_as_wife_indices": [],
            "family_as_child_index": [],
        })
        self.__families__ = pd.DataFrame({
            "id": [],
            "husband_index": [],
            "wife_index": [],
            "children_indices": [],
            "marriage_date": [],
        })

    def generate_id(self) -> str:
        return hashlib.sha256(str(random.random()).encode()).hexdigest()[:8]

    def create_individual(self, first_name: str = None, last_name: str = None, sex: str = None, birth_date: datetime.date = None, death_date: datetime.date = None) -> str:
        """
        Creates a new individual.

        Parameters
        ----------
        first_name : str
            The first name of the individual.
        last_name : str
            The last name of the individual.
        sex : str
            The sex of the individual. Must be either 'M' or 'F'.
        birth_date : datetime.date
            The birth date of the individual.
        death_date : datetime.date
            The death date of the individual.

        Returns
        -------
        str
            The id of the newly created individual.
        """
        if first_name is not None and not isinstance(first_name, str):
            raise TypeError(f"'first_name' must be of type 'str', not '{type(first_name)}'.")
        if last_name is not None and not isinstance(last_name, str):
            raise TypeError(f"'last_name' must be of type 'str', not '{type(last_name)}'.")
        if sex is not None and sex != "M" and sex != "F":
            raise ValueError("'sex' must either be 'M' or 'F'.")
        if birth_date is not None and not isinstance(birth_date, datetime.date):
            raise TypeError(f"'birth_date' must be of type 'datetime.date', not '{type(birth_date)}'.")
        if death_date is not None and not isinstance(death_date, datetime.date):
            raise TypeError(f"'death_date' must be of type 'datetime.date', not '{type(death_date)}'.")
        id = self.generate_id()
        new_individual = pd.DataFrame({
            "id": [id],
            "first_name": [first_name],
            "last_name": [last_name],
            "sex": [sex],
            "birth_date": [birth_date],
            "death_date": [death_date],
            "families_as_husband_indices": [[]],
            "families_as_wife_indices": [[]],
            "family_as_child_index": [None],
        })
        self.__individuals__ = pd.concat([self.__individuals__, new_individual]).reset_index(drop=True)
        return id

    def create_family(self, husband_id: str = None, wife_id: str = None, children_ids: list = [], marriage_date: datetime.date = None) -> str:
        """
        
        """
        id = self.generate_id()
        if not isinstance(children_ids, list):
            children_ids = [children_ids]
        new_family = pd.DataFrame({
            "id": [id],
        "husband_index": [None],
        "wife_index": [None],
        "children_indices": [[]],
            "marriage_date": [marriage_date],
        })
        self.__families__ = pd.concat([self.__families__, new_family]).reset_index(drop=True)
        if husband_id is not None:
            self.add_individual_to_family(individual_id=husband_id, family_id=id, role="husband")
        if wife_id is not None:
            self.add_individual_to_family(individual_id=wife_id, family_id=id, role="wife")
        for child_id in children_ids:
            self.add_individual_to_family(individual_id=child_id, family_id=id, role="child")
        return id

    def add_individual_to_family(self, individual_id: str, family_id: str, role: str) -> None:
        """
        
        """
        individual_index = self.__individuals__.query("id == @individual_id").index[0]
        family_index = self.__families__.query("id == @family_id").index[0]


        if role == "husband":
            self.__families__.iloc[family_index]["husband_index"] = individual_id
            self.__individuals__.iloc[individual_index]["families_as_husband_indices"].append(family_id)
        elif role == "wife":
            self.__families__.iloc[family_index]["wife_index"] = individual_id
            self.__individuals__.iloc[individual_index]["families_as_wife_indices"].append(family_id)
        elif role == "child":
            self.__families__.iloc[family_index]["children_indices"].append(individual_id)
            self.__individuals__.iloc[individual_index]["family_as_child_index"] = family_id
        else:
            raise ValueError("Role must be either 'husband', 'wife' or 'child'.")

    def mermaid(self) -> str:
        
        result = ""
        
        result += "graph TD\n"
        
        for _, individual in self.__individuals__.iterrows():
            result += f'{individual["id"]}[{individual["first_name"]} {individual["last_name"]}]\n'
            
        for _, family in self.__families__.iterrows():
            result += f'{family["id"]}[ ]\n'
        
        for _, individual in self.__individuals__.iterrows():
            for family in individual["families_as_husband_indices"]:
                result += f'{individual["id"]} --> {family}\n'
            for family in individual["families_as_wife_indices"]:
                result += f'{individual["id"]} --> {family}\n'
                
        for _, family in self.__families__.iterrows():
            for child in family["children_indices"]:
                result += f'{family["id"]} --> {child}\n'
                
        return result

    def gedcom(self) -> str:
        result = ""
        result += "0 HEAD\n"
        result += "1 SOUR PAF\n"
        result += "2 NAME Personal Ancestral File\n"
        result += "2 VERS 5.0\n"
        result += "1 DATE 30 NOV 2000\n"
        result += "1 GEDC\n"
        result += "2 VERS 5.5\n"
        result += "2 FORM LINEAGE-LINKED\n"
        result += "1 CHAR ANSEL\n"
        result += "1 SUBM @U1@\n"
        
        for _, individual_obj in self.__individuals__.iterrows():
            result += f"0 @{individual_obj['id']}@ INDI\n"
            result += f"1 NAME {individual_obj['first_name']} /{individual_obj['last_name']}/\n"
            result += f"1 SEX {individual_obj['sex']}\n"
            if individual_obj["birth_date"] is not None:
                result += f"1 BIRT\n"
                result += f"2 DATE {individual_obj['birth_date'].isoformat()}\n"
            if individual_obj["death_date"] is not None:
                result += f"1 DEAT\n"
                result += f"2 DATE {individual_obj['death_date'].isoformat()}\n"
            for family_id in individual_obj["families_as_husband_indices"]:
                result += f"1 FAMS @{family_id}@\n"
            for family_id in individual_obj["families_as_wife_indices"]:
                result += f"1 FAMS @{family_id}@\n"
            if individual_obj["family_as_child_index"] is not None:
                family_id = individual_obj["family_as_child_index"]
                result += f"1 FAMC @{family_id}@\n"
        
        for _, family_obj in self.__families__.iterrows():
            result += f"0 @{family_obj['id']}@ FAM\n"
            if family_obj["marriage_date"] is not None:
                result += f"1 MARR\n"
                result += f"2 DATE {family_obj['marriage_date'].isoformat()}\n"
            if family_obj["husband_index"] is not None:
                individual_id = family_obj["husband_index"]
                result += f"1 HUSB @{individual_id}@\n"
            if family_obj["wife_index"] is not None:
                individual_id = family_obj["wife_index"]
                result += f"1 WIFE @{individual_id}@\n"
            for child in family_obj["children_indices"]:
                result += f"1 CHIL @{child}@\n"
        
        result += "0 @U1@ SUBM\n"
        result += "1 NAME Submitter\n"
        result += "0 TRLR"
        
        return result