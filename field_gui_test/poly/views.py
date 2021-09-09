from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .helper import Helper
from .models import Field

def index(request):
    #degree = polys.get_degree()
    #output = '\n'.join([str(q.degree) for q in degree])

    return render(request, 'poly/index.html')
    #return HttpResponse('adsasdkfjbsdhf')

def output(request):
    # input_degree = None
    # input_disc = None
    # input_cm = None
    r = ''
    
    input_degree = request.GET.get('degree')
    input_disc = request.GET.get('discriminant')
    input_cm = request.GET.get('cm')
    input_sig = request.GET.get('signature')
    transitive_group_id = request.GET.get('transitive_group_id')
    group_order_small_id = request.GET.get('group_order_small_id')

    if not input_degree and not input_disc and not input_cm and not input_sig and not transitive_group_id and not group_order_small_id:
        return render(request, 'poly/index.html')

    poly = Helper()
    
    ## signature check
    if input_sig: #!= '' and input_sig is not None:
        r,s = poly.format_signature(input_sig)
        if r < 0 or s < 0:
            return render(request, 'poly/index.html')

        if input_degree == '' or input_degree == None:
            input_degree = r+(2*s)
            input_degree = str(input_degree)

        elif r+(2*s) != int(input_degree):      
            return render(request, 'poly/index.html')
        elif ',' in input_degree:
            return render(request, 'poly/index.html')

    

    ## degree check
    if input_degree: #!= '' and input_degree is not None:
        if ',' not in input_degree:
            if int(input_degree) < 1:   
                return render(request, 'poly/index.html')
        else:
            degree_range = input_degree.split(',')
            if int(degree_range[0]) < 1 or int(degree_range[1]) < 1:
                return render(request, 'poly/index.html')


    # if input_degree != '' and input_disc == '':
    #     output_list = poly.degree_(input_degree)
    # elif input_degree == '' and input_disc != '':
    #     output_list = poly.disc_(input_disc)
    # elif input_degree != '' and input_disc != '':
    #     output_list = poly.degree_disc_(input_disc,input_degree)
    # else:
    #     output_list = poly.signature_(sig[0],sig[1])

    if transitive_group_id or group_order_small_id:
        if not input_degree:
            return render(request, 'poly/index.html')
        else:
            output_polys, output_discs = poly.galois_group_search(input_degree, transitive_group_id, group_order_small_id)
    else:
        output_polys, output_discs = poly.raw_query(input_degree,input_disc, input_cm,r)

    output_list = zip(output_polys[:10], output_discs[:10])

    #for polys,discs in output_list:
        #print(polys,discs)

    if group_order_small_id:
        group = group_order_small_id.split(',')
        group_order = group[0]
        small_group_id = group[1]
    
    input_list = ['degree: ' + str(input_degree),'discriminant: ' + str(input_disc), 'cm: '+ str(input_cm), 'real_embeddings: ' + str(r), 'transitive_group_id: ' + str(transitive_group_id)]
    
    if group_order_small_id:
        input_list.append('group order: ' + str(group_order))
        
        input_list.append('small group ID: ' + str(small_group_id))

    context = {'input_list': input_list, 'queryset': output_list }
    #print((polys[0]))
    #return HttpResponse(output)
    return render(request, 'poly/output.html',context)

