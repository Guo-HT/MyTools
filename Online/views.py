from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect


# Create your views here.
def index(request):
    return render(request, "online/index.html")


def epq_test(request):
    e = request.GET.get("E")
    n = request.GET.get("N")
    p = request.GET.get("P")
    l = request.GET.get("L")
    total = request.GET.get("total")
    print(e + "\t" + n + "\t" + p + "\t" + l + "\t" + total)
    with open("./epq_result.tsv", 'a') as f:
        f.write(e + "\t" + n + "\t" + p + "\t" + l + "\t" + total + "\n" )
    return JsonResponse({"code": 200, "msg": "ok"}, safe=False)
    
