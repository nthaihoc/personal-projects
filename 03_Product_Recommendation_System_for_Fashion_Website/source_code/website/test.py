from intasend import APIService

API_PUBLISHABLE_KEY = 'ISPubKey_test_2e0a0587-2f6d-489e-a9f4-66b4cbb80a1f'
API_TOKEN = 'ISSecretKey_test_18a6df81-1995-40bb-8c53-d3bfd9e38d15'


service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)

create_order = service.collect.mpesa_stk_push(phone_number='254720000000', email='test@gmail.com', amount=100,
                                              narrative='Purchase of items')

print(create_order)