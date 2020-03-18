# Import relevant modules from the directory (for external use and testing).
if __name__ is not None and "." in __name__:
    from .grade_sheet import Category
    from .grade_sheet import Grade
    from .grade_sheet import GradeSheet
    from .grade_sheet import GradeSheetGeneric
    from .parse_grade_sheet import ParseGradeSheet
else:
    from grade_sheet import Category
    from grade_sheet import Grade
    from grade_sheet import GradeSheet
    from grade_sheet import GradeSheetGeneric
    from parse_grade_sheet import ParseGradeSheet