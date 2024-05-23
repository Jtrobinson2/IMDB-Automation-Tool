"""Module that contains custom exception for when a cinema list item is already 
in a specified users list and they are attempting to add the same item again
"""
class DuplicateListItemException(Exception):
    pass