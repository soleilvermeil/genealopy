import genealopy as gp


family = gp.Family()

father = gp.Individual(firstname="Naruto", lastname="Uzumaki")
mother = gp.Individual(firstname="Hinata", lastname="Hyuga")
child1 = gp.Individual(firstname="Boruto", lastname="Uzumaki")
child2 = gp.Individual(firstname="Himawari", lastname="Uzumaki")
children = [child1, child2]

family.set_father(father)
family.set_mother(mother)
family.set_children(children)

print(f"The father of the family is {family.get_father().get_firstname()}")
print(f"The mother of the family is {family.get_mother().get_firstname()}")
print(f"The children of the family are {[child.get_firstname() for child in family.get_children()]}")

print(f"The children of {father.get_firstname()} are :")
for family in father.get_familiesasfather():
    for child in family.get_children():
        print(child.get_firstname())

print(f"The children of {mother.get_firstname()} are :")
for family in mother.get_familiesasmother():
    for child in family.get_children():
        print(child.get_firstname())

print(f"The father of {child1.get_firstname()} is {child1.get_familyaschild().get_father().get_firstname()}")
print(f"The mother of {child2.get_firstname()} is {child2.get_familyaschild().get_mother().get_firstname()}")