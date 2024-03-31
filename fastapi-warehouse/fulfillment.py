import time
from main import redis, ProductModel

key = 'order-completed'
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
                try:
                    product = ProductModel.get(obj['product_id'])
                    product.quantity -= int(obj['quantity'])
                    product.save()
                    print(product)
                except Exception as e:
                    redis.xadd(name='refund-order', fields=obj)
    except Exception as e:
        print(str(e))
    time.sleep(3)