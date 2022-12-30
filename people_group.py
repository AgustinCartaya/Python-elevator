from person import Person 

# === Class that models a group of people from the class `person.py`. ===

# [For person.py class documentation, click here](./person.html) 
class PeopleGroup():
    def __init__(self, people_list=[]):
        #Initializes the list of 'person' objects.
        self.people = people_list

    def __iter__(self):
        #Iterator Override.
        return self.people.__iter__()

    def __len__(self):
        #Size of People list.
        return len(self.people) 

    def __str__(self):
        #Override of STR for proper representation.
        st = ""
        for p in self.people:
            st = st + str(p) + "\n"
        return st

    def join(self, new):
        #Function to add a new person to the list.
        self.people.extend(new.people)

    def get_weight(self):
        #Returns the sum of the weight of a people group.
        weight = 0
        for p in self.people:
            weight = weight + p.weight
        return weight

    def add_person(self, p):
        #Adds a person individually as it uses append rather than extend.
        self.people.append(p)

    def get_enter_floor(self, floor_nb):
        #Gets the floor where the elevator was taken, for each person in self.people.
        new_group = PeopleGroup([])
        for p in self.people:
            if p.enter_floor == floor_nb:
                new_group.add_person(p)
        return new_group

    def get_exit_floor(self, floor_nb):
        #Gets the target floor for each person in self.people
        new_group = PeopleGroup([])
        for p in self.people:
            # print("p: %d = floor: %d"% (p.exit_floor,floor_nb)) 
            if p.exit_floor == floor_nb:
                new_group.add_person(p)
        return new_group

    def remove_sub_group(self, sub_group):
        #Remove people by subgroups, in case more than one 'person' object, leaves the floor.
        lst = []
        for p in self.people:
            if p not in sub_group.people:
                lst.append(p)
        self.people = lst

    def get_last(self, nb_from=0):
        #return the last group remaining in the elevator.
        new_group = PeopleGroup([])
        new_group.people = self.people[nb_from:len(self.people)]
        return new_group

    def remove_all(self):
        #Remove all 'person' objects from the people group.
        self.people = []

    def get_nb(self):
        #Returns the size of self.people.
        return len(self.people)

# [Go back to main.py, click here](./main.html)
