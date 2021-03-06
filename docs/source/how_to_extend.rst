How to Extend the Library
==========================

The GameBench API was originally written to use the Requests HTTP Library.  However, this functionality can be extended to work with other libraries that need to be used.  The following is an example of extending the Adapter for use with URLLib.

The abstract base class ‘Adapter’:

.. code-block:: python
   :caption: adapter.py
   :linenos:

   class Adapter(ABC):
        """ Abstract adapter for external HTTP request services."""

        def __init__(self):
            """ Abstract init that creates an empty service object."""

            self._http_library = None

        @abstractmethod
        def request(self):
            """ Abstract method to make a request."""

            pass

This class can simply be inherited to a new class for whichever library will be used.  The _http_library instance variable should be used in the new class to hold a reference to the imported library.  The request method needs to be implemented in all concrete classes and will be used to send the request.  Here is the implemented class for using URLLib:

.. code-block:: python
   :caption: adapter.py
   :linenos:

    class URLLibAdapter(Adapter):

        def __init__(self, **request_attributes):
            super().__init__()
            import urllib.request  # Import the library needed
            self._http_library = urllib.request  # Assign library to the _http_library variable
            self.method = request_attributes['method']
            self.url = request_attributes['url']
            self.headers = request_attributes['attributes']['headers']

        def request(self):
            return self._http_library.Request(self.url, headers=self.headers, method=self.method)

For this class we set up our local import of the urllib.request library.  We assign that library to the instance variable to be used in the request method.  The request_attributes argument will be the dictionary returned from the request retriever.  This will include the needed elements for a request.  Each of the needed needed elements is assigned to a variable.  The request method then sends a request to the library using this information and returns the result.

Now that we have the new library set up to send requests, we just have to update our response retrievers to use this library.  Here is what the Authentication Retriever currently looks like:

.. code-block:: python
   :caption: response_retriever.py
   :linenos:
   :emphasize-lines: 12

    class AuthResponseRetriever(AbstractRetriever):
        """ Facade for getting Auth token from the Request.

            :param request_parameters: Dictionary containing information needed for
                an authentication request.  Example:
                {'username': 'John@gmail.com', 'password': '1234'}
        """

        def __init__(self, **request_parameters):
            super().__init__(**request_parameters)
            self.request = self.director.get_auth_request(**self.request_parameters)
            self.adapter = RequestsAdapter(**self.request)
            self.response = self.adapter.request()

        def get_response_json(self):
            """ Return the JSON of the response object.

                :return: The JSON data for a response.
            """

            return super().get_response_json()

This is using the RequestsAdapter to send requests.  We can just update the adapter variable to use the URLLibAdapter to use the new library.

This is all that needs to be done to add in the library of your choosing. We'd love to refactor this class and allow
it to be user configurable.
