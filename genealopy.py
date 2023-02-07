from typing import Union

class Individual: pass
class Family: pass

class Individual:
    
    # Initialisation
        
    def __init__ (
            self,
            firstname: str = None,
            lastname: str = None,
            birthdate: str = None,
            deathdate: str = None,
            familiesasfather: Union[Family, list] = None,
            familiesasmother: Union[Family, list] = None,
            familyaschild: Family = None
        ):
        self.firstname = firstname
        self.lastname_ = lastname
        self.birthdate = birthdate
        self.deathdate = deathdate
        if type(familiesasfather) == list:
            self.familiesasfather = familiesasfather
            for family in familiesasfather:
                family.set_father(self, ignore_recursion=True)
        elif type(familiesasfather) == Family:
            self.familiesasfather = [familiesasfather]
            familiesasfather.set_father(self,ignore_recursion=True)
        elif familiesasfather is None:
            self.familiesasfather = []
        else:
            raise Exception("'familiesasfather' must either be a Family, a list of Family or None (default).")
        if type(familiesasmother) == list:
            self.familiesasmother = familiesasmother
        elif type(familiesasmother) == Family:
            self.familiesasmother = [familiesasmother]
        elif familiesasmother is None:
            self.familiesasmother = []
        else:
            raise Exception("'familiesasmother' must either be a Family, a list of Family or None (default).")
        self.familyaschild = familyaschild
            
    # Setters        
    
    def set_firstname(self, firstname: str) -> None:
        self.firstname = firstname
    def set_lastname(self, lastname: str) -> None:
        self.lastname = lastname
    def set_birthdate(self, birthdate: str) -> None:
        self.birthdate = birthdate
    def set_deathdate(self, deathdate: str) -> None:
        self.deathdate = deathdate
    def set_familiesasfather(self, families: Union[Family, list]) -> None:
        if type(families) == list:
            self.familiesasfather = families
        elif type(families) == Family:
            self.familiesasfather = [families]
        for f in self.familiesasfather:
            f.set_father(self,ignore_recursion=True)
        else:
            raise Exception("'children' must either be a Family or a list of Family.")
    def add_familiesasfather(self, families: Union[Family, list], ignore_recursion = False) -> None:
        if type(families) == list:
            for f in families:
                self.familiesasfather.append(f)
                if not ignore_recursion:
                    f.set_father(self,ignore_recursion=True)
        elif type(families) == Family:
            self.familiesasfather.append(families)
            families.set_father(self,ignore_recursion=True)
        else:
            raise Exception("'children' must either be a Family or a list of Family.")
    
    def get_firstname(self) -> str:
        return self.firstname
    def get_lastname(self) -> str:
        return self.lastname
    def get_birthdate(self) -> str:
        return self.birthdate
    def get_deathdate(self) -> str:
        return self.deatdate
    def get_familiesasfather(self) -> list:
        return self.familiesasfather
    def get_familiesasmother(self) -> list:
        return self.familiesasmother
    def get_familyaschild(self) -> Family:
        return self.familyaschild

class Family:
    
    # Initialisation
    
    def __init__(
            self,
            father: Individual = None,
            mother: Individual = None,
            children: Union[Individual, list] = []
        ):
        self.father = father
        self.mother = mother
        if type(children) is list:
            self.children = children
        elif type(children) is Individual:
            self.children = [children]
        elif children is None:
            self.children = []
        else:
            raise Exception("'children' must either be an Individual, a list of Individual or None (default).") 
        
    # Setters
    
    def set_father(self, father: Individual, ignore_recursion=False):
        self.father = father
        if not ignore_recursion:
            father.add_familiesasfather(self, ignore_recursion=True)
    def set_mother(self, mother):
        self.mother = mother
    def set_children(self, children: Union[Individual, list]):
        if type(children) is list:
            self.children = children
        elif type(children) is Individual:
            self.children = [children]
        else:
            raise Exception(f"'children' must either be an Individual or a list of Individual.")
    def add_children(self, children: Union[Individual, list]):
        if type(children) is list:
            for child in children:
                self.children.append(child)
        elif type(children) is Individual:
            self.children.append(children)
        else:
            raise Exception(f"'children' must either be an Individual or a list of Individual.")
        
    # Getters
    
    def get_father(self) -> Individual:
        return self.father
    def get_mother(self) -> Individual:
        return self.mother
    def get_children(self) -> list:
        return self.children