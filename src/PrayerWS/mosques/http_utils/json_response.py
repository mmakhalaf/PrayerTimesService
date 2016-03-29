from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


##### ###########################
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
    ### ###############################
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        return super(JSONResponse, self).__init__(content, **kwargs)

    def CreateErrorResponse(reason):
    ### ############################
        """Return a standard error response"""
        data = {"result": False, "reason": reason};
        return JSONResponse(data);

    def CreateDataResponse(data):
    ### #########################
        cdata = {"result": True, "data": data};
        return JSONResponse(cdata);