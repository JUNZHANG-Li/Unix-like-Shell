def unsafe(execution):
    """
    <Decorator>
    -------

    Purpose
    -------
    To implement unsafe applications

    unsafe applications: allows the execution of shell
    ignoring any exceptions raised by the unsafe applications

    Functionality
    -------------
    Take in a class method as argument and returns
    an unsafe version of the function
    """

    def unsafe_execution(self):
        try:
            return execution(self)
        except Exception as e:
            print(e)
            return ""

    return unsafe_execution
