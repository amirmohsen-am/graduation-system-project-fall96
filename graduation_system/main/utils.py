def user_is_student(user):
    return hasattr(user, 'student')


def student_check(user):
    return user_is_student(user)


def staff_check(user):
    return user.is_staff
