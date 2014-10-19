
class FormTransformer:
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
            value = request.params[param]
            try:
                value = int(value)
            except:
                try:
                    value = float(value)
                except:
                    pass
            args.append(value)
        return args

    def serialize(self, results):
        return results