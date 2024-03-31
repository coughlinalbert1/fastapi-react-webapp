import time
from main import redis, ProductOrderResponse

key = 'refund-order'
group = 'warehouse-group'
consumer = 'consumer1'

# Creating a key with this group if it does not already exist
try:
    redis.xgroup_create(name=key, groupname=group, mkstream=True)
    print(f"Group {group} created")
except Exception as e:
    print(str(e))

# Consuming messages from the group
while True:
    try:
        # '>' means intercept all strings that come through the stream
        results = redis.xreadgroup(groupname=group, consumername=consumer, streams={key: '>'}) 
        print(results)
        if results:
            for result in results:
                obj = result[1][0][1]
                order = ProductOrderResponse.get(obj['pk'])
                order.status = 'refunded'
                order.save()
                print(order)
    except Exception as e:
        print(str(e))
    time.sleep(3)