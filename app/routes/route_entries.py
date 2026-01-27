from . import (
    auth_route,
    syllabus_route,
    batch_route,
    student_route,
    user_route,
    mentor_route,
    guest_route,
    ws_chat,
)


"""
add your protected route here
"""
PROTECTED_ROUTES = [
    user_route.router,
    syllabus_route.router,
    batch_route.router,
    student_route.router,
    ws_chat.router,
    mentor_route.router,
]


"""
add your public route here
"""
PUBLIC_ROUTES = [
    auth_route.router,
    guest_route.router,
]
