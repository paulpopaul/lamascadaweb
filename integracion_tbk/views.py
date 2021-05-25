from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action

from django.contrib.auth.models import User

from core.models import Item, OrderItem, Order, Payment, Coupon, Used_coupon, Refund, UserProfile, Category,Order_buy, Token_tbk
# Create your views here.

import os
from datetime import datetime
import random
import tbk

CERTIFICATES_DIR = os.path.join(os.path.dirname(__file__), 'commerces')


def load_commerce_data(commerce_code):
    with open(os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + '.key'), 'r') as file:
        key_data = file.read()
    with open(os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + '.crt'), 'r') as file:
        cert_data = file.read()
    with open(os.path.join(CERTIFICATES_DIR, 'certificado-publico-transbank.crt'), 'r') as file:
        tbk_cert_data = file.read()

    return {
        'key_data': key_data,
        'cert_data': cert_data,
        'tbk_cert_data': tbk_cert_data
    }


# app = flask.Flask(__name__)
# app.secret_key = 'TBKSESSION'

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("tbk").setLevel(logging.DEBUG)
# logging.getLogger('suds.transport.http').setLevel(logging.DEBUG)
#HOST = os.getenv('HOST', 'http://127.0.0.1')
#PORT = os.getenv('PORT', '8000')
HOST = os.getenv('HOST', 'https://lamascada.cl')
BASE_URL = '{host}'.format(host=HOST)

#BASE_URL = '{host}:{port}'.format(host=HOST, port=PORT)



NORMAL_COMMERCE_CODE = "597036092076"

#NORMAL_COMMERCE_CODE = "597020000541"
ONECLICK_COMMERCE_CODE = "597020000593"


normal_commerce_data = load_commerce_data(NORMAL_COMMERCE_CODE)
normal_commerce = tbk.commerce.Commerce(
    commerce_code=NORMAL_COMMERCE_CODE,
    key_data=normal_commerce_data['key_data'],
    cert_data=normal_commerce_data['cert_data'],
    tbk_cert_data=normal_commerce_data['tbk_cert_data'],
    environment=tbk.environments.PRODUCTION)
webpay_service = tbk.services.WebpayService(normal_commerce)






oneclick_commerce_data = load_commerce_data(ONECLICK_COMMERCE_CODE)
oneclick_commerce = tbk.commerce.Commerce(
    commerce_code=ONECLICK_COMMERCE_CODE,
    key_data=oneclick_commerce_data['key_data'],
    cert_data=oneclick_commerce_data['cert_data'],
    tbk_cert_data=oneclick_commerce_data['tbk_cert_data'],
    environment=tbk.environments.PRODUCTION)


oneclick_service = tbk.services.OneClickPaymentService(oneclick_commerce)
oneclick_commerce_service = tbk.services.CommerceIntegrationService(oneclick_commerce)

#pagina de inicio de la transaccion de transbank
def init(request):
	template_name = 'integracion_tbk/base.html'

	return render(request,template_name)

#pagina de inicio para transaccion normal
def normal_index(request):
	template_name = 'integracion_tbk/index_normal.html'
	return render(request, template_name)

#metodo que inicia la conexion de la transaccion con webpay
def normal_init_transaction(request):
	order = Order.objects.get(user=request.user, ordered=False)

	template_name = 'integracion_tbk/init_normal.html'
	context = {}
	
	transaction = webpay_service.init_transaction(
	    amount=order.get_total(),
	    buy_order=order.id,
	    return_url=BASE_URL + "/integracion_tbk/return",
	    final_url=BASE_URL + "/integracion_tbk/final",
	    session_id=order.user
	)
	context['transaction'] = transaction
	# print context
	# return flask.render_template(template_name, transaction=transaction)
	return render(request, template_name, context)


#metodo que redirige segun la respuesta de webpay 
@csrf_exempt
def normal_return_from_webpay(request):
	token = request.POST.get('token_ws')
	transaction = webpay_service.get_transaction_result(token)
	transaction_detail = transaction['detailOutput'][0]
	webpay_service.acknowledge_transaction(token)

	if transaction_detail['responseCode'] == 0:
		template_name =  'integracion_tbk/success_normal.html'
		context = {}
		context['transaction'] = transaction

		if len(transaction_detail) != 0:
			context['transaction_detail'] = transaction_detail

		context['token'] = token
		return render(request, template_name, context)

	else:
		template_name = 'integracion_tbk/failure_normal.html'
		context = {}
		context['transaction'] = transaction

		if len(transaction_detail) != 0:
			context['transaction_detail'] = transaction_detail

		context['token'] = token

		return render(request,template_name, context)

#termino de la transaccion
# Create your views here.
from django.contrib.auth.decorators import login_required

import string
from django.contrib import messages

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

def normal_final(request):
	template_name = 'integracion_tbk/final_normal.html'
	context = {}
	token = request.POST.get('token_ws')
	context['token'] = token

	return render(request, template_name, context)




'''
@login_required
@action(detail=True, methods=['post'])
def normal_final(request):
	template_name = 'integracion_tbk/final_normal.html'

	order = Order.objects.get(user=request.user, ordered=False)
	order_item_list = OrderItem.objects.all()
	order_buy_list = Order_buy.objects.all()



	order_buy_list = Order_buy()
	order_buy_list.user = request.user
	order_buy_list.buy_order = create_ref_code()
	order_buy_list.save()


	amount = int(order.get_total() * 100)
	# create the payment

	payment = Payment()
	payment.user = request.user
	payment.amount = order.get_total()
	payment.stripe_charge_id = order_buy_list.buy_order
	payment.save()



	order_items = order.items.all()
	order_items.update(ordered=True)
	order_items.update(buy_order=order_buy_list.buy_order)

	for item in order_items:
		item.save()

	order.ordered = True
	order.payment = payment
	order.user = request.user
	order.buy_order = order_buy_list.buy_order
	order.save()

	messages.success(request, "Su orden fue exitosa!.")

	return render(request, template_name)

'''