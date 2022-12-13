# import graphene
# from rx import Observable


# class MySubscription(graphene.ObjectType):
#     hello = graphene.String()
#     try:
#         def resolve_hello(root, info):
#             print('info')
#             print(info)
#             return Observable.interval(3000) \
#                 .map(lambda i: "hello world!")
#     except Exception() as e:
#         print(e)
