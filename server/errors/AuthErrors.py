class PassMathError(Exception):
    '''
    Passwords don't match
    '''

class PassNotCorrectError(Exception):
    '''
    Password not corrent 
    '''

class UserNotFoundError(Exception):
    '''
    User not found
    '''

class UserExistError(Exception):
    '''
    User is exist
    '''

class AuthenticationError(Exception):
    '''
    Not Authentication
    '''