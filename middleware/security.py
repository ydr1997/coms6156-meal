unsecure_path = {
    '/health': ['GET'],
    '/': ['GET'],
    '/favicon.ico': ['GET'],
    '/login': ['GET']           # TODO: link auth.html with /login
}


def check_security(request):
    path = request.path
    method = request.method
    print("[security] requested path: ", path)

    # TODO: change uToken (which is from Google) to userId (assigned from our DB) to pass from request
    if path in unsecure_path and method in unsecure_path[path]:
        return True

    return False
