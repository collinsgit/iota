# Import relevant modules from the directory (for external use and testing).
if __name__ is not None and "." in __name__:
    from .iota import Val
else:
    from iota import Val
