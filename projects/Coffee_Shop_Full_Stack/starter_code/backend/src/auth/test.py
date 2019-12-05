import http.client

conn = http.client.HTTPSConnection("irzelindo.auth0.com")

payload = "{\"client_id\":\"UeA0xQQN55lIuSz5MH2jpxxWR5R6AmUI\",\"client_secret\":\"kotpZ8sJED36QhSgoqUmrZh314NEghSP9s8g_Feq-JLdPoqQOtTMRA9Vtt2Cn2Ry\",\"audience\":\"coffeeshop\",\"grant_type\":\"client_credentials\"}"

headers = {'content-type': "application/json"}

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
