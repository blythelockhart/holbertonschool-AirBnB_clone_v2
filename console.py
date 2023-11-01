#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""
    # determines prompt for interactive/non-interactive modes
    if sys.__stdin__.isatty():
        prompt = '(hbnb) '
    else:
        prompt = ''
    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        arg = args.split()
        class_name = arg[0]
        attr_dict = {}

        if not class_name:
            print("** class name missing **")
            return
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        for value in arg:
            if '=' in value:
                key, val = value.split('=')
                val = val.strip('"').replace('\\"', '"').replace('_', ' ')

                if '.' in val:
                    try:
                        val = float(val)
                    except ValueError:
                        continue
                else:
                    try:
                        val = int(val)
                    except ValueError:
                        continue
                attr_dict[key] = val
        new_instance = HBNBCommand.classes[class_name](**attr_dict)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        arg = args.split()
        class_name = arg[0]
        class_id = arg[1]

        if not class_name:
            print("** class name missing **")
            return
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not class_id:
            print("** instance id missing **")
            return
        key = class_name + "." + class_id

        try:
            print(storage.all()[key])
            return
        except KeyError:
            print("** no instance found **")
            return

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        arg = args.split()
        class_name = arg[0]
        class_id = arg[1]

        if not class_name:
            print("** class name missing **")
            return
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not class_id:
            print("** instance id missing **")
            return
        key = class_name + "." + class_id

        try:
            del storage.all()[key]
            storage.save()
            return
        except KeyError:
            print("** no instance found **")
            return

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            arg = args.split()
            if arg[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for key, val in storage.all().items():
                if arg[0] in val.__class__.__name__:
                    print_list.append(val.__str__())
        else:
            for key, val in storage.all().items():
                print_list.append(val.__str__())
        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0

        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ Help information for the count command """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        arg = args.split()
        class_name = arg[0]
        class_id = arg[1]
        att_name = arg[2]
        att_val = arg[3]

        if not class_name:
            print("** class name missing **")
            return
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not class_id:
            print("** instance id missing **")
            return
        key = class_name + "." + class_id

        if key not in storage.all():
            print("** no instance found **")
            return
        if not att_name:
            print("** attribute name missing **")
            return
        if not att_val:
            print("** value missing **")
            return
        if att_name in HBNBCommand.types:
            att_val = HBNBCommand.types[att_name](att_val)
        setattr(storage.all()[key], att_name, att_val)
        storage.all()[key].save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
