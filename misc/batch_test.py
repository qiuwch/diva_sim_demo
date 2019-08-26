from unrealcv import client

client.connect()

# res = client.request('vbatch 2')
# print(res)
# res = client.request_async('vget /camera/0/lit png')
# # Need to send request without waiting for reply
# print(res)
# res = client.request_async('vget /camera/0/depth npy')
# print(res)

res = client.request([
    'vget /camera/0/lit png',
    'vget /camera/0/depth npy',
    'vget /camera/1/lit png',
    'vget /camera/1/depth npy'
])
print(res)
print(len(res))
# print(res)
