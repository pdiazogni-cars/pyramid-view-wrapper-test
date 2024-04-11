from pyramid.view import view_config
from pyramid.response import Response


class MyViewMapper:
    def __init__(self, **kw):
        self.kw = kw

    def __call__(self, view):
        # This attr is the View method that should be called from the matched routing
        # It could be either 'home1' or 'home2'
        method = self.kw['attr']

        def wrapper(context, request):
            # Creates MyView instance
            inst = view(context, request)

            # Calls the corresponding method
            response = getattr(inst, method)()

            # Enhance the response and resturn it
            result = {
                'request': {
                    'params': dict(request.params),
                },
                'response': response,
            }
            return result
        return wrapper


class MyView:
    __view_mapper__ = MyViewMapper

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(route_name='home1', renderer='json')
    def home1(self):
        return {'url': 'home1', 'project': 'pyramid_view_wrapper_test'}

    @view_config(route_name='home2', renderer='json')
    def home2(self):
        return {'url': 'home2', 'project': 'pyramid_view_wrapper_test'}


#class MyResponse(Response):
#    def __new__(cls, request):
#        return super().__new__(cls)


def includeme(config):
    pass
    #config.set_response_factory(lambda request: MyResponse(request))
