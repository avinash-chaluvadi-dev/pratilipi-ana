""" [Custom Exceptions for Topic classifier]

This module holds all the custom exception classes required for 
TOPIC_CLASSIFIER package

This file can also be imported as a module and contains the following
classes:

    * TopicClassifierBaseException - Base custom exception class for topic_classifier
    * TopicClassifierBaseWarning   - Base custom exception class for topic_classifier
    * ListStringValueException     - Custom Exception class which raises exception if 
                                     type of object is neither list nor string
    * StringValueWarning           - Custom Warning class which raise warning if any 
                                     of the input is an string
"""

import warnings


class TopicClassifierBaseException(Exception):

    """
    This class is the Base custom exception class for topic_classifier

    Methods
    -------
    __init__()
        Initializes the state of object with the input keyword arguments

    __str__()
        Returns the f string when object of this class is printed

    """

    def __init__(self, **kwargs):

        """
        Constructor of TopicClassifierBaseException class to initialize the state of object

        Parameters
        ----------
            :param **kwargs (dict): exception arguments dictionary
        """

        ## Initializes the object state using input keyword arguments
        if kwargs:
            self.error_message = kwargs.get("error_message")
            self.value = kwargs.get("value")
        else:
            self.error_message = None
            self.value = None

    def __str__(self):

        """
        Dunder/Magic method which is used to represent the class objects as a string
        in other words this method makes iteasy to read and outputs all the
        members of the class

        Returns
        -------
            :exception (str): Formatted exception
        """

        ## Returns the string if an exception of type TopicClassifierBaseException is raised
        if self.error_message:
            return f"TopicClassifierBaseException, {self.error_message}"
        else:
            return f"TopicClassifierBaseException raised an Exception"


class TopicClassifierBaseWarning(UserWarning):

    """
    This class is the Base custom warning class for topic_classifier

    Methods
    -------
    __init__()
        Initializes the state of object with the warning_message

    __str__()
        Returns the f string when object of this class is printed

    """

    def __init__(self, warning_message):

        """
        Constructor of TopicClassifierBaseWarning class to initialize the state of object

        Parameters
        ----------
            :param warning_message (str): message which is to be raised as a warning
        """

        ## Initializes the object state using input keyword arguments
        self.warning_message = warning_message

    def __str__(self):

        """
        Dunder/Magic method which is used to represent the class objects as a string
        in other words this method makes iteasy to read and outputs all the
        members of the class

        Returns
        -------
            :warning_string (str): Formatted warning_message
        """

        ## Returns the string if a warning of type TopicClassifierBaseWarning is raised
        if self.message:
            return f"TopicClassifierBaseWarning, {self.warning_message}"
        else:
            return f"TopicClassifierBaseWarning raised a warning"


class ListStringValueException(TopicClassifierBaseException):

    """
    This class inherits from TopicClassifierBaseException class and raises
    an exception if type of object is neither list nor string

    Methods
    -------
    __init__()
        Initializes the state of object with the input keyword arguments

    __str__()
        Returns the f string when object of this class is printed

    """

    def __init__(self, **kwargs):

        """
        Constructor of ListStringValueException class to initialize the state of object

        Parameters
        ----------
            :param **kwargs (dict): exception arguments dictionary
        """

        ## Calls the parent class __init__ method to initialize the object state
        super().__init__(**kwargs)

    def __str__(self):

        """
        Dunder/Magic method which is used to represent the class objects as a string
        in other words this method makes iteasy to read and outputs all the
        members of the class

        Returns
        -------
            :exception (str): Formatted exception
        """

        ## Returns the string if an exception of type ListStringValueException is raised
        if self.error_message:
            return f"ListStringValueException, {self.error_message}"
        else:
            return f"{self.value} is invalid input, topic_classifier() function can only accept list and string as its values"


class StringValueWarning(TopicClassifierBaseWarning):

    """
    This class inherits from TopicClassifierBaseWarning class and raises
    a warning if any string is empty or doesn't contain any words/message in other words an empty
    string with zero or more spaces

    Methods
    -------
    __init__()
        Initializes the state of object with the input keyword arguments

    __str__()
        Returns the f string when object of this class is printed

    """

    def __init__(self, warning_message=None):
        """
        Constructor of StringValueWarning class to initialize the state of object

        Parameters
        ----------
            :param warning_message (str): message which is to be raised as a warning
        """

        ## Calls the parent class __init__ method to initialize the object state
        super().__init__(warning_message=warning_message)

    def __str__(self):

        """
        Dunder/Magic method which is used to represent the class objects as a string
        in other words this method makes iteasy to read and outputs all the
        members of the class

        Returns
        -------
            :warning (str): Formatted warning
        """

        if self.warning_message:
            return f"StringValueWarning, {self.warning_message}"
        else:
            return f"Classifier cannot encode, preprocess and predict for empty strings, so all the empty strings will be classified as [No Reason Given]'"
