"""Module that contains custom exception for when a cinema item is not in the watchlist when it's expected to be"""
class WatchListItemNotFoundError(Exception):
    pass