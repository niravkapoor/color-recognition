from django.http import HttpResponse

class Util:
    def _404Code(self):
        response = HttpResponse("Not Found")
        response.status_code = 404
        return response

    def constructResponse(self, statusCode):
        switcher = {
            404: self._404Code
        }
        func = switcher.get(statusCode)
        print(func)
        return func()
    
    