FILE_PREFIX = '__file__'


class FormTransformer(object):
    """
    Deserializes requests constructed by HTML forms, and serializes results to
    JSON.
    """

    def parse(self, request, service_params):
        """
        Parses the parameter values in the request to a list with the order of
        the given service_params.
        """
        # TODO(orlade): Read types from IDL.
        args = []
        for param in service_params:
            # Check files first. Empty if no files uploaded.
            file_param = FILE_PREFIX + param
            if file_param in request.files.keys():
                value = self.parse_value(request.files.get(file_param).file.read())
                args.append(value)

            elif param in request.params:
                value = self.parse_value(request.params[param])
                args.append(value)

        return args

    def parse_value(self, value):
        """
        Converts the given string to the appropriate Python type.
        """
        try:
            return int(value)
        except:
            try:
                return float(value)
            except:
                pass
        return value

    def serialize(self, results):
        """
        Converts the given Python object into a string for the client.
        """
        return results